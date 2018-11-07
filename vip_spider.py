import json
import re

from scrapy.spiders import Request
from w3lib.url import add_or_replace_parameter

from skuscraper.utils.decorators import remove_duplicates
from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'vip'
    start_urls = ['https://www.vip.com/']
    allowed_domains = ['vip.com']

    default_brand = 'Vip'


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    categories_url = 'https://category.vip.com/ajax/getSellingCategory.php?callback=getTopCategory&tree_id=117'
    sub_categories_url_t = 'https://category.vip.com/ajax/getTreeList.php?callback=getSubCategory{}&cid={}&tree_id=117'
    product_api = 'https://category.vip.com/ajax/mapi.php?'
    product_url_t = '{}detail-{}-{}.html'


class VipParseSpider(BaseParseSpider):
    price_css = '.pbox-price ::text, .pbox-market ::text, .pbox-yen::text,' \
                ' .prepay-fav-title ::text, .J-price::text, .J-mPrice::text'
    raw_description_css = '.dc-info table ::text'
    brand_css = '.pib-title-class ::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)

        if self.is_out_of_stock(response):
            garment['out_of_stock'] = True
            garment.update(self.product_pricing_common(response))

        else:
            garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        css = '.other-infoCoding ::text'
        raw_product_id = ''.join(clean(response.css(css)))
        return raw_product_id.split('：')[-1]

    def product_name(self, response):
        return clean(response.css('.pib-title-detail ::text'))[0]

    def product_category(self, response):
        return clean(response.css('.M-class a ::text'))[1:]

    def product_gender(self, response):
        soup = self.product_name(response)
        return self.gender_lookup(soup) or Gender.ADULTS.value

    @remove_duplicates
    def image_urls(self, response):
        css = '.J-mer-bigImgZoom ::attr(href), .J-mer-bigImg::attr(data-original)'
        return clean(response.css(css))

    def is_out_of_stock(self, response):
        css = 'script:contains("skuList")::text'
        return not eval(clean(response.css(css).re('skuList":(.+?\])'))[0])

    def skus(self, response):
        skus = {}

        common_sku = self.product_pricing_common(response)

        colour_css = '.color-selected::attr(title)'
        colour_soup = self.product_name(response)
        colour = clean(response.css(colour_css)) or [self.detect_colour(colour_soup)]

        if all(colour):
            common_sku['colour'] = colour[0]

        for size_s in response.css('.size-list li'):
            sku = common_sku.copy()
            sku['size'] = clean(size_s.css('::attr(title)'))[0]

            if size_s.css('.sli-disabled'):
                sku['out_of_stock'] = True

            sku_id = f'{sku["colour"]}_{sku["size"]}' if all(colour) else sku['size']
            skus[sku_id] = sku

        return skus


class VipCrawlSpider(BaseCrawlSpider):

    def start_requests(self):
        yield Request(url=self.categories_url, callback=self.category_requests)

    def category_requests(self, response):
        meta = response.meta
        meta['trail'] = self.add_trail(response)
        raw_categories = json.loads(re.findall('getTopCategory\((.+)\)', response.text)[0])
        categories = raw_categories['data']['category']

        for category in categories:
            cat_id = category['cate_id']
            url = self.sub_categories_url_t.format(cat_id, cat_id)

            yield Request(url=url, meta=meta.copy(), callback=self.sub_category_requests)

    def sub_category_requests(self, response):
        meta = {'trail': self.add_trail(response)}
        sub_categories_urls = re.findall('url\s*\S:"(.*?)"', response.text)

        for sub_category_url in sub_categories_urls:
            url = response.urljoin(sub_category_url).replace('/ajax', '')
            yield Request(url=url, meta=meta.copy(), callback=self.parse_pagination)

    def parse_pagination(self, response):
        meta = {'trail': self.add_trail(response)}

        css = 'script:contains("productIds")::text'
        text = clean(response.css(css).re_first('merchandise\S, (.+)\)'))
        text = json.loads(text)

        product_details = text['productIds']
        first_section_p_ids = ','.join(product_details[:50])
        last_section_p_ids = ','.join(product_details[50:])
        product_ids = [first_section_p_ids, last_section_p_ids]

        for product_id in product_ids:
            url = add_or_replace_parameter(self.product_api, 'service', 'product_info')
            url = add_or_replace_parameter(url, 'productIds', product_id)
            yield Request(url=url, meta=meta.copy(), callback=self.parse_products)

        total_pages = int(text['pageCount'])

        for page in range(2, total_pages + 1):
            next_page_url = re.sub('-1-0-(\d+)', f'-1-0-{page}', response.url)
            yield Request(url=next_page_url, callback=self.parse_pagination)

    def parse_products(self, response):
        meta = {'trail': self.add_trail(response)}
        products = json.loads(response.text).get('data')
        if not products:
            return

        for p in products['products']:
            p_url = self.product_url_t.format(self.start_urls[0], p['brandId'], p['productId'])
            yield Request(url=p_url, meta=meta.copy(), callback=self.parse_item)


class VipCNParseSpider(VipParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'


class VipCNCrawlSpider(VipCrawlSpider, MixinCN):
    name = MixinCN.retailer + '-crawl'
    parse_spider = VipCNParseSpider()

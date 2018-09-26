import re
import json

from scrapy.spiders import Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    market = 'US'
    retailer = 'loftoutlet-us'
    default_brand = 'Loft'
    gender = Gender.WOMEN.value

    allowed_domains = ['outlet.loft.com', 's7d2.scene7.com']
    start_urls = ['https://outlet.loft.com']

    cat_url_t = 'https://outlet.loft.com/model/services/endecaSimplifiedService?catid={}{}'
    cat_page_url_t = '&goToPage={}'

    image_url_t = 'https://s7d2.scene7.com/is/image/{}'
    image_req_url_t = 'https://s7d2.scene7.com/is/image/LOS/{}_{}_IS?req=set,json'


class LoftOutletParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = self.product_id(raw_product)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(response)
        garment['skus'] = self.skus(response, raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = self.product_category(response)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.image_requests(raw_product)}

        return self.next_request_or_garment(garment)

    def skus(self, response, raw_product):
        skus = {}
        currency = self.currency(response)

        for raw_sku in raw_product:
            money_strs = [raw_sku['listPrice'], currency] + self.sale_price(raw_sku)
            common_sku = self.product_pricing_common(None, money_strs=money_strs)

            for colour in raw_sku['skucolors']['colors']:
                common_sku['colour'] = colour['colorName']

                for size in colour['skusizes']['sizes']:
                    sku = common_sku.copy()
                    sku['size'] = size['sizeAbbr']

                    if size['available'] != 'true':
                        sku['out_of_stock'] = True

                    sku_id = size['skuId']
                    skus[sku_id] = sku

        return skus

    def image_requests(self, raw_product):
        pid = self.product_id(raw_product)
        colours = [colour['colorCode'] for variant in raw_product for colour in variant['skucolors']['colors']]
        return [Request(url=self.image_req_url_t.format(pid, c), callback=self.parse_images) for c in colours]

    def parse_images(self, response):
        garment = response.meta['garment']
        raw_images = re.search('"item":(.*)}}', response.text).group(1)
        images = json.loads(raw_images)

        if isinstance(images, list):
            garment['image_urls'] += [self.image_url_t.format(im['i']['n']) for im in images]
        else:
            garment['image_urls'] += [self.image_url_t.format(images['i']['n'])]

        return self.next_request_or_garment(garment)

    def product_id(self, raw_product):
        return raw_product[0]['prodId']

    def raw_product(self, response):
        css = 'script:contains(__NEXT_DATA__)::text'
        raw_product = clean(response.css(css).re('"products":(\[{.+}\]),"ship'))[0]
        return json.loads(raw_product)

    def product_description(self, raw_product):
        return [v for k, v in raw_product[0].items() if 'bulletPoint' in k and v]

    def product_care(self, raw_product):
        return [raw_product[0]['garmentCare']] + raw_product[0]['fabricationContent'].split(',')

    def sale_price(self, raw_product):
        if 'salePrice' in raw_product:
            return [raw_product['salePrice']]

        raw_price = [promo for promo in raw_product['promoMessages'] if '$' in promo]
        return [re.search('(\$[\d\.?]+)', raw_price[0]).group(1)] if raw_price else []

    def currency(self, response):
        return clean(response.css('script:contains(__NEXT_DATA__)::text').re('"currency":"(.+?)"'))[0]

    def product_name(self, raw_product):
        return raw_product[0]['displayName']

    def product_category(self, response):
        return response.meta['breadcrumbs']

    def merch_info(self, raw_product):
        return [promo for promo in raw_product[0]['promoMessages'] if '$' not in promo]


class LoftOutletCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LoftOutletParseSpider()

    allowed_categories = ['Accessories &amp; Shoes', 'Clothing', 'Petites']
    denied_categories = {'cat3950040', 'cat3950062', 'cat4150003', 'cat3950029', 'cat4150004', 'cat3950042'}

    def parse_start_url(self, response):
        categories_css = '#__next-error+script+script::text'
        categories = clean(response.css(categories_css).re('Nav":({.*})},"res'))[0]
        category_ids = self.filter_category_ids(json.loads(categories).items())

        meta = {'trail': self.add_trail(response)}
        for cat_id in category_ids:
            url = add_or_replace_parameter(self.cat_url_t, 'catid', cat_id)
            yield Request(url=url, callback=self.parse_category, meta=meta.copy())

    def parse_category(self, response):
        raw_products = json.loads(response.text)['response']
        response.meta['trail'] = self.add_trail(response)

        yield from self.product_requests(response, raw_products)

        yield from self.pagination_requests(response, raw_products)

    def product_requests(self, response, raw_products):
        response.meta['breadcrumbs'] = [cat['label'] for cat in raw_products['breadcrumbs']]

        for product in raw_products['productInfo']['records']:

            if 'quickLookUrl' not in product:
                return

            url = response.urljoin(product['quickLookUrl'])
            yield Request(url=url, callback=self.parse_item, meta=response.meta.copy())

    def pagination_requests(self, response, raw_products):
        cat_page = int(url_query_parameter(response.url, 'goToPage', 1))
        pagination_count = raw_products['productInfo']['paginationCount']

        if pagination_count >= cat_page:
            meta = {'trail': response.meta['trail']}
            url = add_or_replace_parameter(response.url, 'goToPage', cat_page+1)
            yield Request(url=url, callback=self.parse_category, meta=meta.copy())

    def filter_category_ids(self, cats):
        return {v['catid'] for k, v in cats if self.is_required_category(k)} - self.denied_categories

    def is_required_category(self, category):
        return any(cat in category for cat in self.allowed_categories)

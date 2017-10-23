import re
import json
import math

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'americaneagle-jp'
    allowed_domains = ['aeo.jp']
    lang = 'ja'
    market = 'JP'
    page_size = 150
    gender_map = [
        ('women', 'women'),
        ('ウィメンズ', 'women'),
        ('men', 'men'),
        ('メンズ', 'men'),
    ]
    brand_map = [
        ('AEO', 'American Eagle Outfitters'),
        ('AE', 'aerie'),
    ]
    url_regex = 'catMainLarge":"\/\/(.+?)"}'
    pagination_url = "{b_url}&pp={page_no}&sort=00"
    start_urls = ['http://www.aeo.jp/top/CSfTop.jsp?cd=1']


class AmericanEagleParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = 'span#productPrice  span:not([class="tax_excluded"]) ::text'

    def parse(self, response):
        p_id = self.product_id(response)
        garment = self.new_unique_garment(p_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.product_image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        return garment

    def skus(self, response):
        skus = {}
        common = self.product_pricing_common_new(response)
        raw_skus = response.xpath('//script[contains(text(),"catMainLarge")]').re('gpObj.matrix(.+)')[0]
        for raw_sku in re.findall("({.+?})", raw_skus):
            sku = common.copy()
            sku_json = json.loads(raw_sku)
            if not sku_json.get('goodsNo'):
                continue
            sku['colour'] = sku_json.get('colorNm')
            sku['size'] = sku_json.get('dispSizeNm')
            if sku_json.get('size1OutOfStock') == "0":
                sku['out_of_stock'] = True
            skus['{}_{}'.format(sku['colour'], sku['size'])] = sku
        return skus

    def product_care(self, response):
        return clean(response.css('.hiddenSP .pdp-about-bullets li::text'))

    def product_category(self, response):
        return clean(response.css('.breadcrumb a ::text'))[1:]

    def product_id(self, response):
        return clean(response.css('.pdp-about-txt .pdp-about-cs ::text'))[0]

    def product_name(self, response):
        return clean(response.css('.psp-product-txt .psp-product-name::text'))[0]

    def product_description(self, response):
        return clean(response.css('.pdp-about-info-txt .pdp-about-copy-specifics::text'))

    def product_image_urls(self, response):
        return response.xpath('//script[contains(text(),"catMainLarge")]').re(self.url_regex)

    def merch_info(self, response):
        return clean(response.css('.psp-product-yousave ::text'))

    def product_gender(self, response):
        category = "".join(self.product_category(response)).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in category:
                return gender
        return 'unisex-adults'

    def product_brand(self, response):
        name = self.product_name(response)
        for brand_string, brand in self.brand_map:
            if brand_string in name:
                return brand
        return 'American Eagle'


class AmericanEagleCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = AmericanEagleParseSpider()
    products_css = '.ProductItem'

    rules = (
        Rule(LinkExtractor(restrict_css=['.WOMEN', '.MEN']), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super(AmericanEagleCrawlSpider, self).parse(response)
        if "&pp=" in response.url:
            return
        total_pages = int(clean(response.css('.CategoryContentsWrap span[id="totalCount"]::text'))[0]) / self.page_size
        total_pages = math.ceil(total_pages)
        for p_no in range(2, total_pages + 1):
            url = self.pagination_url.format(b_url=response.url, page_no=p_no)
            response.meta['trail'] = self.add_trail(response)
            yield Request(url, meta=response.meta, callback=self.parse)

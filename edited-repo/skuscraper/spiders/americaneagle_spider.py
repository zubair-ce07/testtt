import re
import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_parameter

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'americaneagle-jp'
    allowed_domains = ['aeo.jp']
    lang = 'ja'
    market = 'JP'
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
    image_url_re = 'catMainLarge":"\/\/(.+?)"}'
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
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        return garment

    def skus(self, response):
        skus = {}
        common = self.product_pricing_common_new(response)
        raw_skus = response.xpath('//script[contains(text(),"catMainLarge")]/text()').extract_first()
        skus_json = json.loads(re.findall('gpObj.matrix = (.+);', raw_skus)[0])
        for colour_sku in skus_json:
            for size_sku in colour_sku:
                sku = common.copy()
                if not size_sku.get('goodsNo'):
                    continue
                sku['colour'] = size_sku.get('colorNm')
                sku['size'] = size_sku.get('dispSizeNm')
                if size_sku.get('size1OutOfStock') == "0":
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

    def image_urls(self, response):
        return response.xpath('//script[contains(text(),"catMainLarge")]').re(self.image_url_re)

    def merch_info(self, response):
        return clean(response.css('.psp-product-yousave ::text'))

    def product_gender(self, response):
        category = " ".join(self.product_category(response)).lower()
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
    page_size = 150
    products_css = '.ProductItem'
    listing_css = ['.WOMEN', '.MEN']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super(AmericanEagleCrawlSpider, self).parse(response)
        if url_query_parameter(response.url, "pp"):
            return
        total_items = clean(response.css('.CategoryContentsWrap span[id="totalCount"]::text'))[0]
        total_pages = int(total_items) // self.page_size + 1
        for p_no in range(2, total_pages + 1):
            url = self.pagination_url.format(b_url=response.url, page_no=p_no)
            response.meta['trail'] = self.add_trail(response)
            yield Request(url, meta=response.meta, callback=self.parse)

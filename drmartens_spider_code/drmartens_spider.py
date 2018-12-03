import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request

from .base import BaseParseSpider, BaseCrawlSpider
from ..parsers.genders import Gender


class Mixin:
    retailer = 'drmartens'
    market = 'JP'
    allowed_domains = ['drmartens.com']
    start_urls = ['https://www.drmartens.com/jp/']


class DrmartensParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = '#tab1 ::text'
    care_css = '#tab2 ::text'
    price_css = '.price::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['url'] = response.url
        garment['image_urls'] = self.product_image_urls(response)
        garment['category'] = self.product_category(response)
        garment['skus'] = self.product_skus(response)

        return garment

    def product_category(self, response):
        css = '.breadcrumbs a::text'
        return response.css(css).extract()[1:-1]

    def color_sku(self, response, raw_sku_id):
        skus = {}
        common = self.product_pricing_common(response)
        raw_skus = self.raw_sku(response, raw_sku_id)
        common['colour'] = self.color(response, raw_sku_id)

        for raw_sku in json.loads(raw_skus):
            sku = common.copy()
            sku['size'] = raw_sku['display']
            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku

            if not raw_sku['stockLevel']:
                sku['out_of_stock'] = True

        return skus

    def product_skus(self, response):
        skus = {}
        raw_sku_ids = self.sku_ids(response)

        for raw_sku_id in raw_sku_ids:
            skus.update(self.color_sku(response, raw_sku_id))

        return skus

    def color(self, response, id):
        css = f'#{id}::attr(title)'
        return response.css(css).extract_first()

    def raw_sku(self, response, id):
        css = f'#{id}::attr(data-size-displays)'
        return response.css(css).extract_first()

    def sku_ids(self, response):
        css = '.colour-pallet-device span::attr(id)'
        return response.css(css).extract()

    def product_image_urls(self, response):
        css = '.sync2.owl-carousel img::attr(src)'
        return response.css(css).extract()

    def product_id(self, response):
        css = '.product-code ::text'
        return response.css(css).extract_first()

    def product_name(self, response):
        css = '.box-details h1 ::text'
        return response.css(css).extract_first()


class DrmartensCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DrmartensParseSpider()
    category_allow_r = ['c/womens$', 'c/mens$', 'c/kids$']
    product_allow_r = r'/p/[a-z-]+'
    rules = (
        Rule(
            LinkExtractor(allow=category_allow_r),
            callback="gender_category",
        ),
        Rule(
            LinkExtractor(allow=product_allow_r),
            callback="parse_item",
        ),
    )

    def gender_category(self, response):
        if 'c/womens' in response.url:
            return self.parse_and_add_women(response)
        elif 'c/mens' in response.url:
            return self.parse_and_add_men(response)
        elif 'c/kids' in response.url:
            return self.parse_and_add_unisex_kids(response)


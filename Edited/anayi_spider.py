import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'anayi'
    allowed_domains = ['anayi.com']
    default_brand = 'ANAYI'


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    start_urls = ['https://www.anayi.com']


class AnayiParseSpider(BaseParseSpider):
    raw_description_css = '.detail-info td::text'
    price_css = '.block-detail__price ::text'
    gender = Gender.WOMEN.value

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        css = 'tr:contains(商品番号) td::text'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = '.block-detail__name::text'
        return clean(response.css(css))[0]

    def image_urls(self, response):
        css = '.detail-thumbnails__item-trigger .lazyload::attr(data-srcset)'
        return clean(response.css(css))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        colours = clean(response.css('[name="color"]::attr(value)'))
        raw_skus_s = response.css('.detail-size__list')

        for index, raw_sku_s in enumerate(raw_skus_s):
            for size_s in raw_sku_s.css('li'):
                common_sku['colour'] = colour = colours[index]
                sku = common_sku.copy()
                sku['size'] = size = clean(size_s.css('[type="radio"]::attr(value)'))[0]

                if not clean(size_s.css('li + input::attr(value)')):
                    sku['out_of_stock'] = True

                skus[f'{colour}_{size}'] = sku

        return skus


class AnayiCrawlSpider(BaseCrawlSpider, Mixin):
    listings_css = ['.header-submenu__item', '.viewmore']
    products_css = '.block-list__main .item__main'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class AnayiJPParseSpider(AnayiParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class AnayiJPCrawlSpider(AnayiCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = AnayiJPParseSpider()

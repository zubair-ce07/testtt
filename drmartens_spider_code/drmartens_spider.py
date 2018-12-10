import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'drmartens-jp'
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
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        garment['skus'] = self.skus(response)

        return garment

    def skus(self, response):
        skus = {}
        sku_ids_css = '.colour-pallet-device span::attr(id)'
        common = self.product_pricing_common(response)

        for raw_sku_id in clean(response.css(sku_ids_css)):
            colour_css = f'#{raw_sku_id}::attr(title)'
            raw_sku_css = f'#{raw_sku_id}::attr(data-size-displays)'
            common['colour'] = clean(response.css(colour_css))[0]

            for raw_sku in json.loads(clean(response.css(raw_sku_css))[0]):
                sku = common.copy()
                sku['size'] = self.one_size if '1 - SIZE' == raw_sku['display'] else raw_sku['display']
                sku_id = f'{sku["colour"]}_{sku["size"]}'
                skus[sku_id] = sku

                if not raw_sku['stockLevel']:
                    sku['out_of_stock'] = True

        return skus

    def product_gender(self, garment):
        trail = [' '.join(trail) for trail in garment['trail']]
        soup = ' '.join(garment['category'] + [garment['name']] + clean(trail))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, response):
        return clean(response.css('.breadcrumbs a::text'))[1:-1]

    def image_urls(self, response):
        css = '.sync2.owl-carousel img::attr(src)'
        return clean(response.css(css))

    def product_id(self, response):
        return clean(response.css('.product-code ::text'))[0][:-3]

    def product_name(self, response):
        return clean(response.css('.box-details h1 ::text'))[0]


class DrmartensCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DrmartensParseSpider()
    category_allow_r = ['c/womens$', 'c/mens$', 'c/kids$']
    products_css = '.box-product-list'
    rules = (
        Rule(LinkExtractor(allow=category_allow_r), callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item"),
    )


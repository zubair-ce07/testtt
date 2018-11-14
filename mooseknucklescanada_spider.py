import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'mooseknucklescanada-ca'
    market = 'CA'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['https://www.mooseknucklescanada.com/']


class MooseKnucklesCAParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    care_css = '.tab-content ::text'
    raw_description_css = '.tab-content ::text'
    price_x = "//*[contains(@class, 'cent-mx')]//*[contains(@class, 'price')]/text()"

    def parse(self, response):
        pid = self.magento_product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_name(self, response):
        css = '.product-name h1::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.add-to-cart button::attr(data-category)'
        return clean(response.css(css))[0].split('/')

    def image_urls(self, response):
        css = ".more-views ~ [type='text/javascript']"
        raw_urls = response.css(css).extract()[0]
        raw_urls = json.loads(re.findall('{.+}', raw_urls)[0])
        return raw_urls['base_image'].values()

    def product_gender(self, response):
        css = '.add-to-cart button::attr(data-category)'
        soup = ' '.join(clean(response.css(css)))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        raw_skus = self.magento_product_data(response)
        skus = {}

        for sku_id, raw_sku in self.magento_product_map(raw_skus).items():
            sku = common_sku.copy()
            sku['colour'] = raw_sku[0]['label']
            sku['size'] = raw_sku[1]['label']

            if set(raw_sku[0]['products']) & set(raw_sku[0]['products']):
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus


class MooseKnucklesCACrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseKnucklesCAParseSpider()

    listing_css = [
        '.level0',
        '.pager'
    ]
    product_css = [
        '.ls-products-grid__images'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    ]

import json
import re

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'cabourn-us'
    market = 'US'
    default_brand = 'Nigel Cabourn'

    allowed_domains = ['cabourn.com']
    start_urls = ['https://www.cabourn.com/']


class CabournParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'
    price_css = '.regular-price ::text , .special-price ::text'
    raw_description_css = '.pp-description ::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        return garment

    def product_id(self, response):
        return clean(response.css('.no-display ::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name ::text'))[0]

    def image_urls(self, response):
        css = '.MagicToolboxSelectorsContainer ::attr(href),.MagicToolboxContainer ::attr(href)'
        return clean(response.css(css))

    def product_category(self, response):
        trail = response.meta['trail'][1][1]
        return trail.split('/')[3:]

    def product_gender(self, response):
        soup = ' '.join(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def variants(self, response):
        variant_r = '({"attributes.*}})'
        script_text = clean(response.xpath('//script[contains(., "Product.ConfigDefaultText")]/text()'))
        raw_text = re.findall(variant_r, script_text[0])
        raw_json = json.loads(raw_text[0])

        return raw_json

    def skus(self, response):
        retailer_sku = self.product_id(response)
        common_sku = self.product_pricing_common(response)
        colour = self.detect_colour_from_name(response)

        if colour:
            common_sku['colour'] = colour

        skus = {}
        raw_json = self.variants(response)
        for variant in raw_json['attributes']['174']['options']:
            sku = common_sku.copy()
            size = variant['label']
            sku['size'] = size

            skus[f'{retailer_sku}_{size}'] = sku

        return skus


class CabournCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = CabournParseSpider()

    listings_css = [
        '.sub-menu',
        '.next.i-next'
    ]
    products_css = [
        '.product-name'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


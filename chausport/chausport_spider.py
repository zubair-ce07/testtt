import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'chausport'
    allowed_domains = ['chausport.com']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.chausport.com']

    size_labels = ['taille vêtement', 'pointures']


class ParseSpider(BaseParseSpider):
    attribute_css_t = '.left-col .catalog_product_attribute_label{}' \
                      '+.catalog_product_attribute_value ::text'

    description_css = '[itemprop="description"] p::text, .short-description ::text'
    care_css = attribute_css_t.format(':not(:contains("ouleur"))')
    brand_css = '.product-name .brand::text'
    price_css = '.left-col .price-box :not(.reduction-percentage)::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)

        return garment

    def product_id(self, response):
        url = clean(response.css('#product_addtocart_form::attr(action)'))[0]
        return re.findall(r'product/(.*?)/form', url)[0]

    def raw_name(self, response):
        return clean(response.css('.product-name .model::text'))[0]

    def product_name(self, response):
        return self.remove_colours_from_text(self.raw_name(response))

    def product_category(self, response):
        css = self.attribute_css_t.format(':contains("Style")')
        category = clean(response.css(css))
        return category + [clean(response.css('title::text'))[0].split('-')[1]]

    def product_gender(self, response):
        return self.gender_lookup(clean(response.css('title::text'))[0]) or Gender.ADULTS.value

    def image_urls(self, response):
        return clean(response.css('.container-image a::attr(href)'))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour = soupify(clean(response.css(self.attribute_css_t.format(':contains("ouleur")'))))

        if colour:
            common_sku['colour'] = colour

        for raw_size in self.get_raw_sizes(response):
            sku = common_sku.copy()
            sku['size'] = raw_size['label']
            sku['out_of_stock'] = not bool(raw_size['saleable'][0])
            sku_id = f'{colour}_{sku["size"]}' if colour else sku['size']
            skus[sku_id] = sku

        return skus

    def get_raw_sizes(self, response):
        raw_attributes = clean(response.css('#optionsConfig::attr(value)'))

        if not raw_attributes:
            return [{'label': self.one_size, 'saleable': [True]}]

        raw_attributes = json.loads(raw_attributes[0])['attributes']
        return [ra['options'] for ra in raw_attributes.values()
                if ra['label'].lower() in self.size_labels][0]

    def merch_info(self, response):
        return clean(response.css('.right-col .flag::text'))


class CrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.menu__sub-item-link',
        '.next-products-link'
    ]
    product_css = ['.product-item .product-link']

    rules = (
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css)),
    )


class ChausportFRParseSpider(MixinFR, ParseSpider):
    name = MixinFR.retailer + '-parse'


class ChausportFRCrawlSpider(MixinFR, CrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = ChausportFRParseSpider()

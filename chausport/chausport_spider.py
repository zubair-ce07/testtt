import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'chausport'
    allowed_domains = ['chausport.com']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.chausport.com']

    lang = 'fr'


class ParseSpider(BaseParseSpider):
    attribute_css_t = '.left-col .catalog_product_attribute_label{}' \
                      ' +.catalog_product_attribute_value {}::text'
    description_css = '.left-col [itemprop="description"] p::text, ' \
                      '.left-col .short-description p::text'
    care_css = attribute_css_t.format(
        ':not(:contains("Couleur")):not(:contains("couleurs"))',
        'span'
    )
    brand_css = '.right-col .product-name .brand::text'
    price_css = '.left-col .regular-price::text,' \
                '.left-col [itemprop="priceCurrency"]::attr(content),' \
                '.left-col .old-price::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)

        return [garment] + self.colour_requests(response)

    def product_id(self, response):
        return re.findall(r'-(\d+?)\.html', response.url)[0]

    def product_name(self, response):
        raw_name = clean(response.css('.product-name .model::text'))[0]
        return self.remove_colours_from_text(raw_name)

    def product_category(self, response):
        css = self.attribute_css_t.format(':contains("Style")', 'span')
        category_in_features = clean(response.css(css))
        category_in_title = clean(response.css('title::text'))[0].split('-')[1]

        return category_in_features + [category_in_title]

    def product_gender(self, response):
        return self.gender_lookup(clean(response.css('title::text'))[0]) or Gender.ADULTS.value

    def image_urls(self, response):
        return clean(response.css('.container-image a::attr(href)'))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour_css = soupify(
            [
                self.attribute_css_t.format(':contains("Couleur")', 'a'),
                self.attribute_css_t.format(':contains("Couleur")', 'span'),
                self.attribute_css_t.format(':contains("couleurs")', 'span'),
            ],
            delimiter=','
        )
        colour = self.detect_colour(soupify(clean(response.css(colour_css))), multiple=True)

        if colour:
            common_sku['colour'] = colour

        for raw_size in self.get_raw_sizes(response):
            sku = common_sku.copy()
            sku['size'] = raw_size['label']
            oos = raw_size.get('saleable')

            if oos:
                sku['out_of_stock'] = not bool(raw_size['saleable'][0])

            skus[f'{self.product_id(response)}_{sku["size"]}'] = sku

        return skus

    def get_raw_sizes(self, response):
        raw_attributes = clean(response.css('#optionsConfig::attr(value)'))

        if not raw_attributes:
            return [{'label': self.one_size}]

        raw_attributes = json.loads(raw_attributes[0])['attributes']
        raw_sizes = next(
            raw_attributes[ra]['options']
            for ra in raw_attributes.keys()
            if raw_attributes[ra]['label'].lower() == 'pointures'
        )

        return raw_sizes

    def colour_requests(self, response):
        return [Request(url) for url in clean(response.css('.color-wrap a::attr(href)'))]

    def merch_info(self, response):
        return clean(response.css('.right-col .flag::text'))


class CrawlSpider(BaseCrawlSpider):
    listing_css = ['.main-nav-item .inner', '.next-products-link']
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


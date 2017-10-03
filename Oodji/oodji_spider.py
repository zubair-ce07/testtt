import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'oodji-ru'
    lang = 'ru'
    market = 'RU'
    allowed_domains = ['oodji.com']
    start_urls = [
        'http://www.oodji.com/',
    ]


class OodjiParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    image_re = re.compile('(/resize.*)')
    price_css = '::attr(data-oldprice), ::attr(data-price)'

    currency_symbol = '₽'

    gender_map = [
        ('Женская', 'women'),
        ('Мужская', 'men'),
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response)

        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        return garment

    def product_brand(self, response):
        return 'Oodji'

    def skus(self, response):
        skus = {}

        colours_codes = self.colours_and_codes(response)

        for colour_code, colour in zip(colours_codes[0::2], colours_codes[1::2]):
            for size_height in self.product_size_heights(colour_code, response) or ['']:
                for size_s in self.colour_variant_selectors(colour_code, size_height, response):

                    sku_id = clean(size_s.css('::attr(value)'))[0]
                    size = clean(size_s.css(' ::text'))[0]

                    skus[sku_id] = {
                        'colour': colour,
                        'size': size + ('/' + size_height if size_height else '')
                    }

                    skus[sku_id].update(
                        self.product_pricing_common_new(size_s, money_strs=[self.currency_symbol])
                    )

        return skus

    def colours_and_codes(self, response):
        css = '.catalog-section-item-colors ::attr(data-color), .catalog-section-item-colors ::attr(title)'
        return clean(response.css(css))

    def colour_variant_selectors(self, colour_code, growth, response):
        css_t = '#s{colour_code}{h}{growth} label'
        css = css_t.format(colour_code=colour_code, h='h' if growth else '', growth=growth)

        return response.css(css)

    def product_size_heights(self, colour_code, response):
        css_t = '#allh{colour_code} [name="height"]::attr(value)'
        return clean(response.css(css_t.format(colour_code=colour_code)))

    def product_gender(self, response):
        soup = self.product_category(response)
        soup = ' '.join(soup)

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        css = '.small-images__wrap img::attr(src)'
        images = clean(response.css(css))

        return [self.image_re.sub('', img) for img in images]

    def product_id(self, response):
        css = '.size-bar [data-id]::attr(data-id)'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '[itemprop="title"] ::text'
        return clean(response.css(css))[1:]

    def product_name(self, response):
        css = '[itemprop="name"] ::text'
        return clean(response.css(css))[0]

    def raw_description(self, response):
        xpath = '//*[@class="item-description"]//p'
        return clean([self.paragraph_text(d) for d in response.xpath(xpath)])

    def product_description(self, response):
        return [d for d in self.raw_description(response)
                if not self.care_criteria_simplified(d) and "Состав" not in d]

    def paragraph_text(self, para_s):
        return ' '.join(clean(para_s.css(' ::text')))

    def product_care(self, response):
        return [d for d in self.raw_description(response)
                if self.care_criteria_simplified(d) or "Состав" in d]


class DinosCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = OodjiParseSpider()

    listing_css = ['.top-menu', '.page-nav']

    product_css = '.catalog-section-item'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


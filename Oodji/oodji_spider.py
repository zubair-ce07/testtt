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

        garment['brand'] = 'Oodji'
        garment['gender'] = self.product_gender(response)

        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        return garment

    def skus(self, response):
        skus = {}

        for colour_s in response.css('.catalog-section-item-colors a'):
            _skus = self.skus_with_growth(colour_s, response)

            if not _skus:
                _skus = self.skus_with_size(colour_s, growth='', response=response)

            skus.update(_skus)

        return skus

    def skus_with_size(self, colour_s, growth, response):
        skus = {}
        colour_code, colour = self.colour_and_code(colour_s)

        for size_s in self.colour_variant_selectors(colour_code, growth, response):
            sku_id, size = clean(size_s.css('::attr(value), ::text'))

            skus[sku_id] = {
                'colour': colour,
                'size': size + ('/' + growth if growth else '')
            }

            skus[sku_id].update(
                self.product_pricing_common_new(size_s, money_strs=[self.currency_symbol])
            )

        return skus

    def skus_with_growth(self, colour_s, response):
        skus = {}
        colour_code, colour = self.colour_and_code(colour_s)

        for growth in self.product_growths(colour_code, response):
            skus.update(self.skus_with_size(colour_s, growth, response))

        return skus

    def colour_and_code(self, colour_s):
        return clean(colour_s.css('::attr(data-color),::attr(title)'))

    def colour_variant_selectors(self, colour_code, growth, response):
        css_t = '#s{colour_code}{h}{growth} label'
        css = css_t.format(colour_code=colour_code, h='h' if growth else '', growth=growth)

        return response.css(css)

    def product_growths(self, colour_code, response):
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

    def product_description(self, response):
        xpath = '//*[@class="item-description"]//p[not(descendant-or-self::*[contains(text(), "Состав")])]'
        return clean([self.paragraph_text(description_s) for description_s in response.xpath(xpath)])

    def paragraph_text(self, para_s):
        return ' '.join(clean(para_s.css(' ::text')))

    def product_care(self, response):
        xpath = '//*[contains(text(), "Состав")]/parent::*//text()'
        care = clean(response.xpath(xpath))

        return [' '.join(care)]


class DinosCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = OodjiParseSpider()

    listing_css = ['.top-menu', '.page-nav']

    product_css = '.catalog-section-item'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


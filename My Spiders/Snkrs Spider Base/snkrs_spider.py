from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'snkrs'
    allowed_domains = ['snkrs.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls = ['https://www.snkrs.com/en/']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.snkrs.com/fr/']


class SnkrsParseSpider(BaseParseSpider):
    description_css = '#short_description_content p::text, #short_description_content p span::text'
    brand_css = '[itemprop="brand"]::attr(content)'

    merch_map = [
        ('special edition', 'Special Edition'),
        ('limited edition', 'Limited Edition'),
        ('edition limitée', 'Edition limitée'),
        ('édition spéciale', 'Édition spéciale'),
        ('edición limitada', 'Edición Limitada'),
        ('edición especial', 'Edición especial'),
        ('edizione speciale', 'Edizione speciale')
    ]

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response, garment)
        garment['merch_info'] = self.merch_info(garment)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        return clean(response.css('.product_id::text'))[0]

    def product_gender(self, response, garment):
        title_text = clean(response.css('title::text'))
        soup = soupify(garment['category'] + garment['description'] + title_text)
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_name(self, response):
        return self.raw_name(response).split(' - ')[0]

    def image_urls(self, response):
        return clean(response.css('#carrousel_frame li a::attr(href)'))

    def product_category(self, response):
        return clean(response.css('.breadcrumb a ::text'))[1:]

    def merch_info(self, garment):
        soup = soupify(garment['description'])
        return [merch for merch_str, merch in self.merch_map if merch_str.lower() in soup]

    def skus(self, response):
        skus = {}

        current_price = clean(response.css('[itemprop="price"]::attr(content)'))[0]
        previous_price = response.css('#old_price_display .price::text').re_first(r"\d+")
        currency = clean(response.css('[itemprop="priceCurrency"]::attr(content)'))[0]

        colour = self.detect_colour(self.raw_name(response), multiple=True)
        common_sku = {'colour': colour} if colour else {}
        common_sku.update(self.product_pricing_common(
            None, money_strs=[previous_price, current_price, currency]))

        size_css = 'span.size_EU::text, li:not(.hidden) span.units_container::text'
        sizes = clean(response.css(size_css)) or [self.one_size]

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size
            skus[(f"{sku['colour']}_" if colour else '') + size] = sku

        return skus


class SnkrsCrawlSpider(BaseCrawlSpider):
    listings_css = '#menu li'
    product_css = 'div.product-container'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class SnkrsUSParseSpider(MixinUS, SnkrsParseSpider):
    name = MixinUS.retailer + '-parse'


class SnkrsUSCrawlSpider(MixinUS, SnkrsCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = SnkrsUSParseSpider()


class SnkrsFRParseSpider(MixinFR, SnkrsParseSpider):
    name = MixinFR.retailer + '-parse'


class SnkrsFRCrawlSpider(MixinFR, SnkrsCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = SnkrsFRParseSpider()

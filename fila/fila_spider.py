from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify
from ..parsers.genders import Gender


class Mixin:
    retailer = 'fila'


class MixinBR(Mixin):
    default_brand = 'Fila'
    market = 'BR'
    retailer = Mixin.retailer + '-br'
    allowed_domains = ['fila.com.br']
    start_urls = [
        'https://www.fila.com.br/'
    ]


class FilaParseSpider(BaseParseSpider):
    raw_description_css = '.wrap-description ::text, .wrap-long-description ::text'
    price_css = '.pdv_original ::text, .normal_price_span ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['image_urls'].extend(self.image_urls(response))
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)	

    def skus(self, response):
        size_css = '#configurable_swatch_size .swatch-label::text'
        skus = {}

        if not response.css('.normal_price_span'):
            return skus

        common = self.product_pricing_common(response)
        colour = clean(response.css('.wrap-sku > small ::text'))[1]
        common['colour'] = colour

        for size in clean(response.css(size_css)):
            sku = common.copy()
            sku['size'] = size
            skus[f'{colour}_{size}'] = sku

        return skus
    
    def image_urls(self, response):
        return clean(response.css('a.thumb-link > img::attr(src)'))
    
    def product_gender(self, response):
        gender_soup = f'{self.product_name(response)} {soupify(self.product_description(response))}'
        return self.gender_lookup(gender_soup) or Gender.ADULTS.value
        
    def product_category(self, response):
        return clean(response.css('.breadcrumbs a[href] ::text'))[1:]

    def product_id(self, response):
        return clean(response.css('.wrap-sku > small ::text'))[0].split('_')[0]

    def product_name(self, response):
        return clean(response.css('.product-name ::text'))[0]
    
    def colour_requests(self, response):
        css = '.wrap-other-desktop [class="thumb-block "] a::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colours, dont_filter=True) for url in urls]


class FilaCrawlSpider(BaseCrawlSpider):
    listings_css = ['.level2', '[title="Próximo"]']
    products_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )


class FilaBRParseSpider(MixinBR, FilaParseSpider):
    name = MixinBR.retailer + '-parse'


class FilaBRCrawlSpider(MixinBR, FilaCrawlSpider):
    name = MixinBR.retailer + '-crawl'
    parse_spider = FilaBRParseSpider()

    custom_settings = {
        'DOWNLOAD_DELAY': 5.0,  # otherwise website redirects pages to home page
    }

from w3lib.url import add_or_replace_parameter
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'opus-fashion'
    gender = Gender.WOMEN.value


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'

    start_urls = ['https://de.opus-fashion.com/de/']
    allowed_domains = ['de.opus-fashion.com']

    session_url = 'https://ident.casual-fashion.com'


class OpusFashionParseSpider(BaseParseSpider, Mixin):
    price_css = '.c-product-detail .c-product-detail__price :not(.c-price__tax) ::text'
    description_css = '[itemprop=description] ::text,.c-tabs__pane--description .o-list ::text'
    care_css = '.c-tabs__pane--material-care .o-list ::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        colour_urls = clean(response.css('.c-variant:not(.is-active)::attr(href)'))
        return [Request(response.urljoin(url), callback=self.parse_colour) for url in colour_urls]

    def parse_colour(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('.c-product-rating__header::attr(sku)').re_first('(\d+)_'))

    def product_name(self, response):
        return clean(response.css('[itemprop=name] :not([class]) ::text'))[0]

    def product_brand(self, response):
        return clean(response.css('#vue-app>input[checked]::attr(value)'))[0].title()

    def image_urls(self, response):
        return clean(response.css('sim-product-zoom-image::attr(zoom-src-img)'))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = colour = clean(response.css('.c-product-detail__color span ::text'))[0]

        sizes = response.css('.c-product-detail__info option:not(:first-child)')
        for size in sizes:
            sku = common_sku.copy()

            sku['size'] = clean(size.css('::attr(data-size)'))[0]

            if size.css('::attr(disabled)'):
                sku['out_of_stock'] = True

            sku_id = clean(size.css('::attr(value)'))[0]
            skus[sku_id] = sku

        if not sizes:
            common_sku['size'] = self.one_size
            skus[f"{colour}_{self.one_size}"] = common_sku

        return skus


class OpusFashionCrawlSpider(BaseCrawlSpider, Mixin):
    custom_settings = {
        'METAREFRESH_ENABLED': False,
    }

    listings_css = '.c-nav-mobile--opus>.c-nav-list--mobile sim-navigation-list'
    products_css = '.c-product-box'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, tags=['sim-navigation-list-item-title']), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def start_requests(self):
        return [Request(url=self.session_url, callback=self.parse_session_id)]

    def parse_session_id(self, response):
        id = response.text
        url = add_or_replace_parameter(self.start_urls[0], 'idto', id)
        meta = {'trail': self.add_trail(response)}
        return [Request(url, meta=meta.copy(), callback=self.parse)]


class OpusFashionDEParseSpider(OpusFashionParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class OpusFashionDECrawlSpider(OpusFashionCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = OpusFashionDEParseSpider()


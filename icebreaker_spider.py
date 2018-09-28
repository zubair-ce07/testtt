import json

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'icebreaker'
    allowed_domains = ['icebreaker.com']
    default_brand = 'ICEBREAKER'

    def set_locale(self, request):
        request.headers['Cookie'] = self.cookies
        request.meta['dont_merge_cookies'] = True
        return request


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    cookies = 'IBPreferred=UK|UK|en|GBP'
    allowed_domains = ['uk.icebreaker.com']
    start_urls = [
        'https://uk.icebreaker.com/',
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    cookies = 'IBPreferred=US|US|en|USD'
    start_urls = [
        'https://us.icebreaker.com/',
    ]


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    cookies = 'IBPreferred=DE|EU|de|EUR'
    allowed_domains = ['eu.icebreaker.com']
    start_urls = [
        'https://eu.icebreaker.com/de/',
    ]


class MixinCA(Mixin):
    retailer = Mixin.retailer + '-ca'
    market = 'CA'
    cookies = 'IBPreferred=CA|CA|en|CAD'
    allowed_domains = ['ca.icebreaker.com']
    start_urls = [
        'https://ca.icebreaker.com/',
    ]


class MixinDK(Mixin):
    retailer = Mixin.retailer + '-dk'
    market = 'DK'
    cookies = 'IBPreferred=DK|EU|en|DKK'
    allowed_domains = ['eu.icebreaker.com']
    start_urls = [
        'https://eu.icebreaker.com/en/',
    ]


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    cookies = 'IBPreferred=FR|EU|fr_FR|EUR'
    allowed_domains = ['eu.icebreaker.com']
    start_urls = [
        'https://eu.icebreaker.com/fr_FR/',
    ]


class MixinNZ(Mixin):
    retailer = Mixin.retailer + '-nz'
    market = 'NZ'
    cookies = 'IBPreferred=NZ|NZ|en|NZD'
    allowed_domains = ['nz.icebreaker.com']
    start_urls = [
        'https://nz.icebreaker.com/',
    ]


class MixinPL(Mixin):
    retailer = Mixin.retailer + '-pl'
    market = 'PL'
    cookies = 'IBPreferred=PL|EU|en|PLN'
    allowed_domains = ['eu.icebreaker.com']
    start_urls = [
        'https://eu.icebreaker.com/en/',
    ]


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    cookies = 'IBPreferred=SE|EU|en|SEK'
    allowed_domains = ['eu.icebreaker.com']
    start_urls = [
        'https://eu.icebreaker.com/en/',
    ]


class IcebreakerParseSpider(BaseParseSpider):
    price_css = '.product-price ::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(raw_product, response)
        garment['skus'] = {}
        garment['image_urls'] = self.product_images(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        color_urls = clean(response.css('ul.color a::attr(href)'))
        return [self.set_locale(Request(url=url, callback=self.parse_colours)) for url in color_urls]

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.product_images(response)
        size = clean(response.css('.size .selected a::attr(title)'))

        if size:
            garment['skus'].update(self.skus(response))

        else:
            garment['meta']['requests_queue'] += self.size_requests(response)

        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        sizes = clean(response.css('.size .swatchanchor ::attr(href)'))

        return [self.set_locale(Request(url=size_url, dont_filter=True,
                                        callback=self.parse_sizes)) for size_url in sizes]

    def parse_sizes(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        sku = self.product_pricing_common(response)
        sku['colour'] = clean(response.css('.color .selected a::attr(title)'))[0]
        size = clean(response.css('.size .selected a::attr(title)'))
        sku['size'] = size[0] if size else self.one_size
        availability_css = '.availability-msg :contains("out of stock")::text'
        is_sold_out = clean(response.css(availability_css))

        if is_sold_out:
            sku['out_of_stock'] = True

        return {f"{sku['colour']}_{sku['size']}": sku}

    def product_id(self, raw_product):
        return raw_product['id']

    def product_images(self, response):
        css = '[class="thumbnail-tile"]::attr(href),.primary-image::attr(src)'
        return clean(response.css(css))

    def raw_product(self, response):
        json_text = clean(response.css('.product-box::attr(data-selectedproduct)'))[0]
        return json.loads(json_text)

    def product_name(self, response):
        return self.raw_product(response)['name']

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text'))

    def product_gender(self, raw_product, response):
        raw_gender = raw_product['gender']
        categories = self.product_category(response)
        soup = f"{' '.join(categories)} {raw_gender}"

        return self.gender_lookup(soup) or Gender.ADULTS.value

    def raw_description(self, response, **kwargs):
        desc_css = '.description ::text'
        key_css = '.catlabel::text'
        value_css = '.bullet-info::text'
        raw_description = clean(response.css(desc_css))

        raw_description += [f'{clean(d_sel.css(key_css))[0]}{clean(d_sel.css(value_css))[0]}'
                            for d_sel in response.css('.attr') if d_sel.css(value_css)]

        return raw_description


class IcebreakerCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.nav-item .sub-nav-column-container',
        '.infinite-scroll-placeholder'
    ]
    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, attrs=['href', 'data-grid-url']),
             process_request='set_locale', callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), process_request='set_locale', callback='parse_item')
    )


class IceBreakerParseSpiderUK(IcebreakerParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class IceBreakerCrawlSpiderUK(IcebreakerCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderUK()


class IceBreakerParseSpiderUS(IcebreakerParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class IceBreakerCrawlSpiderUS(IcebreakerCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderUS()


class IceBreakerParseSpiderDE(IcebreakerParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class IceBreakerCrawlSpiderDE(IcebreakerCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderDE()


class IceBreakerParseSpiderCA(IcebreakerParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class IceBreakerCrawlSpiderCA(IcebreakerCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderCA()


class IceBreakerParseSpiderDK(IcebreakerParseSpider, MixinDK):
    name = MixinDK.retailer + '-parse'


class IceBreakerCrawlSpiderDK(IcebreakerCrawlSpider, MixinDK):
    name = MixinDK.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderDK()


class IceBreakerParseSpiderFR(IcebreakerParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class IceBreakerCrawlSpiderFR(IcebreakerCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderFR()


class IceBreakerParseSpiderNZ(IcebreakerParseSpider, MixinNZ):
    name = MixinNZ.retailer + '-parse'


class IceBreakerCrawlSpiderNZ(IcebreakerCrawlSpider, MixinNZ):
    name = MixinNZ.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderNZ()


class IceBreakerParseSpiderPL(IcebreakerParseSpider, MixinPL):
    name = MixinPL.retailer + '-parse'


class IceBreakerCrawlSpiderPL(IcebreakerCrawlSpider, MixinPL):
    name = MixinPL.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderPL()


class IceBreakerParseSpiderSE(IcebreakerParseSpider, MixinSE):
    name = MixinSE.retailer + '-parse'


class IceBreakerCrawlSpiderSE(IcebreakerCrawlSpider, MixinSE):
    name = MixinSE.retailer + '-crawl'
    parse_spider = IceBreakerParseSpiderSE()

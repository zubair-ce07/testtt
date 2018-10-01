import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'vagabond'
    allowed_domains = ['vagabond.com']
    default_brand = 'VAGABOND'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['https://vagabond.com/gb/women']


class MixinEU(Mixin):
    retailer = Mixin.retailer + '-eu'
    market = 'EU'
    lang = 'en'
    start_urls = ['https://vagabond.com/de/women']


class MixinPL(Mixin):
    retailer = Mixin.retailer + '-pl'
    market = 'PL'
    lang = 'en'
    start_urls = ['https://vagabond.com/pl/women']


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    lang = 'en'
    start_urls = ['https://vagabond.com/se/women']


class VagabondParseSpider(BaseParseSpider):
    care_css = '#tab3 ::text'
    description_css = '#tab1 :not(a)::text'
    price_css = '.productPrice ::text'

    colour_re = re.compile('Colour:\s(.+)')
    category_re = re.compile('/([^/]+)/?$')
    clean_size_re = re.compile('(\d+)')

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        if self.out_of_stock(response):
            return self.out_of_stock_item(response, response, product_id)

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        if self.is_outlet(response):
            garment['outlet'] = True

        return self.next_request_or_garment(garment)

    def skus(self, response):
        sku_common = self.product_pricing_common(response, price_css=self.price_css)

        colour = self.product_colour(response)
        sku_common['colour'] = colour

        out_of_stock_sizes = self.out_of_stock_sizes(response)
        skus = {}
        for size in self.product_sizes(response):
            sku = sku_common.copy()
            sku['size'] = size

            if size in out_of_stock_sizes:
                sku['out_of_stock'] = True

            skus[f'{colour}_{size}'] = sku

        return skus

    def image_urls(self, response):
        image_urls_css = 'picture::attr(data-src)'
        return [response.urljoin(url) for url in clean(response.css(image_urls_css))]

    def product_id(self, response):
        product_id_css = '.article-number::text'
        return clean(response.css(product_id_css))[0].strip('Article number: ')

    def product_name(self, response):
        name_css = '.product_name ::text'
        return ' '.join(clean(response.css(name_css)))

    def product_gender(self, response):
        trail = response.meta['trail']
        gender_soup = soupify([trail_step[1] for trail_step in trail[1:]]).lower()
        return self.gender_lookup(gender_soup) or Gender.ADULTS.value

    def product_category(self, response):
        trail = response.meta['trail']
        return [self.category_re.findall(trail_step[1])[0] for trail_step in trail[1:]]

    def product_colour(self, response):
        color_css = '#tab2 ::text'
        return response.css(color_css).re_first(self.colour_re)

    def product_sizes(self, response):
        sizes_css = '.sel__box__options::text'
        return [self.clean_size(size) for size in clean(response.css(sizes_css))] or [self.one_size]

    def out_of_stock_sizes(self, response):
        sizes_css = '.sel__box__options::text'
        return [self.clean_size(size) for size in clean(response.css(sizes_css))
                if 'Soon in stock' in size or 'Sold out' in size]

    def out_of_stock(self, response):
        add_to_cart_css = '#addToCart::attr(class)'
        return clean(response.css(add_to_cart_css)) == ['disabled']

    def clean_size(self, size):
        return self.clean_size_re.findall(size)[0]

    def is_outlet(self, response):
        return 'Outlet' in self.product_category(response)


class VagabondCrawlSpider(BaseCrawlSpider):
    listings_css = '.header__main--nav'
    product_css = '.product-list'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class VagabondParseSpiderUK(VagabondParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class VagabondParseSpiderEU(VagabondParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class VagabondParseSpiderPL(VagabondParseSpider, MixinPL):
    name = MixinPL.retailer + '-parse'


class VagabondParseSpiderSE(VagabondParseSpider, MixinSE):
    name = MixinSE.retailer + '-parse'


class VagabondCrawlSpiderUK(VagabondCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = VagabondParseSpiderUK()


class VagabondCrawlSpiderEU(VagabondCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = VagabondParseSpiderEU()


class VagabondCrawlSpiderPL(VagabondCrawlSpider, MixinPL):
    name = MixinPL.retailer + '-crawl'
    parse_spider = VagabondParseSpiderPL()


class VagabondCrawlSpiderSE(VagabondCrawlSpider, MixinSE):
    name = MixinSE.retailer + '-crawl'
    parse_spider = VagabondParseSpiderSE()

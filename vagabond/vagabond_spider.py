import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean


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

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        if self.out_of_stock(response):
            return self.out_of_stock_item(response, response, product_id)

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        if self.is_outlet(response):
            garment['outlet'] = True

        return garment

    def skus(self, response):
        sku_common = self.product_pricing_common(response)

        colour_css = 'span:contains("Colour")::text'
        colour = clean(clean(response.css(colour_css))[0].split(':')[1])
        sku_common['colour'] = colour

        skus = {}
        sizes_css = css = '.sel__box__options::text'
        for size in clean(response.css(sizes_css)) or [self.one_size]:
            sku = sku_common.copy()
            sku['size'] = clean(size.split('-')[0])

            if 'Soon in stock' in size or 'Sold out' in size:
                sku['out_of_stock'] = True

            skus[f'{colour}_{size}'] = sku

        return skus

    def image_urls(self, response):
        css = 'picture::attr(data-src)'
        return [response.urljoin(url) for url in clean(response.css(css))]

    def product_id(self, response):
        css = '.article-number::text'
        return clean(response.css(css))[0].strip('Article number: ')

    def product_name(self, response):
        css = '.product_name ::text'
        return ' '.join(clean(response.css(css)))

    def product_category(self, response):
        return clean([t for t, _ in response.meta.get('trail') or [] if t])

    def out_of_stock(self, response):
        return response.css('#addToCart.disabled')

    def is_outlet(self, response):
        return 'Outlet' in self.product_category(response)


class VagabondCrawlSpider(BaseCrawlSpider):
    women_css = '[data-name="TopLevelBlock_Women_menu"]'
    men_css = '[data-name="TopLevelBlock_Men_menu"]'
    product_css = '.product-list'

    rules = (
        Rule(LinkExtractor(restrict_css=women_css), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=men_css), callback='parse_and_add_men'),
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

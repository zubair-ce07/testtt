import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import url_query_cleaner, url_query_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'bonpoint'
    allowed_domains = ['bonpoint.com']
    default_brand = 'Bonpoint'

    brands = ['Vans', 'Golden Goose for Bonpoint', 'Bonpoint x Izipizi']

    spider_gender_map = [
        ('yam', 'girls'),
        ('ballerinas', 'girls'),
        ('mary', 'girls')
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + "-us"
    market = "US"
    start_urls = ['https://www.bonpoint.com/us/']


class MixinDE(Mixin):
    retailer = Mixin.retailer + "-de"
    market = "DE"
    start_urls = ['https://www.bonpoint.com/de/']


class MixinFR(Mixin):
    retailer = Mixin.retailer + "-fr"
    market = "FR"
    start_urls = ['https://www.bonpoint.com/fr/']


class MixinIT(Mixin):
    retailer = Mixin.retailer + "-it"
    market = "IT"
    start_urls = ['https://www.bonpoint.com/it/']


class MixinES(Mixin):
    retailer = Mixin.retailer + "-es"
    market = "ES"
    start_urls = ['https://www.bonpoint.com/es/']


class MixinPT(Mixin):
    retailer = Mixin.retailer + "-pt"
    market = "PT"
    start_urls = ['https://www.bonpoint.com/pt/']


class MixinAT(Mixin):
    retailer = Mixin.retailer + "-at"
    market = "AT"
    start_urls = ['https://www.bonpoint.com/at/']


class MixinNL(Mixin):
    retailer = Mixin.retailer + "-nl"
    market = "NL"
    start_urls = ['https://www.bonpoint.com/nl/']


class BonpointParseSpider(BaseParseSpider):
    raw_description_css = '#description::text'
    care_css = '#composition::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        self.boilerplate_minimal(garment, response, response.url)

        garment['gender'] = self.product_gender(garment['category'] + [garment['name']]
                                                + [text for text, _ in garment['trail']])
        garment['merch_info'] = self.merch_info(garment['description'] + garment['care'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def get_attribute(self, response, attr):
        return response.css('script:contains(productLayer)').re_first(f'\'{attr}\': "(.*?)"')

    def product_id(self, response):
        return self.get_attribute(response, 'id')

    def product_name_and_color(self, response):
        name_clr = clean(response.css('.product-essential .product-name ::text'))
        if len(name_clr) == 1:
            name_clr.append('')
        return name_clr

    def product_name(self, response):
        name_clr = self.product_name_and_color(response)
        color = self.detect_colour(name_clr[1])
        name_clr[1] = name_clr[1].replace(color.title(), '')
        return ' '.join([name_clr[0]] + name_clr[1].split())

    def product_brand(self, response):
        for brand in self.brands:
            if brand in self.product_name(response):
                return brand
        return self.default_brand

    def product_category(self, response):
        category = self.get_attribute(response, 'category')
        return clean(category.split('/'))

    def product_gender(self, categories):
        gend = self.detect_gender(categories)
        gender = gend if gend else self.gender_lookup(soupify(categories))
        return gender or Gender.KIDS.value

    def merch_info(self, description):
        merch_info = []

        for text in description:
            if 'limited edition' in text.lower():
                merch_info.append('Limited Edition')

        return merch_info

    def image_urls(self, response):
        return clean(response.css('#image-zoom::attr(href)'))

    def skus(self, response):
        sku_ids = []
        skus ={}

        currency = clean(response.css('.product-essential .price ::text'))[0]
        currency = re.sub('(\d+)', '', currency)

        color_str = self.product_name_and_color(response)[1]
        color = (self.detect_colour(color_str) or self.get_attribute(response, 'brand')).title()

        raw_product = self.magento_product_data(response) or {}
        raw_skus = self.magento_product_map(raw_product) if raw_product else None

        if not raw_skus:
            price = float(self.get_attribute(response, 'price'))
            money_str = [price, currency]
            sku = self.product_pricing_common(None, money_strs=money_str)
            sku['size'] = self.one_size
            if color:
                sku['colour'] = color
            skus[self.product_id(response)] = sku
            return skus

        color_id_css = 'script:contains("var initialSelectedColor")'
        color_id = response.css(color_id_css).re_first("var initialSelectedColor = '(.*?)'")

        for sku_id, raw_sku in raw_skus.items():
            if raw_sku[1]['id'] == color_id:
                sku_ids.append(sku_id)

        for sku_id in sku_ids:
            raw_price = raw_product['childProducts'][sku_id]
            money_str = [raw_price['price'], raw_price['finalPrice'], currency]

            sku = self.product_pricing_common(None, money_strs=money_str)
            sku['size'] = raw_skus[sku_id][0]['label']

            if color:
                sku['colour'] = color

            skus[sku_id] = sku

        return skus


class BonpointCrawlSpider(BaseCrawlSpider):
    listings_css = '#nav .level1'
    products_css = '.product-name'
    pagination_css = '.pages a::attr(href)'

    deny_r = ['/looks']

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner),
             callback='parse_item')
    ]

    def parse(self, response):
        yield from super().parse(response)

        if url_query_parameter(response.url, 'p'):
            return

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)
        pagination_urls = clean(response.css(self.pagination_css))

        for url in pagination_urls:
            yield Request(url=url, callback=self.parse, meta=meta.copy())


class BonpointUSParseSpider(MixinUS, BonpointParseSpider):
    name = MixinUS.retailer + '-parse'


class BonpointUSCrawlSpider(MixinUS, BonpointCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = BonpointUSParseSpider()


class BonpointDEParseSpider(MixinDE, BonpointParseSpider):
    name = MixinDE.retailer + '-parse'


class BonpointDECrawlSpider(MixinDE, BonpointCrawlSpider):
    name = MixinDE.retailer + '-crawl'
    parse_spider = BonpointDEParseSpider()


class BonpointFRParseSpider(MixinFR, BonpointParseSpider):
    name = MixinFR.retailer + '-parse'


class BonpointFRCrawlSpider(MixinFR, BonpointCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = BonpointFRParseSpider()


class BonpointITParseSpider(MixinIT, BonpointParseSpider):
    name = MixinIT.retailer + '-parse'


class BonpointITCrawlSpider(MixinIT, BonpointCrawlSpider):
    name = MixinIT.retailer + '-crawl'
    parse_spider = BonpointITParseSpider()


class BonpointESParseSpider(MixinES, BonpointParseSpider):
    name = MixinES.retailer + '-parse'


class BonpointESCrawlSpider(MixinES, BonpointCrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = BonpointESParseSpider()


class BonpointPTParseSpider(MixinPT, BonpointParseSpider):
    name = MixinPT.retailer + '-parse'


class BonpointPTCrawlSpider(MixinPT, BonpointCrawlSpider):
    name = MixinPT.retailer + '-crawl'
    parse_spider = BonpointPTParseSpider()


class BonpointATParseSpider(MixinAT, BonpointParseSpider):
    name = MixinAT.retailer + '-parse'


class BonpointATCrawlSpider(MixinAT, BonpointCrawlSpider):
    name = MixinAT.retailer + '-crawl'
    parse_spider = BonpointATParseSpider()


class BonpointNLParseSpider(MixinNL, BonpointParseSpider):
    name = MixinNL.retailer + '-parse'


class BonpointNLCrawlSpider(MixinNL, BonpointCrawlSpider):
    name = MixinNL.retailer + '-crawl'
    parse_spider = BonpointNLParseSpider()

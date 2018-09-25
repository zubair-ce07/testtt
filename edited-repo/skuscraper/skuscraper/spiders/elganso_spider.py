from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'elganso'
    default_brand = 'elganso'
    allowed_domains = ['elganso.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['https://www.elganso.com/intl_uk/?___store=intl_uk&changecountry=true&pais=UK']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.elganso.com/fr_fr/?___store=fr_fr&changecountry=true&pais=FR']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    start_urls = ['https://www.elganso.com/intl_de/?___store=intl_de&changecountry=true&pais=DE']


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    market = 'ES'
    start_urls = ['https://www.elganso.com/es/?___store=es&changecountry=true&pais=ES']


class MixinCL(Mixin):
    retailer = Mixin.retailer + '-cl'
    market = 'CL'
    lang = 'fr'
    retailer_currency = 'EUR'
    start_urls = ['https://www.elganso.com/es/?___store=es&changecountry=true&pais=CL']


class MixinPT(Mixin):
    retailer = Mixin.retailer + '-pt'
    market = 'PT'
    lang = 'fr'
    retailer_currency = 'EUR'
    start_urls = ['https://www.elganso.com/fr/?___store=fr&changecountry=true&pais=PT']


class MixinNL(Mixin):
    retailer = Mixin.retailer + '-nl'
    market = 'NL'
    lang = 'de'
    retailer_currency = 'EUR'
    start_urls = ['https://www.elganso.com/intl_de/?___store=intl_de&changecountry=true&pais=NL']


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    market = 'IT'
    lang = 'es'
    retailer_currency = 'EUR'
    start_urls = ['https://www.elganso.com/intl_es/?___store=intl_es&changecountry=true&pais=IT']


class MixinBE(Mixin):
    retailer = Mixin.retailer + '-be'
    market = 'BE'
    lang = 'de'
    retailer_currency = 'EUR'
    start_urls = ['https://www.elganso.com/intl_de/?___store=intl_de&changecountry=true&pais=BE']


class ElgansoParseSpider(BaseParseSpider):
    one_sizes = [
        'os',
        'one size'
    ]

    price_css = '.price-box ::text'
    description_css = '.short-description .std:first-child ::text'
    care_css = '.short-description .std:nth-child(n+2)  ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        if self.out_of_stock(response):
            return self.out_of_stock_item(response, response, product_id)

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['category'] = self.product_category(response)
        garment['skus'] = self.skus(response)

        return garment

    @staticmethod
    def product_id(response):
        return response.css('.desc ::text').re_first(r'Ref.\s*(.*)')

    def out_of_stock(self, response):
        return "SOLD OUT" in ''.join(clean(response.css('.productoagotado ::text'))).upper()

    def product_gender(self, response):
        soup = [response.url] + self.product_category(response)
        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def product_category(self, response):
        return clean(response.css('.prod-breadcrumb ::text'))

    @staticmethod
    def image_urls(response):
        return clean(response.css('#carousel-product img::attr(src)'))

    @staticmethod
    def product_name(response):
        return clean(response.css('.data-product .tit ::text'))[0]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        for size_s in response.css('#size-list li'):
            sku = common_sku.copy()
            size = clean(size_s.css('::attr(title)'))[0]
            sku['size'] = size = self.one_size if size.lower() in self.one_sizes else size

            if size_s.css('.disabled'):
                sku['out_of_stock'] = True

            skus[size] = sku

        return skus


class ElgansoCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.panel-body'
    ]

    products_css = [
        '.more-info'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    ]


class ElgansoUKParseSpider(MixinUK, ElgansoParseSpider):
    name = MixinUK.retailer + '-parse'


class ElgansoUKCrawlSpider(MixinUK, ElgansoCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ElgansoUKParseSpider()


class ElgansoFRParseSpider(MixinFR, ElgansoParseSpider):
    name = MixinFR.retailer + '-parse'


class ElgansoFRCrawlSpider(MixinFR, ElgansoCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = ElgansoFRParseSpider()


class ElgansoDEParseSpider(MixinDE, ElgansoParseSpider):
    name = MixinDE.retailer + '-parse'


class ElgansoDECrawlSpider(MixinDE, ElgansoCrawlSpider):
    name = MixinDE.retailer + '-crawl'
    parse_spider = ElgansoDEParseSpider()


class ElgansoESParseSpider(MixinES, ElgansoParseSpider):
    name = MixinES.retailer + '-parse'


class ElgansoESCrawlSpider(MixinES, ElgansoCrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = ElgansoESParseSpider()


class ElgansoCLParseSpider(MixinCL, ElgansoParseSpider):
    name = MixinCL.retailer + '-parse'


class ElgansoCLCrawlSpider(MixinCL, ElgansoCrawlSpider):
    name = MixinCL.retailer + '-crawl'
    parse_spider = ElgansoCLParseSpider()


class ElgansoPTParseSpider(MixinPT, ElgansoParseSpider):
    name = MixinPT.retailer + '-parse'


class ElgansoPTCrawlSpider(MixinPT, ElgansoCrawlSpider):
    name = MixinPT.retailer + '-crawl'
    parse_spider = ElgansoPTParseSpider()


class ElgansoNLParseSpider(MixinNL, ElgansoParseSpider):
    name = MixinNL.retailer + '-parse'


class ElgansoNLCrawlSpider(MixinNL, ElgansoCrawlSpider):
    name = MixinNL.retailer + '-crawl'
    parse_spider = ElgansoNLParseSpider()


class ElgansoITParseSpider(MixinIT, ElgansoParseSpider):
    name = MixinIT.retailer + '-parse'


class ElgansoITCrawlSpider(MixinIT, ElgansoCrawlSpider):
    name = MixinIT.retailer + '-crawl'
    parse_spider = ElgansoITParseSpider()


class ElgansoBEParseSpider(MixinBE, ElgansoParseSpider):
    name = MixinBE.retailer + '-parse'


class ElgansoBECrawlSpider(MixinBE, ElgansoCrawlSpider):
    name = MixinBE.retailer + '-crawl'
    parse_spider = ElgansoBEParseSpider()

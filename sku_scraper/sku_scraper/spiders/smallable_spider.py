from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request, FormRequest

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'smallable'
    allowed_domains = ['smallable.com']

    currency_url = 'https://smallable.com/currency/change'
    country_url = 'https://smallable.com/country/change'

    unwanted_items = [
        'pushchairs', 'poussette', 'cochecitos', 'kinderwagen', 'passaggini',
    ]


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    currency_code = '3'
    country_code = '11'
    start_urls = ['https://en.smallable.com/']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    currency_code = '2'
    country_code = '15'
    start_urls = ['https://en.smallable.com/']


class MixinCA(Mixin):
    retailer = Mixin.retailer + '-ca'
    market = 'CA'
    currency_code = '8'
    country_code = '4'
    start_urls = ['https://en.smallable.com/']


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    lang = 'en'
    currency_code = '5'
    country_code = '46'
    start_urls = ['https://en.smallable.com/']


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    lang = 'en'
    currency_code = '14'
    country_code = '45'
    start_urls = ['https://en.smallable.com/']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    currency_code = '1'
    country_code = '1'
    start_urls = ['https://de.smallable.com/']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    currency_code = '1'
    country_code = '7'
    start_urls = ['https://fr.smallable.com/']


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    market = 'ES'
    currency_code = '1'
    country_code = '5'
    start_urls = ['https://es.smallable.com/']


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    market = 'IT'
    currency_code = '1'
    country_code = '8'
    start_urls = ['https://it.smallable.com/']


class MixinNL(Mixin):
    retailer = Mixin.retailer + '-nl'
    market = 'NL'
    currency_code = '1'
    country_code = '18'
    start_urls = ['https://en.smallable.com/']


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    currency_code = '10'
    country_code = '63'
    start_urls = ['https://en.smallable.com/']


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    currency_code = '9'
    country_code = '43'
    start_urls = ['https://en.smallable.com/']


class MixinKR(Mixin):
    retailer = Mixin.retailer + '-kr'
    market = 'KR'
    lang = 'en'
    currency_code = '13'
    country_code = '56'
    start_urls = ['https://en.smallable.com/']


class MixinHK(Mixin):
    retailer = Mixin.retailer + '-hk'
    market = 'HK'
    lang = 'en'
    currency_code = '6'
    country_code = '65'
    start_urls = ['https://en.smallable.com/']


class MixinSA(Mixin):
    retailer = Mixin.retailer + '-sa'
    market = 'SA'
    currency_code = '11'
    country_code = '64'
    start_urls = ['https://en.smallable.com/']


class MixinKW(Mixin):
    retailer = Mixin.retailer + '-kw'
    market = 'KW'
    currency_code = '15'
    country_code = '62'
    start_urls = ['https://en.smallable.com/']


class MixinQA(Mixin):
    retailer = Mixin.retailer + '-qa'
    market = 'QA'
    currency_code = '12'
    country_code = '61'
    start_urls = ['https://en.smallable.com/']


class SmallableParseSpider(BaseParseSpider):
    brand_css = '[itemprop="brand"] ::text'
    raw_description_css = '[itemprop="description"] ::text'
    sentence_delimiter_r = ':|,'

    def parse(self, response):
        if self.is_unwanted(response):
            return

        garment = self.new_unique_garment(self.product_id(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if self.is_homeware(response, garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        if self.is_outlet(response):
            garment['outlet'] = True

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.sku(response)

        return garment

    def is_unwanted(self, response):
        soup = soupify(clean(response.css('.c-breadcrumb-elem::text'))).lower()
        return any(u in soup for u in self.unwanted_items)

    def is_outlet(self, response):
        return 'outlet' in clean(response.css('title::text'))[0].lower()

    def is_homeware(self, response, garment):
        return 'design' in soupify(garment['category']).lower()

    def product_id(self, response):
        return response.url.split('-')[-1].strip('.html')

    def product_name(self, response):
        return clean(response.css('.p-name::text'))[0]

    def product_category(self, response):
        raw_categories = clean(response.css('.c-breadcrumb-elem::text'))[1:-1]
        return clean(soupify(raw_categories).split('/'))

    def image_urls(self, response):
        return clean(response.css('.image-wrapper .zoomIn::attr(data-src)'))

    def product_gender(self, garment):
        return self.gender_lookup(soupify(garment['category'])) or Gender.ADULTS.value

    def sku(self, response):
        skus = {}

        colour_css = '#form_color_select [selected=selected]::text'
        colour = clean(response.css(colour_css))[0]

        for size_s in response.css('#form_size_select option:not(.hide)'):
            if size_s.css('.oos'):
                continue

            price_css = '::attr(data-price), ::attr(data-discount-price)'
            currency_css = '.-cur-sel > div ::text'

            money_strs = clean(size_s.css(price_css)) + [clean(response.css(currency_css))[0]]
            sku = self.product_pricing_common(response, money_strs=money_strs)

            sku['size'] = clean(size_s.css('::attr(data-size)'))[0]
            sku['colour'] = colour

            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus


class SmallableCrawlSpider(BaseCrawlSpider):
    listings_css = ['.nav-list', '[rel="next"]']
    products_css = ['.ratio-product-item']

    deny_re = ['brands', 'toys', 'marques', 'jouets', 'marcas', 'juguetes',
               'marken', 'spiel', 'marche', 'giocattoli']

    custom_settings = {
        'DOWNLOAD_DELAY': '2'
    }

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def start_requests(self):
        return [Request(self.start_urls[0], callback=self.parse_currency)]

    def parse_currency(self, response):
        return FormRequest(self.currency_url, formdata={'id': self.currency_code},
                           callback=self.parse_location, dont_filter=True)

    def parse_location(self, response):
        return FormRequest(self.country_url, formdata={'id': self.country_code},
                           callback=self.parse, dont_filter=True)


class SmallableUKParseSpider(SmallableParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class SmallableUKCrawlSpider(SmallableCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = SmallableUKParseSpider()


class SmallableUSParseSpider(SmallableParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class SmallableUSCrawlSpider(SmallableCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = SmallableUSParseSpider()


class SmallableCAParseSpider(SmallableParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class SmallableCACrawlSpider(SmallableCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = SmallableCAParseSpider()


class SmallableCNParseSpider(SmallableParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'


class SmallableCNCrawlSpider(SmallableCrawlSpider, MixinCN):
    name = MixinCN.retailer + '-crawl'
    parse_spider = SmallableCNParseSpider()


class SmallableJPParseSpider(SmallableParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class SmallableJPCrawlSpider(SmallableCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = SmallableJPParseSpider()


class SmallableDEParseSpider(SmallableParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class SmallableDECrawlSpider(SmallableCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = SmallableDEParseSpider()


class SmallableFRParseSpider(SmallableParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class SmallableFRCrawlSpider(SmallableCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = SmallableFRParseSpider()


class SmallableESParseSpider(SmallableParseSpider, MixinES):
    name = MixinES.retailer + '-parse'


class SmallableESCrawlSpider(SmallableCrawlSpider, MixinES):
    name = MixinES.retailer + '-crawl'
    parse_spider = SmallableESParseSpider()


class SmallableITParseSpider(SmallableParseSpider, MixinIT):
    name = MixinIT.retailer + '-parse'


class SmallableITCrawlSpider(SmallableCrawlSpider, MixinIT):
    name = MixinIT.retailer + '-crawl'
    parse_spider = SmallableITParseSpider()


class SmallableNLParseSpider(SmallableParseSpider, MixinNL):
    name = MixinNL.retailer + '-parse'


class SmallableNLCrawlSpider(SmallableCrawlSpider, MixinNL):
    name = MixinNL.retailer + '-crawl'
    parse_spider = SmallableNLParseSpider()


class SmallableAEParseSpider(SmallableParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class SmallableAECrawlSpider(SmallableCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = SmallableAEParseSpider()


class SmallableAUParseSpider(SmallableParseSpider, MixinAU):
    name = MixinAU.retailer + '-parse'


class SmallableAUCrawlSpider(SmallableCrawlSpider, MixinAU):
    name = MixinAU.retailer + '-crawl'
    parse_spider = SmallableAUParseSpider()


class SmallableKRParseSpider(SmallableParseSpider, MixinKR):
    name = MixinKR.retailer + '-parse'


class SmallableKRCrawlSpider(SmallableCrawlSpider, MixinKR):
    name = MixinKR.retailer + '-crawl'
    parse_spider = SmallableKRParseSpider()


class SmallableHKParseSpider(SmallableParseSpider, MixinHK):
    name = MixinHK.retailer + '-parse'


class SmallableHKCrawlSpider(SmallableCrawlSpider, MixinHK):
    name = MixinHK.retailer + '-crawl'
    parse_spider = SmallableHKParseSpider()


class SmallableSAParseSpider(SmallableParseSpider, MixinSA):
    name = MixinSA.retailer + '-parse'


class SmallableSACrawlSpider(SmallableCrawlSpider, MixinSA):
    name = MixinSA.retailer + '-crawl'
    parse_spider = SmallableSAParseSpider()


class SmallableKWParseSpider(SmallableParseSpider, MixinKW):
    name = MixinKW.retailer + '-parse'


class SmallableKWCrawlSpider(SmallableCrawlSpider, MixinKW):
    name = MixinKW.retailer + '-crawl'
    parse_spider = SmallableKWParseSpider()


class SmallableQAParseSpider(SmallableParseSpider, MixinQA):
    name = MixinQA.retailer + '-parse'


class SmallableQACrawlSpider(SmallableCrawlSpider, MixinQA):
    name = MixinQA.retailer + '-crawl'
    parse_spider = SmallableQAParseSpider()

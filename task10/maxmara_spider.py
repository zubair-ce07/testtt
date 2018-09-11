import json
from six.moves.urllib_parse import urljoin
from w3lib.url import add_or_replace_parameter

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'maxmara'
    default_brand = 'Max Mara World'

    allowed_domains = ['maxmara.com']
    one_sizes = ['onesize', '-', 'U',"OSO","F"]


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    market = 'IT'
    retailer_currency = 'EUR'
    Lang = 'it'

    start_urls = ['https://it.maxmara.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    retailer_currency = 'GBP'
    Lang = 'en'

    start_urls = ['https://gb.maxmara.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    retailer_currency = 'USD'
    Lang = 'en'

    start_urls = ['https://us.maxmara.com']


class MixinCA(Mixin):
    retailer = Mixin.retailer + '-ca'
    market = 'CA'
    retailer_currency = 'CAD'
    Lang = 'en'

    start_urls = ['https://ca.maxmara.com']


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    retailer_currency = 'JPY'
    Lang = 'ja'

    start_urls = ['https://jp.maxmara.com']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    retailer_currency = 'EUR'
    Lang = 'de'

    start_urls = ['https://de.maxmara.com']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    retailer_currency = 'EUR'
    Lang = 'fr'

    start_urls = ['https://fr.maxmara.com']


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    market = 'ES'
    retailer_currency = 'EUR'
    Lang = 'es'

    start_urls = ['https://es.maxmara.com']


class MixinSE(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    retailer_currency = 'SEK'
    Lang = 'en'

    start_urls = ['https://se.maxmara.com']


class MixinPL(Mixin):
    retailer = Mixin.retailer + '-pl'
    market = 'PL'
    retailer_currency = 'PLN'
    Lang = 'en'

    start_urls = ['https://pl.maxmara.com']


class MixinDK(Mixin):
    retailer = Mixin.retailer + '-dk'
    market = 'DK'
    retailer_currency = 'DKK'
    Lang = 'en'

    start_urls = ['https://dk.maxmara.com']


class MixinKR(Mixin):
    retailer = Mixin.retailer + '-kr'
    market = 'KR'
    retailer_currency = 'KRW'
    Lang = 'ko'

    start_urls = ['https://kr.maxmara.com']


class MixinEU(Mixin):
    retailer = Mixin.retailer + '-eu'
    market = 'EU'
    retailer_currency = 'EUR'
    Lang = 'en'

    start_urls = ['https://eu.maxmara.com']


class MaxMaraParseSpider(BaseParseSpider, Mixin):

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = self.product_id(raw_product)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_minimal(garment, response, response.urljoin(self.product_url(raw_product)))

        garment['name'] = self.product_name(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)

        garment['meta'] = {'requests_queue': self.colors_request(response, raw_product)}
        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        return json.loads(response.text)

    def product_id(self, raw_product):
        return clean(raw_product['baseProduct'])

    def product_url(self, raw_product):
        return clean(raw_product['url'])

    def product_name(self, raw_product):
        return clean(raw_product['summary'] or raw_product['name'])

    def product_description(self, raw_product):
        return clean([raw_product['description']])

    def product_care(self, raw_product):
        return clean([raw_product['care'], raw_product['composition']])

    def image_urls(self, raw_product):
        prod_images_urls = []
        for raw_images in raw_product['images']:

            if raw_images['imageType'] == 'GALLERY' and raw_images['format'] == 'product':
                prod_images_urls.append(raw_images['url'])

        return prod_images_urls

    def product_category(self, raw_product):
        return clean([raw_category['name'] for raw_category in raw_product['categories']])

    def skus(self, raw_product):
        skus = {}

        price = raw_product['price']
        money_strs = [price['value'], price['saleValue'], price['currencyIso']]
        common = self.product_pricing_common(None, money_strs=money_strs)

        common['colour'] = raw_product['colour']
        size_stock_map = self.extract_stock_map(raw_product)

        for raw_size in raw_product['sizes']:
            sku = common.copy()

            size = raw_size['localizedSizeValue']
            sku['size'] = self.one_size if size.lower() in self.one_sizes else size

            if size_stock_map[raw_size['productCode']] == 'outOfStock':
                sku['out_of_stock'] = True

            skus[raw_size['productCode']] = sku

        return skus

    def extract_stock_map(self, raw_product):
        return {raw_stock['code']: raw_stock['stock']['stockLevelStatus']['code']
                for raw_stock in raw_product['variantOptions']}

    def colors_request(self, response, raw_product):
        requests_to_follow = []
        for raw_color in raw_product['baseOptions'][0]['options']:

            if raw_color['code'] != raw_product['code']:
                request = response.follow(f"{raw_color['url']}/json", self.parse_skus)
                requests_to_follow.append(request)

        return requests_to_follow

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(json.loads(response.text)))
        garment['image_urls'] += self.image_urls(json.loads(response.text))
        return self.next_request_or_garment(garment)


class MaxMaraCrawlSpider(BaseCrawlSpider, Mixin):
    pagination_url_t = 'resultsViaAjax?q=&sort=topRated&numberOfPage=0&categoryCode=&' \
                       'numberOfClothes=16&numberOfClothesPE=16&scrollTop='

    listing_xpath = '//div[contains(@class,"cat")]'
    products_css = '.productMainLink'
    deny_urls = ['collection', 'runway', 'icon']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listing_xpath, deny=deny_urls),
             callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=lambda url: f'{url}/json'),
             callback='parse_item')
    )

    def parse(self, response):
        yield from super().parse(response)

        if response.css('.pagination'):
            request = Request(self.pagination_url(response), callback=self.parse_listing)

            yield self.add_meta(request, response)

    def parse_listing(self, response):
        for next_page in range(1, json.loads(response.text)['totalPage'] + 1):
            pagination_url = add_or_replace_parameter(response.url, 'numberOfPage', next_page)
            request = Request(pagination_url, callback=self.parse_pagination)

            yield self.add_meta(request, response)

    def parse_pagination(self, response):
        raw_products = json.loads(response.text)['searchPageData']['results'][0]['productList']
        for raw_product in raw_products:
            request = response.follow(f"{raw_product['url']}/json", callback=self.parse_item)
            yield self.add_meta(request, response)

    def pagination_url(self, response):
        q = clean(response.css('#variables::attr(data-query-on-ready)'))[0]
        pagination_url = add_or_replace_parameter(self.pagination_url_t, 'q', q)

        category_code = clean(response.css('#category-div::attr(data-category)'))[0]
        pagination_url = add_or_replace_parameter(pagination_url, 'categoryCode', category_code)

        return urljoin(response.url + '/', pagination_url)

    def add_meta(self, request, response):
        request.meta['trail'] = self.add_trail(response)
        for meta in ('gender', 'category', 'industry', 'outlet', 'brand'):
            request.meta[meta] = request.meta.get(meta) or response.meta.get(meta)
        return request


class MaxMaraUKParseSpider(MaxMaraParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class MaxMaraUKCrawlSpider(MaxMaraCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = MaxMaraUKParseSpider()


class MaxMaraEUParseSpider(MaxMaraParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class MaxMaraEUCrawlSpider(MaxMaraCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = MaxMaraEUParseSpider()


class MaxMaraKRParseSpider(MaxMaraParseSpider, MixinKR):
    name = MixinKR.retailer + '-parse'


class MaxMaraKRCrawlSpider(MaxMaraCrawlSpider, MixinKR):
    name = MixinKR.retailer + '-crawl'
    parse_spider = MaxMaraKRParseSpider()


class MaxMaraDKParseSpider(MaxMaraParseSpider, MixinDK):
    name = MixinDK.retailer + '-parse'


class MaxMaraDKCrawlSpider(MaxMaraCrawlSpider, MixinDK):
    name = MixinDK.retailer + '-crawl'
    parse_spider = MaxMaraDKParseSpider()


class MaxMaraPLParseSpider(MaxMaraParseSpider, MixinPL):
    name = MixinPL.retailer + '-parse'


class MaxMaraPLCrawlSpider(MaxMaraCrawlSpider, MixinPL):
    name = MixinPL.retailer + '-crawl'
    parse_spider = MaxMaraPLParseSpider()


class MaxMaraSEParseSpider(MaxMaraParseSpider, MixinSE):
    name = MixinSE.retailer + '-parse'


class MaxMaraSECrawlSpider(MaxMaraCrawlSpider, MixinSE):
    name = MixinSE.retailer + '-crawl'
    parse_spider = MaxMaraSEParseSpider()


class MaxMaraESParseSpider(MaxMaraParseSpider, MixinES):
    name = MixinES.retailer + '-parse'


class MaxMaraESCrawlSpider(MaxMaraCrawlSpider, MixinES):
    name = MixinES.retailer + '-crawl'
    parse_spider = MaxMaraESParseSpider()


class MaxMaraFRParseSpider(MaxMaraParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class MaxMaraFRCrawlSpider(MaxMaraCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = MaxMaraFRParseSpider()


class MaxMaraDEParseSpider(MaxMaraParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class MaxMaraDECrawlSpider(MaxMaraCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = MaxMaraDEParseSpider()


class MaxMaraJPParseSpider(MaxMaraParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class MaxMaraJPCrawlSpider(MaxMaraCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = MaxMaraJPParseSpider()


class MaxMaraCAParseSpider(MaxMaraParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class MaxMaraCACrawlSpider(MaxMaraCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = MaxMaraCAParseSpider()


class MaxMaraUSParseSpider(MaxMaraParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class MaxMaraUSCrawlSpider(MaxMaraCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = MaxMaraUSParseSpider()


class MaxMaraITParseSpider(MaxMaraParseSpider, MixinIT):
    name = MixinIT.retailer + '-parse'


class MaxMaraITCrawlSpider(MaxMaraCrawlSpider, MixinIT):
    name = MixinIT.retailer + '-crawl'
    parse_spider = MaxMaraITParseSpider()

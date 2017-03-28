import re
import json
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from scrapy.spiders import Rule
from scrapy import Request, FormRequest
from skuscraper.parsers.jsparser import JSParser
from .base import BaseParseSpider, CurrencyParser, BaseCrawlSpider, clean


class Mixin:
    retailer = 'cubus'
    allowed_domains = ['cubus.com']
    pfx = 'https://cubus.com/'


class MixinSV(Mixin):
    retailer = Mixin.retailer + '-se'
    market = 'SE'
    lang = 'sv'
    start_urls = [Mixin.pfx + 'sv/']


class MixinNO(Mixin):
    retailer = Mixin.retailer + '-no'
    market = 'NO'
    lang = 'no'
    start_urls = [Mixin.pfx + 'no/']


class CubusParseSpider(BaseParseSpider):

    def parse(self, response):
        product = response.meta['product']
        pid = product['Code']

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment['image_urls'] = self.image_urls(product, response)
        garment['name'] = product['Name']
        garment['description'] = [product.get('ShortDescription')]
        garment['brand'] = product['ProductBrand']
        garment['care'] = self.product_care(response)
        garment['gender'] = self.gender(response)
        garment['merch_info'] = clean(product['DiscountMessages'])
        garment['skus'] = self.skus(response, product)
        garment['category'] = response.meta['category']

        return garment

    def currency(self, response):
        pattern = re.compile(r"currency(.*?);")
        currency_string = response.xpath("//script[contains(.,'siteObject."
                                         "currency')]/text()").re(pattern)[0]
        return CurrencyParser.currency(currency_string)

    def product_care(self, response):
        return response.css('.wash-symbols img::attr(title)').extract()

    def gender(self, response):
        return response.css('.site-sub-navigation-active a::text').extract_first()

    def image_urls(self, product, response):
        return [response.urljoin(img['Url']) for img in product['ProductImages']]

    def common_sku(self, response, product):
        sku = {}
        sku['price'] =CurrencyParser.prices(product['FormattedOfferedPrice'])[0]
        prev_price = CurrencyParser.prices(product['FormattedListPrice'])
        if prev_price != sku['price']:
            sku['previous_prices'] = prev_price
        sku['colour'] = product['VariantColor']['Label']
        sku['currency'] = self.currency(response)

        return sku

    def skus(self, response, product):
        skus = {}
        common_sku = self.common_sku(response, product)
        variants = response.css('.size-picker>li .size-button')

        for variant in variants:
            sku = common_sku.copy()
            quantity = int(variant.css('::attr(data-amount-in-stock)').extract_first())
            sku['out_of_stock'] = quantity < 1
            sku_id = variant.css('::attr(data-sku-id)').extract_first()
            sku['size'] = variant.css('::text').extract_first().strip()
            skus[sku_id] = sku

        return skus


class CubusCrawlSpider(BaseCrawlSpider, Mixin):

    categories = ['.sidebar-nav:first-child']
    listings = ['.site-navigation-links']

    allowed_urls = [
        '/Kollektion/',
        '/Kolleksjon/'
    ]

    denied_urls = [
        '/vis-alle/',
        '/visa-alla/'
    ]

    rules = (

        Rule(LinkExtractor(restrict_css=categories, allow=allowed_urls, deny=denied_urls),
             callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_css=listings), follow=True),

    )

    def product_requests(self, products, response):
        requests = []
        category = response.css('.url-wrap.current a::text').extract_first()
        for product in products:
            url = urljoin(self.start_urls[0], product['Url'])
            request = Request(url, meta={'product': product, 'category': [category]},
                              callback=self.parse_item, priority=1)
            requests.append(request)

        return requests

    def product_script(self, response):
        return response.xpath("//script[contains(.,'currentCatalogNode=')]/text()")

    def catalog_node(self, response):
        pattern = re.compile(r"currentCatalogNode=\"(.*?)\",")
        return self.product_script(response).re(pattern)

    def first_page_products(self, response):
        pattern = re.compile(r"products=(.*?),ProductSearchPageId")
        items = "var product = " + self.product_script(response).re(pattern)[0]

        products = JSParser(items)
        return self.product_requests(products['product'], response)

    def next_page_request(self, response):
        listing_url = urljoin(self.start_urls[0], 'api/product/post')
        request = FormRequest(listing_url,
                              formdata={
                                  'Language': response.meta['language'],
                                  'MarketId': response.meta['market'],
                                  'CatalogNode': response.meta['catalog_node'],
                                  'Page': str(response.meta['next_page']),
                                  'ProductSearchPageId': response.meta['page_id'],
                              },
                              headers={
                                  'Accept': '*/*',
                              },
                              meta=response.meta.copy(),
                              dont_filter=True,
                              callback=self.parse_next_page
                              )
        request.meta['next_page'] += 1
        return request

    def parse_pagination(self, response):

        if not self.catalog_node(response):
            return
        for request in self.first_page_products(response):
            yield request

        url = response.css('.site-language-selector-list a::attr(href)').extract_first()
        pattern = re.compile(r"siteObject.init\((.*?)\)")
        script = response.xpath("//script[contains(.,'siteObject.init')]"
                                "/text()").re(pattern)[0].replace('"', '')

        response.meta['catalog_node'] = self.catalog_node(response)[0]
        response.meta['next_page'] = 1
        response.meta['page_id'] = url.split('=')[1]
        response.meta['language'], response.meta['market'] = script.split(',')

        yield self.next_page_request(response)

    def parse_next_page(self, response):
        page = json.loads(response.text)
        products = page['Products']

        for request in self.product_requests(products, response):
            yield request

        if page['HaveMoreItems']:
            yield self.next_page_request(response)


class CubusSVParseSpider(CubusParseSpider, MixinSV):
    name = MixinSV.retailer + '-parse'


class CubusSVCrawlSpider(CubusCrawlSpider, MixinSV):
    name = MixinSV.retailer + '-crawl'
    parse_spider = CubusSVParseSpider()


class CubusNOParseSpider(CubusParseSpider, MixinNO):
    name = MixinNO.retailer + '-parse'


class CubusNOCrawlSpider(CubusCrawlSpider, MixinNO):
    name = MixinNO.retailer + '-crawl'
    parse_spider = CubusNOParseSpider()


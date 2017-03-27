import re
import json
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from scrapy.spiders import Rule
from scrapy import Request, FormRequest
from skuscraper.parsers.jsparser import JSParser
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'cubus-sv'
    market = 'SE'
    lang = 'sv'
    allowed_domains = ['cubus.com']
    start_urls = ['https://cubus.com/sv']


class CubusParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

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

        if response.meta['first_page']:
            skus = self.first_page_skus(product)
            category = self.first_page_product_category(product)
        else:
            skus = self.skus(response, product)
            category = self.product_category(response)

        garment['category'] = category
        garment['skus'] = skus
        return garment

    def formatted_price(self, price):
        return float(clean(price.split(':')[0]))

    def skus(self, response, product):
        skus = {}
        previous_price = self.formatted_price(product['FormattedListPrice'])
        price = self.formatted_price(product['FormattedOfferedPrice'])
        currency = 'SEK'
        common_sku = self.common_sku(price, previous_price,
                                     product['VariantColor']['Label'], currency)

        variants = response.css('.size-picker>li .size-button')

        for variant in variants:
            sku = common_sku.copy()
            quantity = int(variant.css('::attr(data-amount-in-stock)').extract_first())
            sku['out_of_stock'] = True if quantity < 1 else False
            sku_id = variant.css('::attr(data-sku-id)').extract_first()
            sku['size'] = variant.css('::text').extract_first().strip()
            skus[sku_id] = sku

        return skus

    def product_category(self, response):
        return response.css('.back-to a::text').extract()

    def first_page_product_category(self, product):
        category = [product['SeoCategoryName']]
        return category if category else [product['ProductDepartment']]

    def product_care(self, response):
        return response.css('.wash-symbols img::attr(title)').extract()

    def gender(self, response):
        return response.css('.site-sub-navigation-active a::text').extract_first()

    def image_urls(self, product, response):
        return [urljoin(response.url, image['Url']) for image in product['ProductImages']]

    def common_sku(self, price, prev_price, colour, currency):
        sku = {}
        sku['price'] = price
        if prev_price != sku['price']:
            sku['previous_prices'] = prev_price
        sku['colour'] = colour
        sku['currency'] = currency

        return sku

    def first_page_skus(self, product):
        skus = {}
        common_sku = self.common_sku(product['OfferedPrice']['Price'],
                                     [product['ListPrice']['Price']],
                                     product['VariantColor']['Label'],
                                     product['OfferedPrice']['Currency'])
        for sku in product['Skus']:
            variant = common_sku.copy()
            variant['out_of_stock'] = True if sku['Quantity'] == 0 else False
            variant['size'] = sku['Size']
            skus[sku['Id']] = variant
        return skus


class CubusCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = CubusParseSpider()

    listings = ['.sidebar-nav:first-child']
    listing_url = 'https://cubus.com/sv/api/product/post'
    products = ['.product-list-wrap']

    rules = (

        Rule(LinkExtractor(restrict_css=listings, allow='/Kollektion/'),
             callback='parse_pagination', follow=True),
        Rule(LinkExtractor(allow=('/sv/Dam/', '/sv/Herr/', '/sv/Barn/',
                                  '/sv/Baby/')), follow=True),

    )

    def product_requests(self, products, first_page):
        requests = []
        for product in products:
            url = urljoin(Mixin.start_urls[0], product['Url'])
            request = Request(url, meta={'product': product, 'first_page': first_page},
                              callback=self.parse_item, priority=1)
            requests.append(request)
        return requests

    def page_id(self, response):
        url = response.css('.site-language-selector-list a::attr(href)').extract_first()
        return url.split('=')[1]

    def product_script(self, response):
        return response.xpath("//script[contains(.,'currentCatalogNode=')]/text()")

    def catalog_node(self, response):
        pattern = re.compile(r"currentCatalogNode=\"(.*?)\",")
        return self.product_script(response).re(pattern)

    def first_page_products(self, response):
        pattern = re.compile(r"products=(.*?),ProductSearchPageId")
        items = "var product = " + self.product_script(response).re(pattern)[0]

        products = JSParser(items)
        return self.product_requests(products['product'], True)

    def next_page_request(self, response):
        request = FormRequest(self.listing_url,
                              formdata={
                                  'Language': 'sv',
                                  'MarketId': '8WS',
                                  'CatalogNode': response.meta['catalog_node'],
                                  'Page': str(response.meta['next_page']),
                                  'ProductSearchPageId': response.meta['page_id'],
                              },
                              headers={
                                  'Accept': '*/*',
                              },
                              meta={'next_page': response.meta['next_page'],
                                    'catalog_node': response.meta['catalog_node'],
                                    'page_id': response.meta['page_id']},
                              dont_filter=True,
                              callback=self.parse_next_page
                              )
        request.meta['next_page'] += 1
        return request

    def parse_pagination(self, response):
        if not self.catalog_node(response):
            return
        requests = self.first_page_products(response)
        for request in requests:
            yield request
        response.meta['catalog_node'] = self.catalog_node(response)[0]
        response.meta['next_page'] = 1
        response.meta['page_id'] = self.page_id(response)
        yield self.next_page_request(response)

    def parse_next_page(self, response):
        page = json.loads(response.text)
        products = page['Products']
        requests = self.product_requests(products, False)
        for request in requests:
            yield request

        if page['HaveMoreItems']:
            yield self.next_page_request(response)

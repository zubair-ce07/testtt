import re
import json

import js2py
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Product(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    skus = scrapy.Field()


class MonsoonLondonParser(scrapy.Spider):
    name = "monsoonlondon_parser"
    currency_conversion_rate = None
    currency_code = None

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def set_currency(self, currency_code, currency_conversion_rate):
        self.currency_code = currency_code
        self.currency_conversion_rate = currency_conversion_rate

    def parse(self, response):
        product = Product()
        variant = self.get_product_variant(response)

        product['retailer_sku'] = variant['retailer_sku']
        product['name'] = self.get_product_name(response)
        product['brand'] = 'Monsoon'
        product['category'] = self.get_product_categories(response)
        product['image_urls'] = self.get_product_images(response)
        product['url'] = response.url
        product['description'] = self.get_product_description(variant)
        product['care'] = self.get_product_care(response)
        product['gender'] = self.get_product_gender(response)
        product['skus'] = [self.generate_product_sku(variant)]

        sku_requests = self.generate_sku_requests(response, product, variant)
        return self.get_request(sku_requests) or product

    def parse_variant(self, response):
        product = response.meta['product']
        sku_requests = response.meta['sku_requests']
        variant = self.get_product_variant(response)
        images = self.get_product_images(response)

        for image in images:
            if image not in product['image_urls']:
                product['image_urls'].append(image)

        product['skus'].append(self.generate_product_sku(variant))
        return self.get_request(sku_requests) or product

    def generate_product_sku(self, raw_sku):
        return {
            'sku_id': raw_sku['sku_id'],
            'price': int(float(raw_sku['price']) * self.currency_conversion_rate * 100),
            'is_in_stock': bool(int(raw_sku['stock'])),
            'currency': self.currency_code,
            'color': raw_sku['color'],
            'size': raw_sku['size']
        }

    @staticmethod
    def generate_header(response):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': response.url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive'
        }

    def generate_sku_requests(self, response, product, variant):
        url = 'https://www.monsoonlondon.com/en-us/view/component/' \
              'QuickliveProductDetailsComponentController'
        product_code = self.get_product_code(response)
        component_uid = self.get_component_uid(response)
        category_path = self.get_category_path(response)
        catalog_id = self.get_catalog_id(response)

        headers = self.generate_header(response)

        sku_requests = []

        for color_sel in self.get_product_colors(response):
            for size_sel in self.get_product_sizes(response):
                if self.is_current_response(color_sel, size_sel, variant):
                    continue

                form_data = {
                    'componentUid': component_uid,
                    'catalogId': catalog_id,
                    'categoryPath': category_path,
                    'productCode': product_code,
                    'attributes[\'colour\']': color_sel,
                    'attributes[\'size\']': size_sel
                }

                request = scrapy.FormRequest(url, headers=headers, formdata=form_data,
                                             callback=self.parse_variant, dont_filter=True)

                request.meta['sku_requests'] = sku_requests
                request.meta['product'] = product
                sku_requests.append(request)

        return sku_requests

    @staticmethod
    def is_current_response(color_sel, size_sel, variant):
        return (color_sel.lower() == variant['color'].lower()) \
               and (size_sel.lower() == variant['size'].lower())

    def get_product_variant(self, response):
        raw_variant = self.get_raw_variant(response)

        return {
            'sku_id': raw_variant[0],
            'retailer_sku': raw_variant[1],
            'price': raw_variant[6],
            'description': raw_variant[9],
            'color': raw_variant[11],
            'size': raw_variant[12],
            'stock': raw_variant[13],
            'special_price': raw_variant[14]
        }

    @staticmethod
    def get_product_colors(response):
        colors_css = '[id="attributes\'colour\'"] .dropdown-values li::attr(data-code)'
        return response.css(colors_css).extract()

    @staticmethod
    def get_request(requests):
        return requests.pop() if requests else None

    @staticmethod
    def get_product_sizes(response):
        return response.css('[id="attributes\'size\'"] .sizeVariants li::attr(data-code)').extract()

    @staticmethod
    def get_catalog_id(response):
        catalog_id_xpath = '//*[@id="productFormBean"]//input[@name="catalogId"]/@value'
        return response.xpath(catalog_id_xpath).extract_first()

    @staticmethod
    def get_category_path(response):
        category_path_xpath = '//*[@id="productFormBean"]//input[@name="categoryPath"]/@value'
        return response.xpath(category_path_xpath).extract_first()

    @staticmethod
    def get_product_code(response):
        product_code_xpath = '//*[@id="productFormBean"]//input[@name="productCode"]/@value'
        return response.xpath(product_code_xpath).extract_first()

    @staticmethod
    def get_component_uid(response):
        component_uid_xpath = '//*[@id="productFormBean"]//input[@name="componentUid"]/@value'
        return response.xpath(component_uid_xpath).extract_first()

    @staticmethod
    def get_product_description(variant):
        return re.split(r'[.,]', variant['description'])

    @staticmethod
    def get_product_care(response):
        care = response.css('#product-features-content p::text').extract()
        return [c.strip() for c in care if c.strip()][1:]

    @staticmethod
    def get_raw_variant(response):
        raw_variant_xpath = '//script[contains(text(), "addTrackingProduct")]'
        raw_variant = response.xpath(raw_variant_xpath).extract_first()
        raw_variant = re.findall(r'addTrackingProduct\(\s*(.*)\);\s*//', raw_variant,
                                 flags=re.DOTALL)
        raw_variant = f"var variant = [{raw_variant[0]}];"
        return js2py.eval_js(raw_variant)

    @staticmethod
    def get_product_images(response):
        return [response.urljoin(i) for i in response.css('a::attr(data-zoom)').extract()]

    @staticmethod
    def get_product_categories(response):
        return response.css('#breadcrumbs a::text').extract()[1:]

    def get_product_gender(self, response):
        categories = self.get_product_categories(response)

        for category in categories:
            if 'women' in category.lower() or 'wedding' in category.lower():
                return 'Women'

            if 'girl' in category.lower() or 'storm' in category.lower():
                return 'Girls'

            if 'boys' in category.lower():
                return 'Boys'

            if 'newborn' in category.lower():
                return 'Kids'

    @staticmethod
    def get_product_name(response):
        return response.css('.product-info h1::text').extract_first().strip()


class MonsoonLondonCrawler(CrawlSpider):
    name = "monsoonlondon"
    product_parser = MonsoonLondonParser()

    rules = (
        Rule(LinkExtractor(restrict_css='.mainNavigation'), callback='parse_listing'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'monsoonlondon.com'
    ]

    headers = {
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
    }

    def start_requests(self):
        currency_url = 'https://gepi.global-e.com/proxy/initsession/302?optCountry=US&' \
                       'optCurrency=USD&webStoreCode=INT&webStoreInstanceCode=INT&_=153328738322'
        yield scrapy.Request(currency_url, headers=self.headers, callback=self.parse_currency_data)

    def parse_currency_data(self, response):
        raw_currency = re.findall(r'\((.*)\)', response.text)[0]
        raw_currency = js2py.eval_js(f"var currency = {raw_currency};")
        self.product_parser.set_currency(raw_currency['currencyCode'], raw_currency['geFactor'])
        landing_page_url = 'https://www.monsoonlondon.com/en-us/?redirected&skipRedirection=true'

        return scrapy.Request(landing_page_url, callback=self.parse)

    def parse_listing(self, response):
        sub_category_code = response.css('#js-subcategory-code::attr(value)').extract_first()
        if sub_category_code:
            return self.get_raw_listing(sub_category_code)

    def get_raw_listing(self, sub_category_code, page=1):
        raw_listing_url = 'https://www.monsoonlondon.com/en-us/view/services/getProducts.json'
        form_data = {
            'page': str(page),
            'pageSize': '12',
            'sort': 'newIn',
            'category': sub_category_code.split(',')
        }

        request = scrapy.FormRequest(raw_listing_url, formdata=form_data, method='GET',
                                     headers=self.headers, callback=self.parse_raw_listing,
                                     dont_filter=True)
        request.meta['sub_category_code'] = sub_category_code
        return request

    def parse_raw_listing(self, response):
        raw_listing = json.loads(response.text)
        sub_category_code = response.meta['sub_category_code']

        for product in raw_listing['results']:
            request = scrapy.Request(response.urljoin(product['productUrl']),
                                     self.product_parser.parse)
            yield request

        current_page = raw_listing['pagination']['currentPage']
        total_pages = raw_listing['pagination']['totalPages']

        if current_page < total_pages:
            yield self.get_raw_listing(sub_category_code, current_page + 1)

import re
import json

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
    meta = scrapy.Field()


class GarageClothingSpider(CrawlSpider):
    name = "garageclothing"

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    allowed_domains = [
        'garageclothing.com',
        'dynamiteclothing.com'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/cat/', deny=['/fr-ca/', '/us/']), callback='parse'),
        Rule(LinkExtractor(allow=r'/p/'), callback='parse_product'),
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.garageclothing.com/',
        'Origin': 'https://www.garageclothing.com',
        'DNT': '1',
        'Connection': 'keep-alive'
    }

    def start_requests(self):
        yield scrapy.Request(
            'https://www.dynamiteclothing.com/?canonicalSessionRenderSessionId=true',
            headers=self.headers, callback=self.parse_landing_page)

    def parse_landing_page(self, response):
        session_id = response.css('p::text').extract_first()
        return scrapy.Request('https://www.garageclothing.com/ca/',
                              cookies={'JSESSIONID': session_id}, callback=self.parse)

    def parse_product(self, response):
        product = Product()

        product['retailer_sku'] = self.get_product_retailer_sku(response)
        product['name'] = self.get_product_name(response)
        product['brand'] = 'Garage'
        product['gender'] = 'Female'
        product['category'] = []
        product['image_urls'] = []
        product['url'] = response.url.split(';')[0]
        product['description'] = self.get_product_description(response)
        product['care'] = self.get_product_care(response)
        product['skus'] = []

        product['meta'] = {
            'price': self.get_product_price(response),
            'colors': self.get_product_colors(response),
            'requests': self.generate_image_requests(response, product)
        }

        return self.get_request_or_product(product)

    def parse_product_images(self, response):
        product = response.meta['product']
        image_requests = product['meta']['requests']
        product['image_urls'].extend(self.get_product_images(response))

        if image_requests:
            return image_requests.pop()

        product['meta']['requests'] = self.generate_size_requests(product)
        return self.get_request_or_product(product)

    def parse_product_sizes(self, response):
        product = response.meta['product']

        if response.css('#productLengths'):
            product['meta']['requests'] = self.generate_multi_dimension_requests(
                response, product)
            return self.get_request_or_product(product)

        product['skus'].append(self.generate_product_skus(product, response))
        return self.get_request_or_product(product)

    def parse_multi_dimension_product(self, response):
        product = response.meta['product']
        product['skus'].append(self.generate_multi_dimension_product_skus(response, product))
        return self.get_request_or_product(product)

    def generate_image_requests(self, response, product):
        colors = self.get_product_colors(response)
        product_id = self.get_product_retailer_sku(response)
        original_style = self.get_product_original_style(response)

        image_requests = []

        for color_sel in colors.keys():
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/prod/include/pdpImageDisplay.jsp',
                self.parse_product_images, formdata={
                    'colour': color_sel,
                    'productId': product_id,
                    'originalStyle': original_style
                }
            )

            request.meta['product'] = product
            image_requests.append(request)

        return image_requests

    def generate_size_requests(self, product):
        colors = product['meta']['colors']
        product_id = product['retailer_sku']

        size_requests = []

        for color_sel in colors.keys():
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/prod/include/productSizes.jsp',
                self.parse_product_sizes, formdata={
                    'colour': color_sel,
                    'productId': product_id
                }
            )

            request.meta['product'] = product
            size_requests.append(request)

        return size_requests

    def generate_multi_dimension_requests(self, response, product):
        color_code = response.css('span.size::attr(colour)').extract_first()

        multi_dimension_requests = []

        for length in response.css('span.length'):
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/json/sizeInventoryCheckByLengthJSON.jsp',
                self.parse_multi_dimension_product, formdata={
                    'skuId': length.css('span::attr(skuid)').extract_first(),
                    'productId': product['retailer_sku']
                }
            )

            request.meta['product'] = product
            request.meta['skus_color_code'] = color_code
            request.meta['length'] = length.css('span::text').extract_first()

            multi_dimension_requests.append(request)

        return multi_dimension_requests

    @staticmethod
    def generate_product_skus(product, response):
        variants = []

        for size in response.css('span'):
            variant = {
                'color': product['meta']['colors'].get(size.css('span::attr(colour)')
                                                       .extract_first()),
                'sku_id': size.css('span::attr(skuid)').extract_first(),
                'size': size.css('span::text').extract_first(),
                'is_in_stock': bool(int(size.css('span::attr(stocklevel)').extract_first()))
            }

            variant.update(product['meta']['price'])
            variants.append(variant)

        return variants

    def generate_multi_dimension_product_skus(self, response, product):
        color_code = response.meta['skus_color_code']
        length = response.meta['length']
        raw_sizes = self.get_raw_sizes(response)

        variants = []

        for size_sel in raw_sizes['skulist']:
            variant = {
                'sku_id': size_sel['skuId'],
                'size': f"{length}/{size_sel['size']}",
                'is_in_stock': True if size_sel['available'] == 'true' else False,
                'color': product['meta']['colors'].get(color_code)
            }

            variant.update(product['meta']['price'])
            variants.append(variant)

        return variants

    @staticmethod
    def get_product_currency(response):
        currency_xpath = '//script[contains(text(), "priceCurrency")]'
        return response.xpath(currency_xpath).re(r'"priceCurrency": "([A-Z]+)"')[0]

    def get_product_price(self, response):
        prices = {'currency': self.get_product_currency(response)}
        normal_price = response.css('.prodPricePDP::text').extract_first()

        if normal_price:
            prices['price'] = self.get_price_from_string(normal_price)
        else:
            raw_prices = response.css('.prodPricePDP span::text').extract()
            normalized_prices = [self.get_price_from_string(p) for p in raw_prices]
            special_price = min(normalized_prices)
            prices['price'] = special_price
            normalized_prices.remove(special_price)
            prices['previous_price'] = normalized_prices

        return prices

    @staticmethod
    def get_product_colors(response):
        colors_xpath = '//*[@id="prodDetailSwatch"]/*[contains(@class, "prodDetailSwatch")]'
        raw_colors = response.xpath(colors_xpath)
        colors = {}

        for color_sel in raw_colors:
            color_name = color_sel.css('div::attr(colorname)').extract_first()
            color_code = color_sel.css('div::attr(colourid)').extract_first()
            colors[color_code] = color_name

        return colors

    @staticmethod
    def get_product_retailer_sku(response):
        return response.css('#productId::attr(value)').extract_first()

    @staticmethod
    def get_product_name(response):
        return response.css('.prodName::text').extract_first()

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+.?\d+', string)[0]
        return int(float(price) * 100)

    @staticmethod
    def get_product_description(response):
        description_css = '#descTabDescriptionContent p::text, #descTabDescriptionContent::text, ' \
                          '#descTab0Content::text'
        description = response.css(description_css).extract_first()
        return [d.strip() for d in re.split(r'[.,]', description) if d.strip()]

    @staticmethod
    def get_product_care(response):
        return response.css('#descTabDetailsContent li::text').extract()

    @staticmethod
    def get_product_original_style(response):
        return response.css('#originalStyle::attr(value)').extract_first()

    @staticmethod
    def get_raw_sizes(response):
        return json.loads(response.css('p::text').extract_first())

    @staticmethod
    def get_request_or_product(product):
        if product['meta']['requests']:
            return product['meta']['requests'].pop()

        del product['meta']
        return product

    @staticmethod
    def get_product_images(response):
        return [f"https://{i.lstrip('/')}"
                for i in response.css('.addViews a::attr(href)').extract()]

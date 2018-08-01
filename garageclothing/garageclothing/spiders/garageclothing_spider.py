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


class GarageClothingSpider(CrawlSpider):
    name = "garageclothing"

    custom_settings = {
        'DOWNLOAD_DELAY': 2
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

        # return scrapy.Request('https://www.garageclothing.com/ca/crew-neck-sweater/p/'
        #                       'prod3030019.product',
        #                       cookies={'JSESSIONID': session_id}, callback=self.parse_product)
        return scrapy.Request('https://www.garageclothing.com/ca/',
                              cookies={'JSESSIONID': session_id}, callback=self.parse)

    def parse_product(self, response):
        sku = Product(
            retailer_sku=self.get_product_retailer_sku(response),
            name=self.get_product_name(response),
            brand='Garage',
            gender='Female',
            category=[],
            image_urls=[],
            url=response.url.split(';')[0],
            description=self.get_product_description(response),
            care=self.get_product_care(response),
            skus=[],
        )

        meta = {
            'price': self.get_product_price(response),
            'colors': self.get_product_colors(response)
        }

        image_requests = self.generate_image_requests(response, sku, meta)
        for request in image_requests:
            yield request

    def parse_product_images(self, response):
        sku = response.meta['sku']
        meta = response.meta['meta']
        sku['image_urls'].extend(self.get_product_images(response))
        size_requests = self.generate_size_requests(sku, meta)

        if size_requests:
            return size_requests.pop()

    def parse_product_sizes(self, response):
        sku = response.meta['sku']
        meta = response.meta['meta']
        size_requests = response.meta['size_requests']

        if response.css('#productLengths'):
            multi_dimension_requests = self.generate_multi_dimension_requests(response, sku, meta)
            return multi_dimension_requests.pop()
        else:
            for size in response.css('span'):
                sku['skus'].append(self.generate_product_sku(size, meta))

            if size_requests:
                return size_requests.pop()
            return sku

    def parse_multi_dimension_product(self, response):
        sku = response.meta['sku']
        color_code = response.meta['skus_color_code']
        length = response.meta['length']
        multi_dimension_requests = response.meta['multi_dimension_requests']
        meta = response.meta['meta']

        raw_sizes = json.loads(response.css('p::text').extract_first())

        for raw_size in raw_sizes['skulist']:
            sku_variant = self.generate_multi_dimension_product_sku(meta, raw_size, length)
            sku_variant['color'] = self.map_color_code_to_name(color_code, meta['colors'])
            sku['skus'].append(sku_variant)

        if multi_dimension_requests:
            return multi_dimension_requests.pop()
        return sku

    def generate_image_requests(self, response, sku, meta):
        colors = self.get_product_colors(response)
        product_id = self.get_product_retailer_sku(response)
        original_style = self.get_product_original_style(response)

        image_requests = []

        for color_sel in colors:
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/prod/include/pdpImageDisplay.jsp',
                self.parse_product_images, formdata={
                    'colour': color_sel['code'],
                    'productId': product_id,
                    'originalStyle': original_style
                }
            )

            request.meta['sku'] = sku
            request.meta['meta'] = meta
            image_requests.append(request)

        return image_requests

    def generate_size_requests(self, sku, meta):
        colors = meta['colors']
        product_id = sku['retailer_sku']

        size_requests = []

        for color in colors:
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/prod/include/productSizes.jsp',
                self.parse_product_sizes, formdata={
                    'colour': color['code'],
                    'productId': product_id
                }
            )

            request.meta['sku'] = sku
            request.meta['meta'] = meta
            request.meta['size_requests'] = size_requests
            size_requests.append(request)

        return size_requests

    def generate_multi_dimension_requests(self, response, sku, meta):
        color_code = response.css('span.size::attr(colour)').extract_first()

        multi_dimension_requests = []

        for length in response.css('span.length'):
            request = scrapy.FormRequest(
                'https://www.garageclothing.com/ca/json/sizeInventoryCheckByLengthJSON.jsp',
                self.parse_multi_dimension_product, formdata={
                    'skuId': length.css('span::attr(skuid)').extract_first(),
                    'productId': sku['retailer_sku']
                }
            )

            request.meta['sku'] = sku
            request.meta['meta'] = meta
            request.meta['skus_color_code'] = color_code
            request.meta['length'] = length.css('span::text').extract_first()
            request.meta['multi_dimension_requests'] = multi_dimension_requests

            multi_dimension_requests.append(request)

        return multi_dimension_requests

    def generate_product_sku(self, size, meta):
        variant = {
            'color': self.map_color_code_to_name(size.css('span::attr(colour)').extract_first(),
                                                 meta['colors']),
            'sku_id': size.css('span::attr(skuid)').extract_first(),
            'size': size.css('span::text').extract_first(),
            'is_in_stock': bool(int(size.css('span::attr(stocklevel)').extract_first()))
        }

        variant.update(meta['price'])
        return variant

    @staticmethod
    def generate_multi_dimension_product_sku(meta, raw_size, length):
        variant = {
            'sku_id': raw_size['skuId'],
            'size': f"{length}/{raw_size['size']}",
            'is_in_stock': True if raw_size['available'] == 'true' else False
        }

        variant.update(meta['price'])
        return variant

    @staticmethod
    def get_product_currency(response):
        currency_xpath = '//script[contains(text(), "priceCurrency")]'
        return response.xpath(currency_xpath).re(r'"priceCurrency": "([A-Z]+)"')[0]

    def get_product_price(self, response):
        prices = {}

        special_price = response.css('.prodPricePDP .withSale::text').extract_first()
        normal_price = response.css('.prodPricePDP .salePrice::text').extract_first()
        prices['currency'] = self.get_product_currency(response)

        if special_price:
            prices['price'] = self.get_price_from_string(special_price)
            prices['previous_price'] = self.get_price_from_string(normal_price)
        else:
            normal_price = response.css('.prodPricePDP::text').extract_first()
            prices['price'] = self.get_price_from_string(normal_price)

        return prices

    @staticmethod
    def get_product_colors(response):
        colors_xpath = '//*[@id="productColours"]//*[contains(@class, "prodDetail")]' \
                       '/@*[name()="colourid" or name()="colorname"]'
        raw_colors = response.xpath(colors_xpath).extract()
        colors = []

        while raw_colors:
            colors.append({'name': raw_colors.pop(), 'code': raw_colors.pop()})

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
    def get_requests(request, default):
        return request.pop() if request else default

    @staticmethod
    def get_product_images(response):
        return [f"https://{i.lstrip('/')}"
                for i in response.css('.addViews a::attr(href)').extract()]

    @staticmethod
    def map_color_code_to_name(color, color_map):
        for entry in color_map:
            if color == entry['code']:
                return entry['name']

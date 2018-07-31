import re
import json

import scrapy


class GarageClothingSpider(scrapy.Spider):
    name = "garageclothing"

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    allowed_domains = [
        'garageclothing.com',
        'dynamiteclothing.com'
    ]

    def start_requests(self):
        yield scrapy.Request(
            'https://www.dynamiteclothing.com/?canonicalSessionRenderSessionId=true',
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) '
                              'Gecko/20100101 Firefox/62.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.garageclothing.com/',
                'Origin': 'https://www.garageclothing.com',
                'DNT': '1',
                'Connection': 'keep-alive'
            }, callback=self.parse)

    def parse(self, response):
        session_id = response.css('p::text').extract_first()

        return scrapy.Request('https://www.garageclothing.com/ca/',
                              callback=self.parse_landing_page, cookies={'JSESSIONID': session_id})

    def parse_landing_page(self, response):
        listing_css = '.categoryMenuItem .categoryMenuItemSpan a::attr(href)'

        for listing in response.css(listing_css).extract()[:-1]:
            yield response.follow(listing, self.parse_listing)

    def parse_listing(self, response):
        product_css = '.gaProductClickFromGallery::attr(href)'

        for product in response.css(product_css).extract():
            yield response.follow(product, self.parse_product)

        next_page = response.css('#catPageNext::attr(href)').extract_first()
        if next_page:
            return response.follow(next_page, self.parse_listing)

    def parse_product(self, response):
        sku = {'retailer_sku': self.get_product_retailer_sku(response),
               'name': self.get_product_name(response),
               'brand': 'Garage',
               'gender': 'Female',
               'category': [],
               'image_urls': [],
               'url': response.url.split(';')[0],
               'description': self.get_product_description(response),
               'care': self.get_product_care(response),
               'skus': [],
               'sku_fields': {
                'price': self.get_product_price(response),
                'colors': self.get_product_colors(response)
            }}

        img_request_params_queue = self.generate_img_request_params_queue(response)

        if img_request_params_queue:
            return self.generate_image_parse_request(img_request_params_queue, sku)

        del sku['sku_fields']
        return sku

    def parse_product_images(self, response):
        sku = response.meta['sku']
        img_request_params_queue = response.meta['img_request_params_queue']

        sku['image_urls'].extend(self.get_product_images(response))

        if img_request_params_queue:
            return self.generate_image_parse_request(img_request_params_queue, sku)

        size_request_params_queue = self.generate_size_request_params_queue(sku)

        if size_request_params_queue:
            return self.generate_size_parse_request(size_request_params_queue, sku)

        del sku['sku_fields']
        return sku

    def parse_product_sizes(self, response):
        sku = response.meta['sku']
        size_request_params_queue = response.meta['size_request_params_queue']

        if response.css('#productLengths'):
            if sku.get('multi_dimension_params_queue'):
                sku['multi_dimension_params_queue'].extend(
                    self.generate_multi_dimension_params_queue(response))
            else:
                sku['multi_dimension_params_queue'] = \
                    self.generate_multi_dimension_params_queue(response)
        else:
            for size in response.css('span'):
                sku['skus'].append(self.generate_product_sku(size, sku))

        if size_request_params_queue:
            return self.generate_size_parse_request(size_request_params_queue, sku)

        if sku.get('multi_dimension_params_queue'):
            return self.generate_multi_dimension_parse_request(sku)

        del sku['sku_fields']
        return sku

    def parse_multi_dimension_product(self, response):
        sku = response.meta['sku']
        color_code = response.meta['skus_color_code']
        length = response.meta['length']

        raw_sizes = json.loads(response.css('p::text').extract_first())

        for raw_size in raw_sizes['skulist']:
            sku_variant = self.generate_multi_dimension_product_sku(sku, raw_size, length)
            sku_variant['color'] = self.map_color_code_to_name(color_code,
                                                               sku['sku_fields']['colors'])
            sku['skus'].append(sku_variant)

        if sku.get('multi_dimension_params_queue'):
            return self.generate_multi_dimension_parse_request(sku)

        del sku['sku_fields']
        del sku['multi_dimension_params_queue']
        return sku

    def generate_image_parse_request(self, img_request_params_queue, sku):
        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/prod/include/pdpImageDisplay.jsp',
            self.parse_product_images, formdata=img_request_params_queue.pop())

        request.meta['sku'] = sku
        request.meta['img_request_params_queue'] = img_request_params_queue
        return request

    def generate_size_parse_request(self, size_request_params_queue, sku):
        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/prod/include/productSizes.jsp',
            self.parse_product_sizes, formdata=size_request_params_queue.pop())

        request.meta['sku'] = sku
        request.meta['size_request_params_queue'] = size_request_params_queue
        return request

    def generate_multi_dimension_parse_request(self, sku):
        multi_dimension_params_queue = sku['multi_dimension_params_queue'].pop()
        form_params = {
            'skuId': multi_dimension_params_queue['sku_id'],
            'productId': sku['retailer_sku']
        }

        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/json/sizeInventoryCheckByLengthJSON.jsp',
            self.parse_multi_dimension_product, formdata=form_params)

        request.meta['sku'] = sku
        request.meta['skus_color_code'] = multi_dimension_params_queue['color_code']
        request.meta['length'] = multi_dimension_params_queue['length']
        return request

    def generate_img_request_params_queue(self, response):
        colors = self.get_product_colors(response)
        product_id = self.get_product_retailer_sku(response)
        original_style = self.get_product_original_style(response)

        img_request_params_queue = []

        for color in colors:
            img_request_params_queue.append({
                'colour': color['code'],
                'productId': product_id,
                'originalStyle': original_style
            })

        return img_request_params_queue

    @staticmethod
    def generate_size_request_params_queue(sku):
        colors = sku['sku_fields']['colors']
        product_id = sku['retailer_sku']

        size_request_params_queue = []

        for color in colors:
            size_request_params_queue.append({
                'colour': color['code'],
                'productId': product_id
            })

        return size_request_params_queue

    @staticmethod
    def generate_multi_dimension_params_queue(response):
        multi_dimension_params_queue = []
        color_code = response.css('span.size::attr(colour)').extract_first()

        for length in response.css('span.length'):
            multi_dimension_params_queue.append({
                'color_code': color_code,
                'length': length.css('span::text').extract_first(),
                'sku_id': length.css('span::attr(skuid)').extract_first()
            })

        return multi_dimension_params_queue

    def generate_product_sku(self, size, sku):
        variant = {
            'color': self.map_color_code_to_name(size.css('span::attr(colour)').extract_first(),
                                                 sku['sku_fields']['colors']),
            'sku_id': size.css('span::attr(skuid)').extract_first(),
            'size': size.css('span::text').extract_first(),
            'is_in_stock': bool(int(size.css('span::attr(stocklevel)').extract_first()))
        }

        variant.update(sku['sku_fields']['price'])
        return variant

    @staticmethod
    def generate_multi_dimension_product_sku(sku, raw_size, length):
        variant = {
            'sku_id': raw_size['skuId'],
            'size': f"{length}/{raw_size['size']}",
            'is_in_stock': True if raw_size['available'] == 'true' else False
        }

        variant.update(sku['sku_fields']['price'])
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
    def get_product_images(response):
        return [f"https://{i.lstrip('/')}"
                for i in response.css('.addViews a::attr(href)').extract()]

    @staticmethod
    def map_color_code_to_name(color, color_map):
        for entry in color_map:
            if color == entry['code']:
                return entry['name']

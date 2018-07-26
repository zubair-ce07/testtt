import re
import json

import scrapy


class TausendkindSpider(scrapy.Spider):
    name = "garageclothing"
    start_urls = [
        'https://www.garageclothing.com/ca/'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'garageclothing.com',
        'dynamiteclothing.com'
    ]

    def parse(self, response):
        # listing_css = '#main-menu a::attr(href)'
        #
        # for url in response.css(listing_css).extract()[1:]:
        #     yield response.follow(url, self.parse_listing)
        # yield scrapy.Request('https://www.dynamiteclothing.com/?postSessionRedirect=https%3A//www.garageclothing.com/ca/cropped-classic-tee-with-rolled-cuff/p/100036409.product&noRedirectJavaScript=true', self.parse_product)
        yield scrapy.Request('https://www.dynamiteclothing.com/?postSessionRedirect=https%3A//www.garageclothing.com/ca/crew-neck-sweater/p/prod3030019.product&noRedirectJavaScript=true', self.parse_product)

    def parse_listing(self, response):
        raw_listing = self.get_raw_listing(response)

        for listing in raw_listing.values():
            yield response.follow(f"/{listing['url_key']}", self.parse_product)

        next_page = response.css('#pager-next-page::attr(href)').extract_first()
        if next_page:
            return response.follow(next_page, self.parse_listing)

    @staticmethod
    def get_raw_listing(response):
        script = response.xpath('//div/script[contains(text(),"DOMContentLoaded")]').re(r'{.*}')[0]
        return json.loads(script)['list']

    def parse_product(self, response):
        sku = {
            'retailer_sku': self.get_product_retailer_sku(response),
            'name': self.get_product_name(response),
            'brand': 'Garage',
            'gender': 'Female',
            'category': [],
            'image_urls': [],
            'url': response.url.split(';')[0],
            'description': self.get_product_description(response),
            'care': self.get_product_care(response),
            'skus': []
        }

        sku_variant_fields = {
            'price': self.get_product_price(response),
            'currency': 'CAD',
            'colors': self.get_product_colors(response)
        }

        sku['sku_fields'] = sku_variant_fields
        img_request_params_queue = self.generate_img_request_params_queue(response)

        image_request = self.generate_image_parse_request(img_request_params_queue, sku)
        if image_request:
            return image_request

        return sku

    def parse_product_images(self, response):
        sku = response.meta['sku']
        img_request_params_queue = response.meta['img_request_params_queue']

        sku['image_urls'].extend(self.get_product_images(response))

        if img_request_params_queue:
            return self.generate_image_parse_request(img_request_params_queue, sku)

        size_request_params_queue = self.generate_size_request_params_queue(sku)

        size_request = self.generate_size_parse_request(size_request_params_queue, sku)
        if size_request:
            return size_request

        return sku

    @staticmethod
    def get_product_images(response):
        return [f"https://{i.lstrip('/')}"
                for i in response.css('ul.addViews a::attr(href)').extract()]

    def parse_product_sizes(self, response):
        sku = response.meta['sku']
        size_request_params_queue = response.meta['size_request_params_queue']

        for size in response.css('span'):
            sku['skus'].append(self.generate_product_sku(size, sku))

        if size_request_params_queue:
            return self.generate_size_parse_request(size_request_params_queue, sku)

        del sku['sku_fields']
        return sku

    def generate_image_parse_request(self, img_request_params_queue, sku):
        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/prod/include/pdpImageDisplay.jsp',
            self.parse_product_images, formdata=img_request_params_queue.pop())

        request.meta['sku'] = sku
        request.meta['img_request_params_queue'] = img_request_params_queue
        return request

    @staticmethod
    def map_color_code_to_name(color, color_map):
        for entry in color_map:
            if color == entry['code']:
                return entry['name']

    def generate_product_sku(self, size, sku):
        return {
            'price': sku['sku_fields']['price'],
            'color': self.map_color_code_to_name(size.css('span::attr(colour)').extract_first(),
                                                 sku['sku_fields']['colors']),
            'currency': sku['sku_fields']['currency'],
            'sku_id': size.css('span::attr(skuid)').extract_first(),
            'size': size.css('span::text').extract_first(),
            'is_in_stock': bool(int(size.css('span::attr(stocklevel)').extract_first()))
        }

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

    def generate_size_parse_request(self, size_request_params_queue, sku):
        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/prod/include/productSizes.jsp',
            self.parse_product_sizes, formdata=size_request_params_queue.pop())

        request.meta['sku'] = sku
        request.meta['size_request_params_queue'] = size_request_params_queue
        return request

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

    def get_product_price(self, response):
        return self.get_price_from_string(response.css('h2.prodPricePDP::text').extract_first())

    @staticmethod
    def get_product_colors(response):
        raw_colors = response.xpath('//div[@id="productColours"]'
                                    '//div[contains(@class, "prodDetail")]'
                                    '/@*[name()="colourid" or name()="colorname"]').extract()
        colors = []

        while raw_colors:
            colors.append({'name': raw_colors.pop(), 'code': raw_colors.pop()})

        return colors

    @staticmethod
    def get_product_retailer_sku(response):
        return response.css('#productId::attr(value)').extract_first()

    @staticmethod
    def get_product_name(response):
        return response.css('h1.prodName::text').extract_first()

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+.?\d+', string)[0]
        return int(float(price) * 100)

    @staticmethod
    def get_product_description(response):
        description = response.css('#descTabDescriptionContent p::text').extract_first()
        return [d.strip() for d in re.split(r'[.,]', description) if d.strip()]

    @staticmethod
    def get_product_care(response):
        return response.css('#descTabDetailsContent li::text').extract()

    @staticmethod
    def get_product_original_style(response):
        return response.css('#originalStyle::attr(value)').extract_first()

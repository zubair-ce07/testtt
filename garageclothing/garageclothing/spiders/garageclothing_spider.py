import re

import scrapy


class GarageClothingSpider(scrapy.Spider):
    name = "garageclothing"
    session_id = None
    start_urls = [
        'https://www.dynamiteclothing.com/?canonicalSessionRenderSessionId=true'
    ]

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
        self.session_id = response.css('p::text').extract_first()

        yield scrapy.Request('https://www.garageclothing.com/ca/', callback=self.parse_landing_page,
                             cookies={'JSESSIONID': self.session_id})

    def parse_landing_page(self, response):
        listing_css = 'li.categoryMenuItem span.categoryMenuItemSpan a::attr(href)'

        for listing in response.css(listing_css).extract()[:-1]:
            yield response.follow(listing, self.parse_listing)

    def parse_listing(self, response):
        product_css = 'a.gaProductClickFromGallery::attr(href)'

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
                'currency': 'CAD',
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

    def generate_size_parse_request(self, size_request_params_queue, sku):
        request = scrapy.FormRequest(
            'https://www.garageclothing.com/ca/prod/include/productSizes.jsp',
            self.parse_product_sizes, formdata=size_request_params_queue.pop())

        request.meta['sku'] = sku
        request.meta['size_request_params_queue'] = size_request_params_queue
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

    def generate_product_sku(self, size, sku):
        variant = {
            'color': self.map_color_code_to_name(size.css('span::attr(colour)').extract_first(),
                                                 sku['sku_fields']['colors']),
            'currency': sku['sku_fields']['currency'],
            'sku_id': size.css('span::attr(skuid)').extract_first(),
            'size': size.css('span::text').extract_first(),
            'is_in_stock': 'unavailable' not in size.css('span::attr(class)').extract_first()
        }

        variant.update(sku['sku_fields']['price'])
        return variant

    def get_product_price(self, response):
        prices = {}

        special_price = response.css('h2.prodPricePDP span.withSale::text').extract_first()
        normal_price = response.css('h2.prodPricePDP span.salePrice::text').extract_first()

        if special_price:
            prices['price'] = self.get_price_from_string(special_price)
            prices['previous_price'] = self.get_price_from_string(normal_price)
        else:
            normal_price = response.css('h2.prodPricePDP::text').extract_first()
            prices['price'] = self.get_price_from_string(normal_price)

        return prices

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
        description = response.css('#descTabDescriptionContent p::text,'
                                   ' #descTabDescriptionContent::text,'
                                   ' #descTab0Content::text').extract_first()
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
                for i in response.css('ul.addViews a::attr(href)').extract()]

    @staticmethod
    def map_color_code_to_name(color, color_map):
        for entry in color_map:
            if color == entry['code']:
                return entry['name']

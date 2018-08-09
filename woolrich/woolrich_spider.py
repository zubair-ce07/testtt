import json

from scrapy import FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from woolrich.items import Product


class WoolrichSpider(CrawlSpider):
    """
    WoolrichSpider crawls the whole site to get all the available products and
    their details
    """

    name = "woolrich"
    allowed_domains = ['woolrich.com']
    start_urls = [
        'https://www.woolrich.com',
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='.product'), callback='parse_product'),
        Rule(LinkExtractor(restrict_css='.container-child'))
    )

    def parse_product(self, response):
        product = Product()
        product['url'] = self._product_url(response)
        product['name'] = self._product_name(response)
        product['style_number'] = self._product_style_number(response)
        product['trail'] = self._product_trail(response)
        product['description'] = self._product_description(response)
        product['features'] = self._product_features(response)
        product['categories'] = self._product_categories(response)
        product['product_id'] = self._product_id(response)
        product['img_url'] = self._product_img_url(response)
        product['brand'] = 'Woolrich'
        product['skus'] = []

        requests_queue = self._get_color_requests(product['product_id'], response)

        product['requests_queue'] = requests_queue

        return self._make_color_request(product)

    def parse_colors(self, response):
        product = self._product_skus(response)
        return self._make_color_request(product)

    def _make_color_request(self, product):
        requests_queue = product['requests_queue']

        if not requests_queue:
            del product['requests_queue']
            return product

        current_request = requests_queue.pop()
        product['requests_queue'] = requests_queue
        current_request.meta['product'] = product

        return current_request

    def _product_url(self, response):
        return response.url

    def _product_name(self, response):
        return response.css('.productView-product:first-child h1::text').extract_first()

    def _product_style_number(self, response):
        return response.css('.productView-product:first-child strong::text').extract_first().replace('Style #: ', '')

    def _product_trail(self, response):
        return response.css('.breadcrumbs a::attr(href)').extract()[1:]

    def _product_description(self, response):
        return response.css('#details-content::text').extract()

    def _product_features(self, response):
        return response.css('#features-content li::text').extract()

    def _product_categories(self, response):
        return response.css('.breadcrumbs li a::text').extract()[1:]

    def _product_id(self, response):
        return response.css('input[type="hidden"]::attr(value)').extract()[-1]

    def _product_img_url(self, response):
        return response.css('#content-container div[class*="productView-image"] a img::attr(src)').extract_first()

    def _product_skus(self, response):
        data = json.loads(response.text)['data']
        in_stock_attributes = data['in_stock_attributes']
        sku_id = data['sku']
        price = data['price']['without_tax']['formatted']

        product = response.meta['product']
        color_map = response.meta['color']
        product_attributes_map = response.meta['product_attributes_map']

        current_color = color_map["title"]

        for in_stock_attribute in in_stock_attributes:

            for key, values in product_attributes_map.items():
                if key == 'Color':
                    continue

                for value in values:
                    if in_stock_attribute == int(value['code']):
                        sku = {}
                        sku['color'] = current_color
                        sku[key.lower()] = value['title']
                        sku['price'] = price
                        sku['sku_id'] = sku_id
                        product['skus'].append(sku)

        return product

    def _product_attribute_extraction(self, response):
        """
        Extracts all the attributes available for the product available
        on the page like Color, Size, Fitness

        Arguments:
            response (list): response of the request

        Returns:
            (dict, list): Mapped extracted attributes and list of post request
            parameters
        """

        product_attributes = response.css('.productView-options [data-product-attribute]')
        product_attributes_map = dict()
        attribute_params = []

        for product_attribute in product_attributes:
            param_name = product_attribute.css('span:first-child::text').extract()[1]
            attribute_params.append(
                product_attribute.css('input.form-radio::attr(name)').extract_first()
            )
            codes = product_attribute.css('input.form-radio::attr(value)').extract()

            if param_name == "Color":
                titles = product_attribute.css('span.form-option-variant::attr(title)').extract()
            else:
                titles = product_attribute.css('span.form-option-variant::text').extract()

            entities = []

            for code, title in zip(codes, titles):
                entities.append({'code': code, 'title': title})

            product_attributes_map[param_name] = entities

        return product_attributes_map, attribute_params

    def _get_color_requests(self, product_id, response):
        """
        For each color you need to do a post request, so this method
        compiles parameters and url for the request

        Attributes:
            product_id (str): Id for the product
            response (TextResonse): response from the request

        Returns:
            (list): iterable of all the FormRequest
        """

        product_attributes_map, attribute_params = self._product_attribute_extraction(response)
        color_maps = product_attributes_map['Color']
        all_requests = []
        url = 'https://www.woolrich.com/remote/v1/product-attributes/{}'.format(product_id)
        meta = {}
        formdata = {}
        formdata['action'] = 'add'
        formdata['qty[]'] = '1'

        for attribute_map in color_maps:

            formdata['product_id'] = product_id
            formdata[attribute_params[0]] = attribute_map['code']

            meta['color'] = attribute_map
            meta['product_attributes_map'] = product_attributes_map

            all_requests.append(
                FormRequest(url=url, method='POST', callback=self.parse_colors,
                            formdata=formdata, meta=meta
                            )
            )

        return all_requests

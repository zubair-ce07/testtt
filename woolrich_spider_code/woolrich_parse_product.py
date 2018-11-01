import json

import scrapy
from scrapy.http import FormRequest

from woolrich.items import WoolrichItem


class WoolrichParseProduct(scrapy.Spider):
    name = 'woolrich_parse_product'
    product_sku_url_t = 'https://www.woolrich.com/remote/v1/product-attributes/{pid}'

    def parse_product(self, response):
        product = WoolrichItem()
        product['brand'] = 'woolrich'
        product['care'] = self.product_care(response)
        product['category'] = self.product_catagory(response)
        product['description'] = self.product_description(response)
        product['image_urls'] = self.product_image_url(response)
        product['name'] = self.product_name(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['skus'] = {}
        product['url'] = response.url
        self.map_attributes(response, product)
        self.generate_requests(product, response)
        yield self.request_or_item(product)

    def parse_sku(self, response):
        product = response.meta['product']
        raw_sku = json.loads(response.body)
        self.add_sku(product, raw_sku)
        yield self.request_or_item(product)

    def add_sku(self, product, raw_sku):
        data = product['requests_data']
        color_key = data['color_key']
        size_key = data['size_key']
        fit_key = data['fit_key']
        selected_attributes = raw_sku['data']['selected_attributes']
        color = data['color_values'].get(str(selected_attributes[color_key]))
        size, fit = None, None
        sku_key = color
        if size_key:
            size = data['size_values'].get(str(selected_attributes[size_key]))
            sku_key += f'_{size}'
        if fit_key:
            fit = data['fit_values'].get(str(selected_attributes[fit_key]))
            sku_key += f'_{fit}'
        product['skus'][sku_key] = {}
        self.update_sku(product, sku_key, raw_sku, color, size, fit)

    def update_sku(self, product, sku_key, raw_sku, color, size, fit):
        in_stock = raw_sku['data']['instock']
        product['skus'][sku_key]['color'] = color
        if size:
            product['skus'][sku_key]['size'] = size
        if fit:
            product['skus'][sku_key]['fit'] = fit
        if not in_stock:
            product['skus'][sku_key]['out_of_stock'] = True
        self.product_currancy(product, raw_sku, sku_key)

    def product_currancy(self, product, raw_sku, sku_key):
        price = raw_sku['data']['price']['without_tax']['value']
        previous_price = raw_sku['data']['price'].get('rrp_without_tax')
        product['skus'][sku_key]['currancy'] = 'USD'
        product['skus'][sku_key]['price'] = price
        if previous_price:
            product['skus'][sku_key]['previous_price'] = previous_price['value']

    def request_or_item(self, product):
        requests = product['requests_data']['requests']
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request
        del product['requests_data']
        return product

    def map_attributes(self, response, product):
        color_key = self.color_attribute_key(response)
        size_key = self.size_attribute_key(response)
        fit_key = self.fit_attribute_key(response)
        product['requests_data'] = {
            'color_key': color_key,
            'size_key': size_key,
            'fit_key': fit_key,
            'color_values': self.map_color(response, color_key),
            'size_values': self.map_size(response, size_key),
            'fit_values': self.map_fit(response, fit_key),
        }

    def generate_requests(self, product, response):
        data = product['requests_data']
        color_key = data.get('color_key')
        color_key = f"attribute[{color_key}]"
        size_key = data.get('size_key')
        size_key = f"attribute[{size_key}]"
        fit_key = data.get('fit_key')
        fit_key = f"attribute[{fit_key}]"
        color_values = data.get('color_values')
        size_values = data.get('size_values')
        fit_values = data.get('fit_values')
        params = []
        for color_value in color_values:
            if not size_values:
                params.append({color_key: color_value})
            for size_value in size_values:
                if not fit_values:
                    params.append({
                        color_key: color_value,
                        size_key: size_value
                    })
                for fit_value in fit_values:
                    params.append({
                        color_key: color_value,
                        size_key: size_value,
                        fit_key: fit_value,
                    })
        url = self.product_sku_url_t.format(pid=product['retailer_sku'])
        product['requests_data']['requests'] = [FormRequest(url, callback=self.parse_sku,
                                                            formdata=param)
                                                for param in params]

    def map_color(self, response, color_key):
        color_values = {}
        css = '.form-option-swatch::attr(data-product-attribute-value)'
        color_attribute_values = response.css(css).extract()
        for color_value in color_attribute_values:
            color_value_xpath = f'//label[@data-product-attribute-value={color_value}]//span/@title'
            color_values[str(color_value)] = response.xpath(
                color_value_xpath).extract_first()
        return color_values

    def map_size(self, response, size_key):
        size_values = {}
        if not size_key:
            return size_values

        css = '.product-size .form-option::attr(data-product-attribute-value)'
        size_attribute_values = response.css(css).extract()
        for size_value in size_attribute_values:
            size_value_xpath = f'//label[@data-product-attribute-value={size_value}]//span/text()'
            size_values[str(size_value)] = response.xpath(
                size_value_xpath).extract_first()
        return size_values

    def map_fit(self, response, fit_key):
        fit_values = {}
        if not fit_key:
            return fit_values

        fit_values_xpath = f'//input[@name="attribute[{fit_key}]"]/@value'
        fit_attribute_values = response.xpath(fit_values_xpath).extract()
        for fit_value in fit_attribute_values:
            fit_value_xpath = f'//label[@data-product-attribute-value={fit_value}]/span/text()'
            fit_values[str(fit_value)] = response.xpath(
                fit_value_xpath).extract_first()
        return fit_values

    def color_attribute_key(self, response):
        css = '.form-option-swatch::attr(data-swatch-id)'
        return response.css(css).extract_first()

    def size_attribute_key(self, response):
        css = '.product-size input::attr(name)'
        size_key = response.css(css).extract_first()
        if size_key:
            size_key = size_key[10:-1]
        return size_key

    def fit_attribute_key(self, response):
        xpath = '//div[@class="form-field" and @data-product-attribute="set-rectangle"]/input/@name'
        fit_key = response.xpath(xpath).extract_first()
        if fit_key:
            fit_key = fit_key[10:-1]
        return fit_key

    def product_care(self, response):
        care_css = '#features-content > li::text'
        return response.css(care_css).extract()

    def product_catagory(self, response):
        category_css = '.breadcrumb > a::text'
        return response.css(category_css)[-1].extract()

    def product_description(self, response):
        description_css = '#details-content::text'
        return response.css(description_css).extract_first()

    def product_image_url(self, response):
        image_url_css = '.productView-image img::attr(src)'
        return response.css(image_url_css).extract()

    def product_name(self, response):
        name_css = '.productView-title::text'
        return response.css(name_css).extract_first()

    def product_retailer_sku(self, response):
        retailer_sku_css = 'input[name="product_id"]::attr(value)'
        return response.css(retailer_sku_css).extract_first()

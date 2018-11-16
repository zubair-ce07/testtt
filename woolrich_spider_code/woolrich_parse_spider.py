import json

from scrapy import Spider
from scrapy.http import FormRequest

from woolrich.items import WoolrichItem


class WoolrichParseSpider(Spider):
    name = 'woolrich_parse_product'
    product_sku_url_t = 'https://www.woolrich.com/remote/v1/product-attributes/{pid}'
    BRAND = 'Woolrich'
    CURRENCY = 'USD'

    def parse_product(self, response):
        product = WoolrichItem()
        product['brand'] = self.BRAND
        product['care'] = self.product_care(response)
        product['category'] = self.product_catagory(response)
        product['description'] = self.product_description(response)
        product['image_urls'] = self.product_image_url(response)
        product['name'] = self.product_name(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['skus'] = {}
        product['url'] = response.url
        product['requests'] = self.product_sku_requests(response)

        yield self.request_or_item(product)

    def parse_sku(self, response):
        product = response.meta['product']
        product['skus'].update(self.product_sku(response))

        yield self.request_or_item(product)

    def product_sku(self, response):
        sku = {}
        raw_sku = json.loads(response.body)
        size = self.sku_size(response)
        sku_key = f"{response.meta.get('color')}_{size}"

        sku[sku_key] = self.sku_price(response)
        sku[sku_key]['color'] = response.meta.get('color')
        sku[sku_key]['size'] = size

        if not raw_sku['data']['instock']:
            sku[sku_key]['out_of_stock'] = True

        return sku

    def sku_size(self, response):
        raw_size = [response.meta.get('size'), response.meta.get('fit')]
        return '/'.join([rs for rs in raw_size if rs]) or 'One Size'

    def sku_price(self, response):
        raw_sku = json.loads(response.body)
        price = raw_sku['data']['price']['without_tax']['value']
        previous_price = raw_sku['data']['price'].get('rrp_without_tax')
        sku = {
            'currency': self.CURRENCY,
            'price': price,
        }

        if previous_price:
            sku['previous_price'] = previous_price['value']
        return sku

    def request_or_item(self, product):
        requests = product.get('requests')
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            return request

        del product['requests']
        return product

    def product_sku_requests(self, response):
        requests = []
        params = self.fit_params(response) or self.size_params(response) or self.color_params(response)
        url = self.product_sku_url_t.format(pid=self.product_retailer_sku(response))

        for param in params:
            request = FormRequest(url, callback=self.parse_sku, meta=self.product_sku_meta(
                param, response), formdata=param)
            requests.append(request)
        return requests

    def product_sku_meta(self, param, response):
        color_key = self.color_attribute_key(response)
        size_key = self.size_attribute_key(response)
        fit_key = self.fit_attribute_key(response)

        color_values = self.map_color(response)
        size_values = self.map_size(response)
        fit_values = self.map_fit(response)

        return {
            'color': color_values.get(param.get(color_key)),
            'size': size_values.get(param.get(size_key)),
            'fit': fit_values.get(param.get(fit_key)),
        }

    def color_params(self, response):
        color_key = self.color_attribute_key(response)
        color_values = self.map_color(response)
        return [{color_key: color_value} for color_value in color_values]

    def size_params(self, response):
        color_key = self.color_attribute_key(response)
        size_key = self.size_attribute_key(response)

        color_values = self.map_color(response)
        size_values = self.map_size(response)

        if not size_values:
            return None

        return [{color_key: color_value, size_key: size_value, }
                for color_value in color_values for size_value in size_values]

    def fit_params(self, response):
        color_key = self.color_attribute_key(response)
        size_key = self.size_attribute_key(response)
        fit_key = self.fit_attribute_key(response)

        color_values = self.map_color(response)
        size_values = self.map_size(response)
        fit_values = self.map_fit(response)

        if not fit_values:
            return

        return [{color_key: color_value, size_key: size_value, fit_key: fit_value, }
                for color_value in color_values for size_value in size_values for fit_value in fit_values]

    def map_color(self, response):
        color_values = {}
        css = '.form-option-swatch::attr(data-product-attribute-value)'
        color_attribute_values = response.css(css).extract()

        for color_value in color_attribute_values:
            color_value_xpath = f'//label[@data-product-attribute-value={color_value}]//span/@title'
            color_values[str(color_value)] = response.xpath(color_value_xpath).extract_first()

        return color_values

    def map_size(self, response):
        size_values = {}
        size_key = self.size_attribute_key(response)
        if not size_key:
            return size_values

        css = '.product-size .form-option::attr(data-product-attribute-value)'
        size_attribute_values = response.css(css).extract()

        for size_value in size_attribute_values:
            size_value_xpath = f'//label[@data-product-attribute-value={size_value}]//span/text()'
            size_values[str(size_value)] = response.xpath(size_value_xpath).extract_first()

        return size_values

    def map_fit(self, response):
        fit_values = {}
        fit_key = self.fit_attribute_key(response)
        if not fit_key:
            return fit_values

        fit_values_xpath = f'//input[@name="{fit_key}"]/@value'
        fit_attribute_values = response.xpath(fit_values_xpath).extract()

        for fit_value in fit_attribute_values:
            fit_value_xpath = f'//label[@data-product-attribute-value={fit_value}]/span/text()'
            fit_values[str(fit_value)] = response.xpath(fit_value_xpath).extract_first()

        return fit_values

    def color_attribute_key(self, response):
        css = '.form-option-swatch::attr(data-swatch-id)'
        return f"attribute[{response.css(css).extract_first()}]"

    def size_attribute_key(self, response):
        css = '.product-size input::attr(name)'
        return response.css(css).extract_first()

    def fit_attribute_key(self, response):
        xpath = '//div[@class="form-field" and @data-product-attribute="set-rectangle"]/input/@name'
        return response.xpath(xpath).extract_first()

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
        return list(set(response.css(image_url_css).extract()))

    def product_name(self, response):
        name_css = '.productView-title::text'
        return response.css(name_css).extract_first()

    def product_retailer_sku(self, response):
        retailer_sku_css = 'input[name="product_id"]::attr(value)'
        return response.css(retailer_sku_css).extract_first()


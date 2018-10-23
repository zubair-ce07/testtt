# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_products'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/']
    product_attribute_url_t = '/remote/v1/product-attributes/'
    catagory_and_pagination_allow_r = '.com/([a-z-]+$)|(.*page)'
    catagory_css_r = '#primary'
    pagination_css_r = '.pagination-item--next'
    product_css_r = '.card'

    rules = (
        Rule(LinkExtractor(allow=(catagory_and_pagination_allow_r),
                           restrict_css=([catagory_css_r, pagination_css_r])),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=(product_css_r)),
             callback='parse_products'),
    )

    def parse_products(self, response):
        product = {
            'brand': 'woolrich',
            'care': self.product_care(response),
            'category': self.product_catagory(response),
            'description': self.product_description(response),
            'image_url': self.product_image_url(response),
            'name': self.product_name(response),
            'retailer_sku': self.product_retailer_sku(response),
            'skus': {},
            'url': response.url
        }
        meta = self.extract_attributes_with_values(response, product)
        yield self.color_request(response, meta)

    def parse_colors(self, response):
        color_values = response.meta.get('color_values')
        product = response.meta.get('product')
        curr_color = response.meta.get('curr_color_value')
        self.update_skus(response, color_values.get(curr_color))
        del color_values[curr_color]
        response.meta['color_values'] = color_values
        if color_values:
            yield self.color_request(response, response.meta)
        else:
            yield product

    def color_request(self, response, meta):
        color_attribute_key = meta.get('color_attribute_key')
        product = meta.get('product')
        color_values = meta.get('color_values')
        product_id = product['retailer_sku']
        url = self.product_attribute_url_t + f'{product_id}'
        curr_color = list(color_values.keys())[0]
        meta = {
            'product': meta['product'],
            'color_attribute_key': color_attribute_key,
            'color_values': color_values,
            'size_values': meta.get('size_values'),
            'fit_values': meta.get('fit_values'),
            'curr_color_value': curr_color
        }
        param_attribute = f'attribute[{color_attribute_key}]'
        params = {param_attribute: curr_color}
        return scrapy.Request(
            url=response.urljoin(url), callback=self.parse_colors,
            method='Post', body=json.dumps(params), meta=meta
        )

    def extract_attributes_with_values(self, response, product):
        color_attribute_key_css = '.form-option-swatch::attr(data-swatch-id)'
        color_attribute_key = response.css(
            color_attribute_key_css).extract_first()
        color_values = self.color_map(response)
        size_values = self.size_map(response)
        meta = {
            'product': product,
            'color_attribute_key': color_attribute_key,
            'color_values': color_values,
            'size_values': size_values,
        }
        fit_attribute_xpath = '//div[@class="form-field" and @data-product-attribute="set-rectangle"]/input/@name'
        fit_attribute = response.xpath(fit_attribute_xpath).re_first(r'[0-9]+')
        if fit_attribute:
            meta['fit_values'] = self.fit_map(response, fit_attribute)
        return meta

    def update_skus(self, response, color):
        color = color.replace(' ', '-')
        size_values = response.meta.get('size_values')
        fit_values = response.meta.get('fit_values')
        resp_dict = json.loads(response.body)
        if not size_values:
            self.update_without_size(response, color, resp_dict)
        elif not fit_values:
            self.update_without_fit(response, color, resp_dict, size_values)
        else:
            self.update_with_size_and_fit(
                response, color, resp_dict, size_values, fit_values)

    def update_without_size(self, response, color, resp_dict):
        sku_key = color
        response.meta['product']['skus'][sku_key] = {
            'color': color.replace('-', ' '),
            'currency': 'USD',
            'price': resp_dict['data']['price']['without_tax']['value'],
        }

    def update_without_fit(self, response, color, resp_dict, size_values):
        in_stock_attributes = resp_dict['data'].get('in_stock_attributes')
        for size_value in size_values:
            size = size_values.get(size_value)
            sku_key = color + '_' + size
            response.meta['product']['skus'][sku_key] = {
                'color': color.replace('-', ' '),
                'currency': 'USD',
                'price': resp_dict['data']['price']['without_tax']['value'],
                'size': size,
            }
            if int(size_value) in in_stock_attributes:
                response.meta['product']['skus'][sku_key]['in_stock'] = True
            else:
                response.meta['product']['skus'][sku_key]['in_stock'] = False

    def update_with_size_and_fit(self, response, color,
                                 resp_dict, size_values, fit_values):
        in_stock_attributes = resp_dict['data'].get('in_stock_attributes')
        for size_value in size_values:
            size = size_values.get(size_value)
            for fit_value in fit_values:
                fit = fit_values.get(fit_value)
                sku_key = color + '_' + size + '_' + fit
                response.meta['product']['skus'][sku_key] = {
                    'color': color.replace('-', ' '),
                    'fit': fit,
                    'currency': 'USD',
                    'price': resp_dict['data']['price']['without_tax']['value'],
                    'size': size,
                }
                if int(size_value) in in_stock_attributes and \
                        int(fit_value) in in_stock_attributes:
                    response.meta['product']['skus'][sku_key]['in_stock'] = True
                else:
                    response.meta['product']['skus'][sku_key]['in_stock'] = False

    def color_map(self, response):
        css = '.form-option-swatch::attr(data-product-attribute-value)'
        color_attribute_values = response.css(css).extract()
        color_attributes = {}
        for color_value in color_attribute_values:
            color_value_xpath = f'//label[@data-product-attribute-value={color_value}]//span/@title'
            color_attributes[str(color_value)] = response.xpath(
                color_value_xpath).extract_first()
        return color_attributes

    def size_map(self, response):
        css = '.product-size .form-option::attr(data-product-attribute-value)'
        size_attribute_values = response.css(css).extract()
        size_attributes = {}
        for size_value in size_attribute_values:
            size_value_xpath = f'//label[@data-product-attribute-value={size_value}]//span/text()'
            size_attributes[str(size_value)] = response.xpath(
                size_value_xpath).extract_first()
        return size_attributes

    def fit_map(self, response, fit_attribute):
        fit_attribute_key = f'attribute[{str(fit_attribute)}]'
        fit_values_xpath = f'//input[@name={fit_attribute_key}]/@value'
        fit_attribute_values = response.xpath(fit_values_xpath).extract()
        fit_attributes = {}
        for fit_value in fit_attribute_values:
            fit_value_xpath = f'//label[@data-product-attribute-value={fit_value}]/span/text()'
            fit_attributes[str(fit_value)] = response.xpath(
                fit_value_xpath).extract_first()
        return fit_attributes

    def product_care(self, response):
        care_css = '#features-content > li::text'
        return response.css(care_css).extract()

    def product_description(self, response):
        description_css = '#details-content::text'
        return response.css(description_css).extract_first()

    def product_catagory(self, response):
        category_css = '.breadcrumb > a::text'
        return response.css(category_css)[-1].extract()

    def product_image_url(self, response):
        image_url_css = '.productView-image img::attr(src)'
        return response.css(image_url_css).extract()

    def product_name(self, response):
        name_css = '.productView-title::text'
        return response.css(name_css).extract_first()

    def product_retailer_sku(self, response):
        retailer_sku_css = 'input[name="product_id"]::attr(value)'
        return response.css(retailer_sku_css).extract_first()


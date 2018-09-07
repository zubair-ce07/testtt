"""
This module scrapes required information about different products from woolrich website
"""
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Tasks.items import TasksItem


class QuotesSpider(CrawlSpider):

    storage = {}
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com']
    navigation = ['#primary ul li']
    product = ['.card-title']
    allows = ('/men','/women', '/parkas', '/flannels', '/blankets')
    rules = (

        Rule(LinkExtractor(restrict_css=navigation,allow=allows)),
        Rule(LinkExtractor(restrict_css=product), callback='parse_products'),

    )
    item = TasksItem()

    def parse_products(self, response):
        product_id = response.css('input[name=product_id]::attr(value)').extract_first()
        api_url = 'https://www.woolrich.com/remote/v1/product-attributes/{product_id}'
        color_key = response.css('.form-field:nth-child(1) label.form-option-swatch '
                                 'input.form-radio::attr(name)').extract_first()
        color_values = response.css('.form-field:nth-child(1) '
                                    'label.form-option-swatch '
                                    'input.form-radio::attr(value)').extract()
        fit_key = response.css('.form-field:nth-child(3) input.form-radio'
                               '::attr(name)').extract_first()
        fit_values = response.css('.form-field:nth-child(3) '
                                  'input.form-radio::attr(value)').extract()
        size_key = response.css('.form-field:nth-child(2) '
                                'input.form-radio::attr(name)').extract_first()
        size_values = response.css('.form-field:nth-child(2) '
                                   'input.form-radio::attr(value)').extract()
        size_names = response.css('.form-field:nth-child(2) '
                                  'span.form-option-variant::text').extract()
        color_names = response.css('.form-field:nth-child(1) label.form-option '
                                   'span.form-option-variant:nth-child(2)::attr(title)').extract()
        fit_names = response.css('.form-field:nth-child(3) '
                                 'label.form-option span.form-option-variant::text').extract()
        self.item['product_name'] = response.css('.productView-title::text').extract_first()
        self.item['product_style'] = response.css('.productView-product div '
                                                  'strong::text').extract_first()
        self.item['breadcrumb_trail'] = '/'.join(response.css('.breadcrumb-label::text').extract())
        self.item['product_description'] = response.css('#details-content::text').extract_first()
        self.item['product_care'] = response.css('.half li::text').extract()
        self.item['brand'] = response.css('.header-logo-image::attr(title)').extract_first()
        self.item['product_url'] = response.url
        self.item['product_currency'] = response.css('meta[property="product:price:currency"]'
                                              '::attr(content)').extract_first()
        self.item['image_url'] = response.css('img[data-sizes="auto"]::attr(src)').extract()
        if fit_values:
            return self.parse_three_attributes_request(color_values, fit_values, size_values, product_id, color_key,
                                                size_key, fit_key, size_names, color_names, fit_names, api_url)
        elif size_values:
            return self.parse_two_attributes_request(color_values, size_values, product_id, color_key,
                                              size_key, size_names, color_names, api_url)
        else:
            return self.parse_single_attribute_request(color_values, product_id, color_key, color_names, api_url)


    def parse_price(self, response):
        fit_name = response.meta['fit_name']
        result = response.meta['result']
        size_name = response.meta['size_name']
        color_name = response.meta['color_name']
        data = json.loads(response.text)
        price = data['data']['price']['without_tax']['formatted']
        if fit_name is not 'None':
            self.storage.setdefault('color', {}).setdefault(color_name, {}).setdefault('fit', {}).\
            setdefault(fit_name, {}).setdefault('size', {})[size_name] = price
            if result:
                self.item['product_price'] = self.storage
                yield self.item
                self.storage.clear()
        elif size_name is not 'None':
            self.storage.setdefault('color', {}).setdefault(color_name, {}).\
            setdefault('size', {})[size_name] = price
            if result:
                self.item['product_price'] = self.storage
                yield self.item
                self.storage.clear()
        else:
            self.storage.setdefault('color', {}).setdefault(color_name, {})[size_name] = price
            if result:
                self.item['product_price'] = self.storage
                yield self.item
                self.storage.clear()


    def parse_three_attributes_request(self, color_values, fit_values, size_values, product_id, color_key,
                                       size_key, fit_key, size_names, color_names, fit_names, api_url):
        """
        This method executes when there are three attributes (i.e. color, siza and fit)
        in request that is to be sent to API for price extraction
        :param color_values:
        :param fit_values:
        :param size_values:
        :param product_id:
        :param color_key:
        :param size_key:
        :param fit_key:
        :param size_names:
        :param color_names:
        :param fit_names:
        :param api_url:
        :return:
        """
        for color_index, color_value in enumerate(color_values):
            for fit_index, fit_value in enumerate(fit_values):
                for size_index, size_value in enumerate(size_values):
                    form_data = {
                        'action': 'add',
                        'product_id': product_id,
                        color_key: color_value,
                        size_key: size_value,
                        fit_key: fit_value,
                        'qty[]': '1'
                    }
                    size_name = size_names[size_index]
                    color_name = color_names[color_index]
                    fit_name = fit_names[fit_index]
                    result = False
                    if color_index == len(color_names) - 1 and fit_index == len(fit_names) - 1 and \
                            size_index == len(size_names) - 1:
                        result = True
                    yield scrapy.Request(url=api_url.format(product_id=product_id),
                                         method='POST',
                                         headers={'Content-Type': 'application/json'},
                                         body=json.dumps(form_data),
                                         meta={'size_name': size_name, 'color_name': color_name,
                                               'fit_name': fit_name, 'result': result},
                                         callback=self.parse_price)


    def parse_two_attributes_request(self, color_values, size_values, product_id, color_key,
                                     size_key, size_names, color_names, api_url):
        for color_index, color_value in enumerate(color_values):
            for size_index, size_value in enumerate(size_values):
                form_data = {
                    'action': 'add',
                    'product_id': product_id,
                    color_key: color_value,
                    size_key: size_value,
                    'qty[]': '1'
                }
                size_name = size_names[size_index]
                color_name = color_names[color_index]
                result = False
                if color_index == len(color_names) - 1 and size_index == len(size_names) - 1:
                    result = True
                yield scrapy.Request(url=api_url.format(product_id=product_id), method='POST',
                                     headers={'Content-Type': 'application/json'},
                                     body=json.dumps(form_data),
                                     meta={'size_name': size_name, 'color_name': color_name,
                                           'result': result, 'fit_name': 'None'},
                                     callback=self.parse_price)


    def parse_single_attribute_request(self, color_values, product_id, color_key, color_names, api_url):
        for color_index, color_value in enumerate(color_values):
                form_data = {
                    'action': 'add',
                    'product_id': product_id,
                    color_key: color_value,
                    'qty[]': '1'
                }
                color_name = color_names[color_index]
                result = False
                if color_index == len(color_names) - 1:
                    result = True
                yield scrapy.Request(url=api_url.format(product_id=product_id), method='POST',
                                     headers={'Content-Type': 'application/json'},
                                     body=json.dumps(form_data),
                                     meta={'size_name': 'None', 'color_name': color_name,
                                           'result': result, 'fit_name': 'None'},
                                     callback=self.parse_price)


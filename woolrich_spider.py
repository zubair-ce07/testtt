"""
This module scrapes required information from woolrich website
"""
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Tasks.items import TasksItem


class QuotesSpider(CrawlSpider):
    """
    This class scrapes required information from woolrich website
    """
    storage = {}
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com']
    navigation = ['nav#primary + ul']
    allows = ('/men', '/women')
    rules = (
        Rule(LinkExtractor(restrict_css=navigation)),
        Rule(LinkExtractor(allow=allows), callback='parse_url'),
    )
    item = TasksItem()

    def parse_url(self, response):
        """
        This method captures all the urls and traverses them at a time
        :param response:
        :return:
        """
        for url in response.css('h4.card-title a::attr(href)').extract():
            yield scrapy.Request(url=url, callback=self.parse_details)


    def parse_details(self, response):
        """
        This method extracts all the key information needed to scrap the required data
        :param response:
        :return:
        """
        product_id = response.css('input[name=product_id]::attr(value)').extract_first()
        api_url = 'https://www.woolrich.com/remote/v1/product-attributes/{product_id}'
        color_key = response.css('div div.form-field:nth-child(1) label.form-option-swatch '
                                 'input.form-radio::attr(name)').extract_first()
        color_values = response.css('div div.form-field:nth-child(1) '
                                    'label.form-option-swatch '
                                    'input.form-radio::attr(value)').extract()
        fit_key = response.css('div div.form-field:nth-child(3) input.form-radio'
                               '::attr(name)').extract_first()
        fit_values = response.css('div div.form-field:nth-child(3) '
                                  'input.form-radio::attr(value)').extract()
        size_key = response.css('div div.form-field:nth-child(2) '
                                'input.form-radio::attr(name)').extract_first()
        size_values = response.css('div div.form-field:nth-child(2) '
                                   'input.form-radio::attr(value)').extract()
        size_names = response.css('div div.form-field:nth-child(2) '
                                  'span.form-option-variant::text').extract()
        color_names = response.css('div div.form-field:nth-child(1) label.form-option '
                                   'span.form-option-variant:nth-child(2)::attr(title)').extract()
        fit_names = response.css('div div.form-field:nth-child(3) '
                                 'label.form-option span.form-option-variant::text').extract()
        self.item['product_name'] = response.css('h1.productView-title::text').extract_first()
        self.item['product_style'] = response.css('div.productView-product div '
                                                  'strong::text').extract_first()
        if fit_values:
            for color_index, color_value in enumerate(color_values):
                for fit_index, fit_value in enumerate(fit_values):
                    for size_index, size_value in enumerate(size_values):
                        form_data = {
                            'action':'add',
                            'product_id':product_id,
                            color_key:color_value,
                            size_key:size_value,
                            fit_key:fit_value,
                            'qty[]':'1'
                        }
                        size_name = size_names[size_index]
                        color_name = color_names[color_index]
                        fit_name = fit_names[fit_index]
                        result = False
                        if color_index == len(color_names)-1 and fit_index == len(fit_names)-1 and\
                                size_index == len(size_names)-1:
                            result = True
                        yield scrapy.Request(url=api_url.format(product_id=product_id),
                                             method='POST',
                                             headers={'Content-Type': 'application/json'},
                                             body=json.dumps(form_data),
                                             meta={'size_name': size_name, 'color_name': color_name,
                                                   'fit_name':fit_name, 'result':result},
                                             callback=self.parse_accept_request)
        else:
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
                    if color_index == len(color_names)-1 and size_index == len(size_names)-1:
                        result = True
                    yield scrapy.Request(url=api_url.format(product_id=product_id), method='POST',
                                         headers={'Content-Type': 'application/json'},
                                         body=json.dumps(form_data),
                                         meta={'size_name': size_name, 'color_name': color_name,
                                               'result': result, 'fit_name':'None'},
                                         callback=self.parse_accept_request)

    def parse_accept_request(self, response):
        """
        This method calls API for each iteration and extracts price from it
        :param response:
        :return:
        """
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
        else:
            self.storage.setdefault('color', {}).setdefault(color_name, {}).\
            setdefault('size', {})[size_name] = price
            if result:
                self.item['product_price'] = self.storage
                yield self.item


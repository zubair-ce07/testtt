# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_products'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/']

    rules = (
        Rule(LinkExtractor(deny=('.php$'), restrict_css=(
            ['#primary > ul > li > a', '.pagination-item--next > a']))),
        Rule(LinkExtractor(restrict_css=('#product-listing-container .card')),
             callback='parse_products'),
    )

    def parse_products(self, response):
        product = {
            'brand': 'woolrich',
            'care': response.css('#features-content > li::text').extract(),
            'category': response.css('.breadcrumb > a::text')[-1].extract(),
            'description': response.css('#details-content::text').extract_first(),
            'name': response.css('.productView-title::text').extract_first(),
            'retailer_sku': response.css('input[name="product_id"]::attr(value)').extract_first(),
            'skus': {},
            'url': response.url
        }
        response.meta['product'] = product
        my_meta = self.extract_attributes_and_values(response)
        url = '/remote/v1/product-attributes/'
        url += response.meta.get('product').get('retailer_sku')
        params = {
            'attribute['+str(my_meta['color_attribute'])+']': list(my_meta['color_values'].keys())[0]
        }
        my_meta['curr_color_value'] = list(my_meta['color_values'].keys())[0]
        yield scrapy.Request(
            url=response.urljoin(url),
            callback=self.parse_colors,
            method='Post',
            body=json.dumps(params),
            meta=my_meta
        )

    def extract_attributes_and_values(self, response):
        color_attribute = response.css(
            '.form-option-swatch::attr(data-swatch-id)').extract_first()
        color_values = self.find_color_values_and_names(response)
        size_values = self.find_size_values_and_names(response)
        my_meta = {
            'product': response.meta['product'],
            'color_attribute': color_attribute,
            'color_values': color_values,
            'size_values': size_values,
        }
        fit_attribute = response.xpath(
            '//div[@class="form-field" and @data-product-attribute="set-rectangle"]/input/@name'
        ).re_first(r'[0-9]+')
        if fit_attribute is not None:
            fit_values = self.find_fit_values_and_names(
                response, fit_attribute)
            my_meta['fit_values'] = fit_values
        return my_meta

    def parse_colors(self, response):
        color_attribute = response.meta.get('color_attribute')
        color_values = response.meta.get('color_values')
        size_values = response.meta.get('size_values')
        fit_values = response.meta.get('fit_values')
        product = response.meta.get('product')
        curr_color = response.meta.get('curr_color_value')
        self.update_skus(response, color_values.get(curr_color))
        del color_values[curr_color]
        if len(color_values) > 0:
            url = '/remote/v1/product-attributes/'
            url += response.meta.get('product').get('retailer_sku')
            my_meta = {
                'product': response.meta['product'],
                'color_attribute': color_attribute,
                'color_values': color_values,
                'size_values': size_values,
                'fit_values': fit_values,
            }
            curr_color = list(color_values.keys())[0]
            params = {
                'attribute['+str(color_attribute)+']': curr_color}
            my_meta['curr_color_value'] = curr_color
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_colors,
                method='Post',
                body=json.dumps(params),
                meta=my_meta,
                dont_filter=True
            )
        else:
            yield product

    def update_skus(self, response, color):
        color = color.replace(' ', '-')
        size_values = response.meta.get('size_values')
        fit_values = response.meta.get('fit_values')
        resp_dict = json.loads(response.body)
        if size_values is None:
            self.update_without_size(response, color, resp_dict)
        elif fit_values is None:
            self.update_without_fit(response, color, resp_dict, size_values)
        else:
            self.update_with_size_and_fit(
                response, color, resp_dict, size_values, fit_values)

    def update_without_size(self, response, color, resp_dict):
        response.meta['product']['skus'][color] = {
            'color': color.replace('-', ' '),
            'currency': 'USD',
            'price': resp_dict['data']['price']['without_tax']['value'],
        }

    def update_without_fit(self, response, color, resp_dict, size_values):
        in_stock_attributes = resp_dict['data'].get('in_stock_attributes')
        for size_value in size_values:
            size = size_values.get(size_value)
            response.meta['product']['skus'][color+'_'+size] = {
                'color': color.replace('-', ' '),
                'currency': 'USD',
                'price': resp_dict['data']['price']['without_tax']['value'],
                'size': size,
            }
            if int(size_value) in in_stock_attributes:
                response.meta['product']['skus'][color +
                                                 '_'+size]['in_stock'] = True
            else:
                response.meta['product']['skus'][color +
                                                 '_'+size]['in_stock'] = False

    def update_with_size_and_fit(self, response, color,
                                 resp_dict, size_values, fit_values):
        in_stock_attributes = resp_dict['data'].get('in_stock_attributes')
        for size_value in size_values:
            size = size_values.get(size_value)
            for fit_value in fit_values:
                fit = fit_values.get(fit_value)
                response.meta['product']['skus'][color+'_'+size+'_'+fit] = {
                    'color': color.replace('-', ' '),
                    'fit': fit,
                    'currency': 'USD',
                    'price': resp_dict['data']['price']['without_tax']['value'],
                    'size': size,
                }
                if int(size_value) in in_stock_attributes and \
                        int(fit_value) in in_stock_attributes:
                    response.meta['product']['skus'][color +
                                                     '_'+size+'_'+fit]['in_stock'] = True
                else:
                    response.meta['product']['skus'][color +
                                                     '_'+size+'_'+fit]['in_stock'] = False

    def find_color_values_and_names(self, response):
        color_attribute_values = response.css(
            '.form-option-swatch::attr(data-product-attribute-value)').extract()
        color_attributes = dict()
        for color_value in color_attribute_values:
            color_attributes[str(color_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]//span/@title',
                val=color_value).extract_first()
        return color_attributes

    def find_size_values_and_names(self, response):
        size_attribute_values = response.css(
            '.product-size .form-option::attr(data-product-attribute-value)').extract()
        size_attributes = {}
        for size_value in size_attribute_values:
            size_attributes[str(size_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]//span/text()',
                val=size_value).extract_first()
        return size_attributes

    def find_fit_values_and_names(self, response, fit_attribute):
        fit_attribute_values = response.xpath(
            '//input[@name=$val]/@value', val='attribute['+str(fit_attribute)+']'
        ).extract()
        fit_attributes = {}
        for fit_value in fit_attribute_values:
            fit_attributes[str(fit_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]/span/text()', val=fit_value).extract_first()
        return fit_attributes


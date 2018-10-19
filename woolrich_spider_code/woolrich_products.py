# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from string import Template


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_products'
    product_attribute_url_t = Template('/remote/v1/product-attributes/$sku_id')
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/']

    rules = (
        Rule(LinkExtractor(allow=('.com/([a-z-]+$)|(.*page)'),
                           restrict_css=(['#primary', '.pagination-item--next']))),
        Rule(LinkExtractor(restrict_css=('.card')), callback='parse_products'),
    )

    def parse_products(self, response):
        care_css = '#features-content > li::text'
        category_css = '.breadcrumb > a::text'
        description_css = '#details-content::text'
        image_url_css = '.productView-image img::attr(src)'
        name_css = '.productView-title::text'
        retailer_sku_css = 'input[name="product_id"]::attr(value)'
        product = {
            'brand': 'woolrich',
            'care': response.css(care_css).extract(),
            'category': response.css(category_css)[-1].extract(),
            'description': response.css(description_css).extract_first(),
            'image_url': response.css(image_url_css).extract(),
            'name': response.css(name_css).extract_first(),
            'retailer_sku': response.css(retailer_sku_css).extract_first(),
            'skus': {},
            'url': response.url
        }
        response.meta['product'] = product
        meta = self.extract_attributes_with_values(response)
        url = self.product_attribute_url_t.substitute(
            sku_id=product['retailer_sku'])
        params = {
            'attribute['+str(meta['color_attribute'])+']': list(meta['color_values'].keys())[0]
        }
        meta['curr_color_value'] = list(meta['color_values'].keys())[0]
        yield scrapy.Request(
            url=response.urljoin(url),
            callback=self.parse_colors,
            method='Post',
            body=json.dumps(params),
            meta=meta
        )

    def extract_attributes_with_values(self, response):
        color_attribute_css = '.form-option-swatch::attr(data-swatch-id)'
        color_attribute = response.css(color_attribute_css).extract_first()
        color_values = self.color_map(response)
        size_values = self.size_map(response)
        meta = {
            'product': response.meta['product'],
            'color_attribute': color_attribute,
            'color_values': color_values,
            'size_values': size_values,
        }
        fit_attribute_xpath = '//div[@class="form-field" and @data-product-attribute="set-rectangle"]/input/@name'
        fit_attribute = response.xpath(fit_attribute_xpath).re_first(r'[0-9]+')
        if fit_attribute:
            meta['fit_values'] = self.fit_map(response, fit_attribute)
        return meta

    def parse_colors(self, response):
        color_attribute = response.meta.get('color_attribute')
        color_values = response.meta.get('color_values')
        size_values = response.meta.get('size_values')
        fit_values = response.meta.get('fit_values')
        product = response.meta.get('product')
        curr_color = response.meta.get('curr_color_value')
        self.update_skus(response, color_values.get(curr_color))
        del color_values[curr_color]
        if color_values:
            url = self.product_attribute_url_t.substitute(
                sku_id=product['retailer_sku'])
            meta = {
                'product': response.meta['product'],
                'color_attribute': color_attribute,
                'color_values': color_values,
                'size_values': size_values,
                'fit_values': fit_values,
            }
            curr_color = list(color_values.keys())[0]
            params = {
                'attribute['+str(color_attribute)+']': curr_color}
            meta['curr_color_value'] = curr_color
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_colors,
                method='Post',
                body=json.dumps(params),
                meta=meta,
                dont_filter=True
            )
        else:
            yield product

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
        color_attribute_values_css = '.form-option-swatch::attr(data-product-attribute-value)'
        color_attribute_values = response.css(
            color_attribute_values_css).extract()
        color_attributes = dict()
        for color_value in color_attribute_values:
            color_attributes[str(color_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]//span/@title',
                val=color_value).extract_first()
        return color_attributes

    def size_map(self, response):
        size_attribute_values_css = '.product-size .form-option::attr(data-product-attribute-value)'
        size_attribute_values = response.css(
            size_attribute_values_css).extract()
        size_attributes = {}
        for size_value in size_attribute_values:
            size_attributes[str(size_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]//span/text()',
                val=size_value).extract_first()
        return size_attributes

    def fit_map(self, response, fit_attribute):
        fit_attribute_values = response.xpath(
            '//input[@name=$val]/@value', val='attribute['+str(fit_attribute)+']'
        ).extract()
        fit_attributes = {}
        for fit_value in fit_attribute_values:
            fit_attributes[str(fit_value)] = response.xpath(
                '//label[@data-product-attribute-value=$val]/span/text()', val=fit_value).extract_first()
        return fit_attributes

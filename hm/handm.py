# -*- coding: utf-8 -*-
import json
import urllib.parse as urlparse
from copy import deepcopy

from scrapy import Request, FormRequest, Spider, Selector

from hnm.spiders.products import *


class HandmSpider(Spider):
    name = 'handm'

    def start_requests(self):
        start_url = 'https://kw.hm.com/en/'
        yield Request(
            url=start_url,
            callback=self.parse
        )

    def parse(self, response):
        for level1 in response.css('.menu--one__list-item'):
            label1 = level1.css('div a::text').extract_first()
            url1 = level1.css('div a::attr(href)').extract_first()

            yield Request(
                url=response.urljoin(url1),
                callback=self.parse_pagination,
                meta={
                    'categories': [label1]
                }
            )

            for level2 in level1.css('.menu--two__list-item'):
                label2 = level2.css('div a::text').extract_first()
                url2 = level2.css('div a::attr(href)').extract_first()

                yield Request(
                    url=response.urljoin(url2),
                    callback=self.parse_pagination,
                    meta={
                        'categories': [label1, label2]
                    }
                )

                for level3 in level2.css('.menu--three__list-item'):
                    label3 = level3.css('div a::text').extract_first()
                    url3 = level3.css('div a::attr(href)').extract_first()

                    yield Request(
                        url=response.urljoin(url3),
                        callback=self.parse_pagination,
                        meta={
                            'categories': [label1, label2, label3]
                        }
                    )

    def parse_pagination(self, response):
        next_url = response.css('.pager__item a::attr(href)').extract_first()
        if next_url:
            yield Request(
                url=response.urljoin(next_url),
                callback=self.parse_pagination,
                meta=response.meta
            )

        for item_url in response.css('.c-products__item h2>a::attr(href)').extract():
            yield Request(
                url=response.urljoin(item_url),
                callback=self.parse_item,
                meta=response.meta
            )

    def parse_item(self, response):
        item = Product()
        data = response.css('.content__title_wrapper')

        item['url'] = response.url
        item['category'] = response.meta['categories']
        item['brand'] = 'H&M'
        item['skus'] = {}

        item['name'] = data.css('h1 span::text').extract_first()
        item['base_sku'] = data.css('.content--item-code::text').extract()[1].strip()

        detail_data = response.css('.short-description-wrapper')
        item['description'] = detail_data.css('.desc-value::text').extract()
        item['description'] = [' '.join(item['description']).strip()]
        item['description'] += detail_data.css('.composition-value li::text').extract()
        item['description'] += detail_data.css('.washing-instructions::text').extract()

        data_skuid = \
            response.css('.basic-details-wrapper .field--name-field-skus article::attr(data-skuid)').extract_first()
        params = {
            'js': 'true',
            '_drupal_ajax': '1'
        }
        color_url = response.urljoin('get-cart-form/full/{}?'
                                     '_wrapper_format=drupal_ajax'
                                     .format(data_skuid))
        yield FormRequest(
            url=color_url,
            formdata=params,
            callback=self.parse_color_requests,
            meta={
                'item': item,
                'data_skuid': data_skuid
            }
        )

    def parse_color_requests(self, response):
        response_data = json.loads(response.css('textarea::text').extract_first())
        data_skuid = response.meta['data_skuid']
        params = {
            'sku_id': data_skuid,
            '_triggering_element_name': 'configurables[article_castor_id]',
            'form_id': 'acq_sku_configurable_{}__sku_base_form'.format(data_skuid)
        }
        for data in response_data:
            temp = str(data)
            if 'out-of-stock' in temp:
                return
            elif 'sku_configurable_options_color' in temp:
                for key, value in data['settings']['sku_configurable_options_color'].items():
                    params.update({
                        'configurables[article_castor_id]': key
                    })
                    yield FormRequest(
                        url=response.urljoin('/get-cart-form/full/{}?'
                                             '_wrapper_format=drupal_ajax'
                                             '&ajax_form=1'
                                             '&_wrapper_format=drupal_ajax'
                                             .format(data_skuid)),
                        formdata=params,
                        callback=self.parse_color_item,
                        meta={
                            'item': deepcopy(response.meta['item']),
                            'color_name': value['display_label'],
                            'color_id': key
                        }
                    )

    def parse_color_item(self, response):
        item = response.meta['item']
        response_data = json.loads(response.css('textarea::text').extract_first())
        data_found = False
        for option in response_data:
            if 'configurable-wrapper' in str(option):
                data = Selector(text=option['args'][0]['replaceWith'])
                data_found = True
        if not data_found:
            return
        item['image_urls'] = data.css('.mobilegallery ul li img::attr(src)').extract()
        item['color_name'] = response.meta['color_name']

        size_data = []
        for size_option in data.css('.form-item-configurable-select option'):
            size_id = size_option.css('::attr(value)').extract_first()
            if not size_id:
                continue
            size_name = size_option.css('::text').extract_first()
            size_stock = False if size_option.css('[disabled]').extract_first() else True
            size_data.append((size_id, size_name, size_stock))

        size_id, size_name, size_stock = size_data.pop()
        params = self.make_formdata(size_id, response.request.body)
        yield FormRequest(
            url=response.request.url,
            formdata=params,
            callback=self.parse_size,
            meta={
                'item': item,
                'size_data': size_data,
                'size_name': size_name,
                'size_stock': size_stock,
                'color_id': response.meta['color_id']
            }
        )

    def parse_size(self, response):
        response_data = json.loads(response.css('textarea::text').extract_first())
        data = [temp['data'] for temp in response_data if 'price-block' in temp.get('selector', '')]
        data = Selector(text=data[0])

        item = response.meta['item']
        size_item = Size_Item()
        size_item['size_name'] = response.meta['size_name']
        size_item['in_stock'] = response.meta['size_stock']

        if data.css('.special--price'):
            size_item['full_price'] = data.css('.has--special--price .price-amount::text').extract_first()
            size_item['sale_price'] = data.css('.special--price .price-amount::text').extract_first()
        else:
            size_item['full_price'] = data.css('.price-amount::text').extract_first()
            size_item['sale_price'] = data.css('.price-amount::text').extract_first()

        item['skus'].update({
            '{}_{}'.format(response.meta['color_id'], size_item['size_name']): size_item
        })

        size_data = response.meta['size_data']
        if size_data:
            size_id, size_name, size_stock = size_data.pop()
            params = self.make_formdata(size_id, response.request.body)
            yield FormRequest(
                url=response.request.url,
                formdata=params,
                callback=self.parse_size,
                meta={
                    'item': item,
                    'size_data': size_data,
                    'size_name': size_name,
                    'size_stock': size_stock,
                    'color_id': response.meta['color_id']
                }
            )
        else:
            yield item

    @staticmethod
    def make_formdata(size_id, params):
        formdata = dict(urlparse.parse_qsl(params))
        formdata.update({
            '_triggering_element_name': 'configurables[size]',
            'configurables[size]': size_id
        })
        return formdata

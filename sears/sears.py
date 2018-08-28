# -*- coding: utf-8 -*-
import json
import re
import urllib.parse as urlparse
from copy import deepcopy
from urllib.parse import urlencode

from scrapy import Spider, Request

from items import *


class SearsSpider(Spider):
    name = 'sears'
    blacklist = [
        'shoes',
        'jewelry',
        'beauty & fragrance',
        'accessories & bags',
        'sports fan shop',
        "women's plus",
        "women's petite",
        'workwear',
        "men's big & tall"
    ]

    def start_requests(self):
        header = {
            'Host': 'www.sears.com',
            'User-Agent': 'Mozilla / 5.0(X11; Ubuntu; Linux x86_64; rv: 61.0) Gecko / 20100101 Firefox / 61.0'
        }
        start_url = 'http://www.sears.com/en_us.html'
        yield Request(
            url=start_url,
            callback=self.parse,
            headers=header,
            meta={
                'language_code': 'en',
                'currency': 'USD',
                'country_code': 'US'
            }
        )

    def parse(self, response):
        url = 'https://chrono.shld.net/segments/sears-us-hdrv3-flyouts.html?v=222'
        yield Request(
            url=url,
            callback=self.parse_category,
            meta=response.meta
        )

    def parse_category(self, response):
        data = response.css('#gnf_dept_tree_item_4>ul>li')
        label1 = 'clothing'
        for level1 in data:
            for level2 in level1.css('ul>li'):
                if level2.css('span[class="heading"]'):
                    label2 = level2.css('span>a::text').extract_first()
                elif level2.css('span[class]'):  # span having class other than heading is not a level 2 menu item
                    continue
                elif level2.css('span>a>img'):  # a conting image is also not a level 2 menu item
                    continue
                else:
                    if label2:
                        if label2.lower() in self.blacklist:
                            continue
                    label3 = level2.css('span>a::text').extract_first()
                    url3 = level2.css('span>a::attr(href)').extract_first()

                    if url3:
                        category_code = re.findall('b-(\d{7})', url3)
                        url = ('https://www.sears.com/browse/services/v1/hierarchy/fetch-paths-by-id/'
                               '{}?clientId=obusearch&site=sears').format(category_code[0])

                        meta = response.meta
                        meta.update({
                            'categories': [label1, label2, label3],
                            'home': '1'
                        })
                        yield Request(
                            url=url,
                            callback=self.handle_pagintation,
                            meta=meta,
                            headers={'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='}
                        )

    def handle_pagintation(self, response):  # in between request to get the required data for the pagination request
        category_data = json.loads(response.text)
        if category_data.get('status') == '400':
            return

        for cat_path in category_data['data'][0]['catgroups']:
            if cat_path.get('isPrimary'):
                category_path = cat_path['namePath'].replace(' ', '+')

                return Request(
                    url=('https://www.sears.com/service/search/v2/productSearch?'
                         'catalogId=12605&levels={}').format(category_path),
                    callback=self.parse_pagination,
                    meta=response.meta,
                    headers={'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='}
                )

    def parse_pagination(self, response):
        data = json.loads(response.text)
        data = data['data']
        # check for first category pge request to handle pagination
        if response.meta.get('home'):
            response.meta.pop('home')
            for page in data['pagination']:
                value = page['value'].split('?')[-1]
                next_url = response.url + value

                yield Request(
                    url=next_url,
                    callback=self.parse_pagination,
                    meta=response.meta
                )

        # handle all items on the page
        url = 'https://www.sears.com/content/pdp/config/products/v1/products/{}?site=sears'
        meta = response.meta
        for product in data['products']:
            mini_item = ProductItem()

            mini_item['title'] = product['name']
            mini_item['base_sku'] = product['sin']
            mini_item['category_names'] = response.meta['categories']
            mini_item['brand'] = product.get('brandName', 'sears')
            mini_item['url'] = 'http://www.sears.com' + product['url']
            mini_item['referer_url'] = response.url
            mini_item['language_code'] = response.meta['language_code']
            mini_item['currency'] = response.meta['currency']
            mini_item['country_code'] = response.meta['country_code']

            yield mini_item

            meta.update({
                'item': mini_item
            })
            yield Request(
                url=url.format(product['sin']),
                callback=self.parse_item,
                meta=meta
            )

    def parse_item(self, response):
        data = json.loads(response.text)
        product_data = data['data']['product']
        item = response.meta['item']

        item['description_text'] = [desc['val'] for desc in product_data['desc']]
        item['use_size_level_prices'] = True

        if data['data'].get('attributes'):
            yield from self.parse_colors(item, data['data']['attributes'])
        else:
            yield from self.parse_special_item(item,  product_data)

    def parse_special_item(self, item, data):  # item has no color or size variants to handle
        item['color_name'] = 'no_color'
        item['image_urls'] = [vals['src']
                              for img in data['assets']['imgs']
                              for vals in img['vals']]
        yield Request(
            url=self.make_size_url({
                'ssin': item['base_sku']
            }),
            callback=self.parse_size,
            meta={
                'item': item,
                'size_name': 'no_size',
                'size_urls': []
            },
            headers={
                'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='
            }
        )

    def parse_colors(self, item, data):
        # check for color variants and make items for each
        color_data = [c_data['values']
                      for c_data in data['attributes']
                      if c_data['name'].lower() == 'color']
        all_color_names = []
        color_items = {}
        if not color_data:
            color_items.update({
                'no_color': item
            })
            all_color_names.append('no_color')
            item['identifier'] = item['base_sku']
        else:
            for color in color_data[0]:
                c_item = deepcopy(item)
                c_item['identifier'] = '{}({})'.format(item['base_sku'], color['name'])
                c_item['color_name'] = color['name']
                all_color_names.append(color['name'])
                image_data = color.get('primaryImage')
                c_item['image_urls'] = [image_data['src']] if image_data else []
                color_items.update({color['name']: c_item})

        # get all size variants to handle
        all_size_urls = {name: [] for name in all_color_names}
        all_size_urls = self.parse_size_url(data, color_items, all_size_urls)

        # remove item and size variant info, color wise and yield item from them
        for color_name in all_color_names:
            item = color_items[color_name]
            size_list = all_size_urls[color_name]
            if size_list:
                size_url, size_name = size_list.pop()
                yield Request(
                    url=size_url,
                    callback=self.parse_size,
                    meta={
                        'item': item,
                        'size_name': size_name,
                        'size_urls': size_list
                    },
                    headers={
                        'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='
                    }
                )

    def parse_size_url(self, data, color_items, all_size_urls):
        for variant in data['variants']:
            color_name = [vars['value']
                          for vars in variant['attributes']
                          if vars['name'] == 'Color']
            if not color_name:
                color_name = 'no_color'
            else:
                color_name = color_name[0]
            blacklist = ['color', 'gender']
            size_name = ['{}: {}'.format(var['name'], var['value'])
                         for var in variant['attributes']
                         if var['name'].lower() not in blacklist]
            size_name = ', '.join(size_name)
            color_items[color_name]['image_urls'] += [feature['src']
                                                      for feature in variant.get('featuredImages', [])]

            if variant.get('offerId'):
                param = {
                    'offer': variant['offerId']
                }
            else:
                param = {
                    'ssin': color_items[color_name]['base_sku']
                }
            all_size_urls[color_name].append((self.make_size_url(param), size_name))
        return all_size_urls

    def parse_size(self, response):
        data = json.loads(response.text)
        data = data['priceDisplay']['response'][0]

        item = response.meta['item']

        size_item = SizeItem()
        size_item['size_current_price_text'] = data['finalPrice']['numeric']
        size_item['size_original_price_text'] = data['oldPrice']['numeric'] or data['finalPrice']['numeric']
        size_item['size_name'] = response.meta['size_name']
        size_item['size_identifier'] = '{}_{}'.format(item['identifier'], response.meta['size_name'])
        size_item['stock'] = 1
        item['size_infos'].append(size_item)

        size_list = response.meta['size_urls']
        if size_list:
            size_url, size_name = size_list.pop()
            yield Request(
                url=size_url,
                callback=self.parse_size,
                meta={
                    'item': item,
                    'size_name': size_name,
                    'size_urls': size_list
                },
                headers={
                    'AuthID': 'aA0NvvAIrVJY0vXTc99mQQ=='
                }
            )
        else:
            item['image_urls'] = set(item['image_urls'])
            yield item

    @staticmethod
    def make_size_url(new_param):
        url = 'https://www.sears.com/content/pdp/products/pricing/v2/get/price/display/json'
        params = {
            'priceMatch': 'Y',
            'memberType': 'G',
            'urgencyDeal': 'Y',
            'site': 'SEARS',
        }
        params.update(new_param)
        url_parts = urlparse.urlparse(url)
        return url_parts._replace(query=urlencode(params)).geturl()

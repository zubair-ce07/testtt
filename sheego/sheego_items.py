# -*- coding: utf-8 -*-
import json
import re
import urllib.parse as urlparse
from copy import deepcopy
from urllib.parse import urlencode

from scrapy import Request
from scrapy import Spider

from sheego.spiders.products import *


class SheegoItemsSpider(Spider):
    name = 'sheego-items'
    blacklist_categories = [
        'Übersicht',
        'bh-beratung',
        'beratung',
        'magazin',
        'beratung fur bademode',
        'inspiration'
    ]

    def start_requests(self):
        start_url = 'https://www.sheego.de/index.php'
        params = {
            'cl': 'oxwCategoryTree',
            'jsonly': 'true',
            'sOutputType': 'js'
        }
        yield Request(
            url=self.add_query_params(start_url, params),
            callback=self.parse_category
        )

    def parse_category(self, response):
        category_data = json.loads(response.text)
        for level1 in category_data:
            if level1.get('hidden', 0):
                continue

            label1 = level1['name']
            if label1.lower() in self.blacklist_categories:
                continue

            url1 = level1.get('url')
            if url1:
                yield Request(
                    url=url1,
                    callback=self.parse_pagination,
                    meta={
                        'categories': [label1]
                    }
                )

            for level2 in level1.get('sCat', []):
                if level2.get('hidden', 0):
                    continue

                label2 = level2['name']
                if label2.lower() in self.blacklist_categories:
                    continue

                url2 = level2.get('url')
                if url2:
                    yield Request(
                        url=url2,
                        callback=self.parse_pagination,
                        meta={
                            'categories': [label1, label2]
                        }
                    )

                for level3 in level2.get('sCat', []):
                    if level3.get('hidden', 0):
                        continue

                    label3 = level3['name']
                    if label3.lower() in self.blacklist_categories:
                        continue

                    url3 = level3.get('url')
                    if url3:
                        yield Request(
                            url=url3,
                            callback=self.parse_pagination,
                            meta={
                                'categories': [label1, label2, label3]
                            }
                        )

                    for level4 in level3.get('sCat', []):
                        if level4.get('hidden', 0):
                            continue

                        label4 = level4['name']
                        if label4.lower() in self.blacklist_categories:
                            continue

                        url4 = level4.get('url')
                        if url4:
                            yield Request(
                                url=url4,
                                callback=self.parse_pagination,
                                meta={
                                    'categories': [label1, label2, label3, label4]
                                }
                            )

    def parse_pagination(self, response):
        next_page_url = response.css('.cj-paging--top .js-next::attr(href)').extract_first()
        if next_page_url:
            yield Request(
                url=response.urljoin(next_page_url),
                callback=self.parse_pagination,
                meta=response.meta
            )

        for item_url in response.css('.js-product__link::attr(href)').extract():
            yield Request(
                url=response.urljoin(item_url),
                callback=self.parse_item,
                meta=response.meta
            )

    def parse_item(self, response):
        item = Product()

        item['url'] = response.url
        item['category'] = response.meta['categories']

        data = response.css('.cj-p-details__variants')
        item['name'] = data.css('span[itemprop="name"]::text').extract_first().strip()
        item['brand'] = data.css('span[itemprop="brand"]::text').extract_first().strip()

        item['skus'] = {}

        item['base_sku'] = response.css('.at-dv-artNr::text').extract_first().strip()
        item['base_sku'] = item['base_sku'][:-2]  # remove the 2 chars at the end of string

        item['description'] = self.extract_description(response)

        out_of_stock = [name.strip() for name in response.css('.sizespots__item--strike::text').extract()]

        for color_id in response.css('.colorspots__item::attr(data-varselid)').extract():
            params = {
                'anid': item['base_sku'],
                'cl': 'oxwarticledetails',
                'varselid[0]': color_id,
            }
            yield Request(
                url=self.add_query_params(response.url, params),
                callback=self.parse_color,
                meta={
                    'item': deepcopy(item),
                    'out_of_stock': out_of_stock
                }
            )

    def parse_color(self, response):
        item = response.meta['item']

        item['color_name'] = response.css('span.at-dv-color::text').extract_first()
        item['image_urls'] = [response.urljoin(url) for url in response.css('#magic::attr(href)').extract()]

        params = {
            'anid': item['base_sku'],
            'cl': 'oxwarticledetails',
            'varselid[0]': response.css('.colorspots__item.is-active::attr(data-varselid)').extract_first(),
        }

        param_key = 'varselid[1]'  # default index value is 1
        varselid = response.css('.js-ads-script:contains("varselid")::text').extract()
        if len(varselid) == 3:  # 3 mean 3 values in varselid list
            varselid = ' '.join(varselid)
            params.update({
                param_key: re.findall("\[1\]'\] = '(.*)'", varselid)[0]
            })
            param_key = 'varselid[2]'  # use this key to fill each size varselid to create unique url

        size_urls = []
        for size_id in response.css('.sizespots__item::attr(data-varselid)').extract():
            params.update({param_key: size_id})
            size_urls.append(self.add_query_params(response.urljoin('/index.php'), params))

        if not size_urls:  # send a request with empty size to get data for single size item
            params.update({param_key: ''})
            size_urls.append(self.add_query_params(response.urljoin('/index.php'), params))

        yield Request(
            url=size_urls.pop(),
            callback=self.parse_size,
            meta={
                'item': item,
                'size_urls': size_urls,
                'out_of_stock': response.meta['out_of_stock']
            }
        )

    def parse_size(self, response):
        item = response.meta['item']

        size_item = Size_Item()
        size_name = response.css('.sizespots__item.is-active::text').extract_first()
        if size_name:
            size_item['size_name'] = size_name.strip()
        else:
            size_item['size_name'] = 'one_size'

        size_item['full_price'] = (response.css('.at-wrongprice::text').extract_first() or
                                   response.css('.at-lastprice::text').extract_first()).replace('\xa0', ' ')
        size_item['sale_price'] = response.css('.at-lastprice::text').extract_first().replace('\xa0', ' ')

        out_of_stock = response.meta['out_of_stock']
        size_item['in_stock'] = False if size_item['size_name'] in out_of_stock else True

        color_key_data = response.css('.js-ads-script:contains("colorid")::text').extract()
        color_key_data = '_'.join(color_key_data)
        color_key = re.findall("colorid = '(\d{5})'", color_key_data)

        item['skus'].update({
            '{}_{}'.format(color_key[0], size_item['size_name']): size_item
        })

        size_urls = response.meta['size_urls']
        if size_urls:
            yield Request(
                url=size_urls.pop(),
                callback=self.parse_size,
                meta={
                    'item': item,
                    'size_urls': size_urls,
                    'out_of_stock': out_of_stock
                }
            )
        else:
            yield item

    @staticmethod
    def extract_description(response):
        description = response.css('.l-startext .l-list li::text').extract()
        description += response.css('.details__box__desc p::text').extract()

        for row in response.css('.js-article-ocv .l-ph-10-md tr'):
            line = row.css('td>span::text').extract_first().strip()
            line += ': ' + row.css('td:not([class])::text').extract_first().strip()
            description.append(line)
        return description

    @staticmethod
    def add_query_params(url, params):
        url_parts = urlparse.urlparse(url)
        query = dict(urlparse.parse_qsl(url_parts.query))
        query.update(params)
        return url_parts._replace(query=urlencode(query)).geturl()
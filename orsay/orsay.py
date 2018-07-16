# -*- coding: utf-8 -*-
import json
import re
import urllib.parse as urlparse
from urllib.parse import urlencode

from scrapy import Request
from scrapy import Spider

from products import Product


class OrsaySpider(Spider):
    name = 'orsay'
    page_size = 12
    blacklist_category = ['magazin', 'specials']

    def start_requests(self):
        start_urls = 'http://www.orsay.com/de-de/'
        yield Request(url=start_urls,
                      callback=self.parse_homepage)

    def parse_homepage(self, response):
        for level1 in response.css('.header-navigation .navigation-item.level-1'):
            label1 = level1.css('a::text').extract_first('').strip()
            url1 = level1.css('a::attr(href)').extract_first()
            if label1.lower() in self.blacklist_category:
                continue

            yield Request(
                url=url1,
                callback=self.parse_pagination,
                meta={'categories': [label1]}
            )

            for level2 in level1.css('.navigation-item.level-2:not(.hidden-xlg)'):
                label2 = level2.css('a::text').extract_first('').strip()
                url2 = level2.css('a::attr(href)').extract_first()

                yield Request(
                    url=url2,
                    callback=self.parse_pagination,
                    meta={'categories': [label1, label2]})

                for level3 in level2.css('.navigation-item.level-3:not(.hidden-xlg)'):
                    label3 = level3.css('a::text').extract_first().strip()
                    url3 = level3.css('a::attr(href)').extract_first()

                    yield Request(
                        url=url3,
                        callback=self.parse_pagination,
                        meta={'categories': [label1, label2, label3]})

    def parse_pagination(self, response):
        for item in self.parse_items(response):
            yield item

        total_items = int(response.css('.pagination-product-count::attr(data-count)').extract_first('0'))
        for item_count in range(self.page_size, total_items, self.page_size):
            params = {
                'sz': self.page_size,
                'start': item_count,
                'format': 'page-element'
            }
            yield Request(url=self.add_query_params(response.url, params),
                          callback=self.parse_items,
                          meta=response.meta)

    def parse_items(self, response):
        item_urls = response.css('.product-image > a::attr(href)').extract()
        for url in item_urls:
            yield Request(url=response.urljoin(url),
                          callback=self.parse_color,
                          meta=response.meta)

    def parse_color(self, response):
        color_urls = response.css('.swatches.color > li > a::attr(href)').extract()
        for url in color_urls:
            yield Request(url=url,
                          callback=self.parse_details,
                          dont_filter=True,
                          meta=response.meta)

    def parse_details(self, response):
        item = Product()
        item['category'] = response.meta['categories']
        item['url'] = response.url
        item['name'] = response.css('h1.product-name::text').extract_first()
        item['description'] = response.css('.with-gutter::text').extract()
        item['care'] = response.css('div.product-info-title + p::text').extract()
        item['brand'] = 'Orsay'

        item['image_urls'] = self.extract_image_urls(response)

        product_details = response.css('.js-product-content-gtm::attr(data-product-details)').extract_first()
        product_details = json.loads(product_details)
        item['retailer_sku'] = product_details['productId']

        item['skus'] = {}
        # selected size sku genrated
        self.extract_size_info(product_details, item)

        # request for handleing rest of the sizes
        size_urls = response.css('.size > li:not(.selected) > a::attr(href)').extract()
        if size_urls:
            yield Request(url=size_urls.pop(),
                          callback=self.parse_size,
                          meta={
                              'item': item,
                              'size_url': size_urls
                          },
                          dont_filter=True)

    def parse_size(self, response):
        item = response.meta['item']

        product_details = response.css('.js-product-content-gtm::attr(data-product-details)').extract_first()
        product_details = json.loads(product_details)
        self.extract_size_info(product_details, item)

        size_urls = response.meta['size_url']
        if size_urls:
            yield Request(
                url=size_urls.pop(),
                callback=self.parse_size,
                meta=response.meta,
                dont_filter=True)
        else:
            yield item

    @staticmethod
    def extract_size_info(product_details, item):
        color_sku = re.findall('\d{6}', product_details['productId'])[1]

        item['skus'].update({'{}_{}'.format(color_sku, product_details['size']): {
            'color': product_details['color'],
            'currency': product_details['currency_code'],
            'price': product_details['grossPrice'],
            'size': product_details['size']
        }
        })

    def extract_image_urls(self, response):
        params = {
            'sw': 2000,
            'sh': 2000,
            'sm': 'fit'
        }
        return [self.add_query_params(url, params)
                for url in response.css('.productthumbnail::attr(src)').extract()]

    @staticmethod
    def add_query_params(url, params):
        url_parts = urlparse.urlparse(url)
        query = dict(urlparse.parse_qsl(url_parts.query))
        query.update(params)
        return url_parts._replace(query=urlencode(query)).geturl()

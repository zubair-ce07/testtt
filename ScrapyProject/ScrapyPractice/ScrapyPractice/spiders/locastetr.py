# coding: utf-8
"""
Scrapy spider for stylerunner.
@author: Muhammad Tauseeq
"""
import json
import re

from scrapy import Request
from copy import deepcopy
from urlparse import urljoin

from scrapyproduct.items import ProductItem, SizeItem
from scrapyproduct.spiderlib import SSBaseSpider
from scrapyproduct.toolbox import category_mini_item, extract_text_nodes


class LacosteSpiderTR(SSBaseSpider):
    name = 'trlac'
    long_name = 'lacostetr'
    brand = 'lacoste'
    country = 'TR'
    language_code = 'tr'
    country_code = 'tr'
    currency = 'TRY'
    max_stock_level = 1
    version = '1.0.2'
    seen_base_sku = []
    seen_identifiers = []
    base_url = 'https://www.lacoste.com.tr'
    color_url = '{}?integration_renk={}'
    nav_url = 'https://www.lacoste.com.tr/menus/generate/?format=json&depth_height=3&include_parent=true'

    def start_requests(self):
        yield Request(
            url=self.nav_url,
            callback=self.parse_homepage,
        )

    def get_level(self, node):
        return self.get_level(node['parent']) + [node.get('label')] if node.get('parent') else [node.get('label')]

    def parse_homepage(self, response):
        menus = json.loads(response.text)

        for menu in menus['menu'][:-1]:
            category = self.get_level(menu)
            meta = deepcopy(response.meta)
            meta['category'] = category
            url = '{}?page=1'.format(urljoin(self.base_url, menu.get('url')))
            yield Request(
                url=url,
                meta=meta,
                callback=self.parse_products,
            )

    def parse_pagination(self, response):
        last_page = int(
            response.xpath("//a[contains(@class,'pagination-item')][last()]/text()").extract_first(default=1))

        for page_no in range(2, last_page + 1):
            yield Request(
                url="{}={}".format(response.url.split('=')[0], page_no),
                callback=self.parse_products,
                meta=response.meta,
            )

    def parse_products(self, response):
        for product in response.css('.product-item-box'):
            item_url = product.xpath(".//p[@class='product-name']/a/@href").extract_first()
            item = ProductItem(
                url=response.urljoin(item_url),
                referer_url=response.url,
                base_sku=self.get_base_sku(item_url),
                title=product.xpath(".//p[@class='product-name']/a/text()").extract_first(),
                brand=self.brand,
                language_code=self.language_code,
                category_names=response.meta['category'],
                currency=self.currency,
                country_code=self.country_code,
            )

            yield category_mini_item(item)

            if item['base_sku'] not in self.seen_base_sku:
                self.seen_base_sku.append(item['base_sku'])
                meta = deepcopy(response.meta)
                meta['item'] = item
                yield Request(
                    url=item['url'],
                    callback=self.extract_colors,
                    meta=meta,
                )

        for req in self.parse_pagination(response):
            yield req

    def extract_colors(self, response):
        color_item = deepcopy(response.meta['item'])
        sibling_colors = response.css(".variant-colors a:not(.is-disable)::attr(data-value)").extract()
        for color in sibling_colors:
            url = self.color_url.format(response.url, color)
            color_item['url'] = url
            meta = deepcopy(response.meta)
            meta['item'] = color_item
            yield Request(
                url=url,
                meta=response.meta,
                callback=self.extract_details,
            )

    def extract_details(self, response):
        item = response.meta.get('item')
        final_item = deepcopy(item)
        final_item['image_urls'] = response.css(".js-product-slider__popup div img::attr(src)").extract()
        final_item['color_name'] = response.css(".selected-type > strong::text").extract_first('').strip()
        final_item['color_code'] = response.css(".variant-colors a.is-select::attr(data-value)").extract_first()
        final_item['identifier'] = '{}-{}'.format(final_item['base_sku'], final_item['color_code'])
        if final_item['identifier'] not in self.seen_identifiers:
            self.seen_identifiers.append(final_item['identifier'])

        final_item['description_text'] = extract_text_nodes(
            response.xpath("//div[@class='content-row']//div[@class='content']//*/text()")
        )
        self.set_prices(response, final_item)
        self.extract_sizes(response, final_item)
        yield final_item

    def set_prices(self, response, item):
        cur_price = response.xpath("//*[@class='cf']//*[@class='current-price']/text()").extract_first('')
        old_price = response.xpath("//*[@class='cf']//*[@class='old-price hidden-xs']/text()").extract_first('')

        if old_price:
            item['new_price_text'] = cur_price
            item['old_price_text'] = old_price
        else:
            item['full_price_text'] = cur_price

    def extract_sizes(self, response, item):
        in_stock_sizes = response.css(".dropdown  a.js-variant::text").extract()
        out_stock_sizes = response.css(".dropdown a.js-disable-variant::text").extract()

        item['size_infos'].extend([SizeItem(size_name=size.strip(), stock=1) for size in in_stock_sizes])
        item['size_infos'].extend(
            [SizeItem(size_name='-'.join(size.split('-')[:-1]).strip(), stock=0) for size in out_stock_sizes]
        )

    def get_base_sku(self, url):
        for base_sku in url.split('-'):
            if re.search('\d\d\d', base_sku):
                return base_sku

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
from scrapyproduct.toolbox import category_mini_item


class LacosteSpiderTR(SSBaseSpider):
    name = 'lacostetr'
    long_name = 'lacostetr'
    brand = 'lacoste'
    country = 'TR'
    language_code = 'tr'
    country_code = 'tr'
    currency = 'TRY'
    max_stock_level = 1
    version = '1.0.0'
    seen_base_sku = []
    seen_identifiers =[]
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
        if last_page != 1:
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
                base_sku=item_url.split('-')[-2],
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
                    callback=self.extract_details,
                    meta=meta,
                )

        for req in self.parse_pagination(response):
            yield req

    def extract_details(self, response):
        item = response.meta.get('item')

        mini_details = json.loads(response.css(".js-content .analytics-data::text").extract_first().strip())
        mini_details = mini_details['productDetail']['data']
        cur_price, old_price, is_dis = self.extract_price(response)

        final_item = deepcopy(item)
        final_item['sku'] = mini_details['sku']
        final_item['base_sku'] = mini_details['product_id']
        final_item['identifier'] = mini_details['dimension14']
        final_item['image_urls'] = response.css(".js-product-slider__popup div img::attr(src)").extract()
        final_item['new_price_text'] = cur_price
        final_item['old_price_text'] = old_price if is_dis else cur_price
        final_item['color_name'] = response.css(".selected-type > strong::text").extract_first('').strip()
        final_item['color_code'] = response.css(".variant-colors a.is-select::attr(data-value)").extract_first()
        final_item['description_text'] = self.extract_description(response)
        self.extract_sizes(response, final_item)

        if final_item['identifier'] not in self.seen_identifiers:
            self.seen_identifiers.append(final_item['identifier'])
            yield final_item

        for req in self.extract_colors(response):
            yield req

    def extract_colors(self, response):
        sibling_colors = response.css(".variant-colors a:not(.is-disable)::attr(data-value)").extract()
        for color in sibling_colors:
            url = self.color_url.format(response.url.split('?')[0], color)
            yield Request(
                url=url,
                meta=response.meta,
                callback=self.extract_details,
            )

    def extract_sizes(self, response, item):
        in_stock_sizes = response.css(".dropdown  a.js-variant::text").extract()
        out_stock_sizes = response.css(".dropdown a.js-disable-variant::text").extract()

        item['size_infos'].extend([SizeItem(size_name=size.strip(), stock=1) for size in in_stock_sizes])
        item['size_infos'].extend(
            [SizeItem(size_name='-'.join(size.split('-')[:-1]).strip(), stock=0) for size in out_stock_sizes]
        )

    def extract_description(self, response):
        description = response.xpath("//div[@class='content-row']//div[@class='content']//*/text()").extract()
        description = [text.strip() for text in description]
        return description

    def extract_price(self, response):
        cur_price = response.xpath("//*[@class='cf']//*[@class='current-price']/text()").extract_first('')
        old_price = response.xpath("//*[@class='cf']//*[@class='old-price hidden-xs']/text()").extract_first('')

        cur_price = re.sub("[^0-9,.]", "", cur_price)
        is_discounted = False
        if old_price:
            old_price = re.sub("[^0-9,.]", "", old_price)
            is_discounted = True

        return cur_price, old_price, is_discounted

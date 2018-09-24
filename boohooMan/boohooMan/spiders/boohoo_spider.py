import queue
import re
import time

import scrapy

from boohooMan.items import BoohoomanItem


class BoohooSpider(scrapy.Spider):
    name = "boohoo"
    start_urls = [
        'https://www.boohooman.com/',
    ]

    def __init__(self):
        self.items_set = []

    def parse(self, response):
        for item in response.css('li.has-submenu'):

            for subitem in item.css('li a'):
                next_page = subitem.css('a::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_url)

    def parse_url(self, response):
        for item in response.css('div.product-tile'):
            product_item = BoohoomanItem()
            product_item['sku'] = {}
            product_item['lang'] = response.css(
                'html::attr(lang)').extract_first()
            product_item['name'] = item.css(
                'div.product-name a::text').extract_first().strip("\n")
            product_item['date'] = time.time()
            item_url = response.urljoin(item.css(
                'div.product-image a::attr(href)')
                                        .extract_first())
            product_item['url'] = response.urljoin(item.css(
                'div.product-image a::attr(href)').extract_first())
            yield scrapy.Request(item_url, callback=self.parse_item_color,
                                 meta={'item': product_item})

        next_page = response.css(
            'li.pagination-item a::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item_color(self, response):
        product_item = response.meta['item']
        product_item['retailer_sku'] = response.css(
            'div.product-number span::text').extract_first()
        product_item['retailer'] = 'boohooman-us'
        if product_item['retailer_sku'] in self.items_set:
            return
        else:
            self.items_set = product_item['retailer_sku']
        item_colors_list = response.css('div.product-variations ul.color \
                                         li.selectable:not(.selected) \
                                         span::attr(data-href) ').extract()
        items_color_queue = queue.Queue()
        for item_url in item_colors_list:
            items_color_queue.put(scrapy.Request(item_url + "&format=ajax",
                                                 callback=self.parse_item_size,
                                                 meta={'item': product_item,
                                                       'item_colors_list':
                                                           item_colors_list}))
        while not items_color_queue.empty():
            yield items_color_queue.get()

    def parse_item_size(self, response):
        product_item = response.meta['item']
        item_colors_list = response.meta['item_colors_list']
        item_size_list = response.css('div.product-variations ul.size \
                                        li.selectable:not(.selected) \
                                        span::attr(data-href) ').extract()
        items_size_queue = queue.Queue()
        for item_url in item_size_list:
            items_size_queue.put(scrapy.Request(item_url + "&format=ajax",
                                                callback=self.parse_item_info,
                                                meta={'item': product_item,
                                                      'item_colors_list':
                                                          item_colors_list,
                                                      'item_size_list':
                                                          item_size_list}))
        while not items_size_queue.empty():
            yield items_size_queue.get()

    def parse_item_info(self, response):
        item_color = response.css(
            'div.product-variations ul.color li.selected \
              span::attr(title) ').extract_first()
        item_size = response.css(
            'div.product-variations ul.size li.selected \
              span::attr(title)').extract_first()
        item_sales_price = response.css(
            'div.product-price span.price-sales::text ').extract_first()
        item_std_price = response.css(
            'div.product-price span.price-standard::text ').extract_first()
        item_currency = response.css(
            'div.product-price meta::attr(content) ').extract_first()
        item_color = re.sub('.*: ', '', item_color)
        item_size = re.sub('.*: ', '', item_size)
        product_item = response.meta['item']
        item_colors_list = response.meta['item_colors_list']
        item_size_list = response.meta['item_size_list']
        item = {
            'colour': item_color,
            'item_size': item_size,
            'price': self.strip_chars(item_sales_price),
            'previous_prices': self.strip_chars(item_std_price),
            'currency': item_currency,
        }
        product_item['sku'].update({(item_color + "_" + item_size): item})
        item_size_list.pop()
        if not item_size_list:
            item_colors_list.pop()
        if not item_colors_list:
            yield product_item

    def strip_chars(self, str_to_strp):
        if not str_to_strp:
            return ""
        else:
            if "\u00a3" in str_to_strp:
                return str_to_strp.strip("\u00a3")
            else:
                return str_to_strp

# -*- coding: utf-8 -*-
import json
import re

import time
from __builtin__ import unicode
from scrapy.http.request import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cecil.items import CecilItem


class CecilSpider(CrawlSpider):
    name = "cecil-de"
    allowed_domains = ["cecil.de"]
    start_urls = ['http://cecil.de/']

    def process_pagination_link(link):
        match = re.search('ecs_jump\((\d+)\)', link)
        if match:
            page = match.group(1)
            return '?page='+page+'&ajax=1'
    rules = [
        Rule(LinkExtractor(restrict_css=['.mainnavigation', '#sidenavigation'])),
        Rule(LinkExtractor(restrict_css='li.produkt-bild'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.produkte-pagination',
                           attrs='onclick',
                           process_value=process_pagination_link,
                           ),
             callback='parse_ajax_page')
    ]

    def parse_item(self, response):
        garment = CecilItem()
        garment['name'] = self.product_name(response)
        garment['brand'] = 'Cecil'
        garment['category'] = self.product_category(response)
        garment['retailer'] = 'cecil-de'
        garment['price'] = self.product_price(response)
        if self.is_sale(response):
            garment['previous_price'] = self.previous_price(response)
        garment['currency'] = self.product_currency(response)
        garment['gender'] = 'women'
        garment['image_urls'] = self.product_images(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['industry'] = None
        garment['market'] = 'DE'
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['skus'] = self.product_skus(response)
        garment['date'] = int(time.time())
        return garment

    def parse_ajax_page(self, response):
        product_link_extractor = LinkExtractor(restrict_css='li.produkt-bild')
        product_links = product_link_extractor.extract_links(response)
        for link in product_links:
            yield Request(url=link.url, callback=self.parse_item)

    def product_name(self, response):
        return response.css('dd.second > h1::text').extract_first()

    def product_category(self, response):
        return response.css('ul.trail-line li:not(li:first-child) a::text').extract()

    def product_currency(self, response):
        currency_pattern = '"priceCurrency": "(.+?)",'
        return response.css('script[type="application/ld+json"]').re_first(currency_pattern)

    def product_care(self, response):
        last_li = response.css('#cbr-details-info li:last-child').extract_first()
        return re.sub('(<[^>]+>)|(<\/\w+>)', '', last_li)

    def product_description(self, response):
        short_desc = response.css('meta[name="description"]::attr(content)').extract_first()
        long_desc = response.css('div.produkt-infos div#cbr-details-info').extract_first()
        long_desc = re.sub('(<[^>]+>)|(<\/\w+>)', '', long_desc)
        return short_desc + '\r\n' + long_desc

    def product_retailer_sku(self, response):
        return response.css('script:contains("ScarabQueue.push")').re_first("push\(\['view',\s*'(.+)'")

    def product_color(self, response):
        color = response.css('ul.farbe > li.active span.tool-tip > span::text').extract_first()
        if color:
            color = color.replace(' ','_')
            return color
        else:
            # Extract color from URL
            url = response.url
            url = url.split('/')[-1].split('.')[0]
            product_name = self.product_name(response).strip().replace(' ','-')
            if product_name in url:
                return url.replace(product_name,'').lstrip('-').replace('-','_')

    def product_skus(self, response):
        skus = {}
        product_price = self.product_price(response)
        color = self.product_color(response)
        currency = self.product_currency(response)
        available_sizes = self.product_available_sizes(response)
        out_of_stock = self.out_of_stock_sizes(response)
        sizes = available_sizes if available_sizes else []
        sizes += out_of_stock if out_of_stock else []

        if sizes:
            size_details = self.product_size_details(response)
            for size in sizes:
                price = size_details[size]['price'] \
                    if size in size_details else product_price
                sku = {
                    'size': size,
                    'price': self.format_sku_price(price),
                    'colour': color,
                    'currency': currency
                }
                if size in out_of_stock:
                    sku.update({'out_of_stock': True})

                skus[color + '_' + size] = sku

        return skus

    def product_available_sizes(self, response):
        script = response.css('script:contains("var attr")')
        sizes = script.re_first('sizes = new Array([^;]*)')
        if sizes:
            sizes= re.sub('\(|\)|\'', '', sizes).split(',')
            return sizes
        return None

    def product_size_details(self, response):
        script = response.css('script:contains("var attr")')
        if script:
            match_json = re.search('(?<=eval\(\()(\{.*\})(?=\)\))',
                                   script.extract_first())
            if match_json:
                raw = match_json.group(0)
                sizes_json = json.loads(raw)
                return sizes_json
        return {}

    def out_of_stock_sizes(self, response):
        script = response.css('script:contains("var attr")')
        # Out of stock SKUs (if applicable)
        values_0 = script.re_first('values\[0\] = new Array([^;]*)')
        values_1 = script.re_first('values\[1\] = new Array([^;]*)')
        out_of_stock = []
        if values_0 and values_1:
            values_0 = re.sub('\(|\)|\'', '', values_0).split(',')
            values_1 = re.sub('\(|\)|\'', '', values_1).split(',')
            all_sizes = [size_0 + '_' + size_1
                         for size_0 in values_0
                         for size_1 in values_1]
            available_sizes = script.re_first('sizes = new Array([^;]*)')
            available_sizes = re.sub('\(|\)|\'', '',
                                     available_sizes).split(',')
            out_of_stock = list(set(all_sizes) - set(available_sizes))
        elif values_0:
            values_0 = re.sub('\(|\)|\'', '', values_0).split(',')
            # Compare values_0 and sizes
            available_sizes = script.re_first('sizes = new Array([^;]*)')
            available_sizes = re.sub('\(|\)|\'', '',
                                     available_sizes).split(',')
            out_of_stock = list(set(values_0) - set(available_sizes))
        return out_of_stock

    def format_sku_price(self, price):
        if type(price) == unicode:
            return price.split()[0].replace(',', '').replace('.', '')
        if type(price) == float:
            return str(price).replace('.', '')
        if type(price) == int:
            return price

    def product_price(self, response):
        json_text = response.css('script[type="application/ld+json"]::text').extract_first()
        product_json = json.loads(json_text)
        return product_json['offers']['price'].replace('.', '')

    def product_images(self, response):
        script = response.css('script:contains("aZoom")')
        url_pattern = re.compile('aZoom\[\d+\].*?\"(.*)\"', re.MULTILINE)
        return response.css('script:contains("aZoom")').re(url_pattern)

    def is_sale(self, response):
        return not not response.css('span.linethrough').extract()

    def previous_price(self, response):
        return response.css('span.linethrough::text')\
            .re_first('(\d+,\d+)').replace(',','')

# -*- coding: utf-8 -*-
import json
import re
import scrapy
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cecil.items import CecilItem


class CecilSpider(CrawlSpider):
    name = "cecil-de"
    allowed_domains = ["cecil.de"]
    start_urls = ['http://cecil.de/']

    rules = [
        Rule(LinkExtractor(restrict_css='.mainnavigation')),
        Rule(LinkExtractor(restrict_css='#sidenavigation')),
        Rule(LinkExtractor(restrict_css='li.produkt-bild'), callback='parse_item'),
    ]

    def parse_item(self, response):
        garment = CecilItem()
        garment['name'] = self.product_name(response)
        garment['category'] = self.product_category(response)
        garment['brand'] = 'Cecil'
        garment['retailer'] = 'cecil-de'
        garment['currency'] = self.product_currency(response)
        garment['gender'] = 'women'
        garment['care'] = self.product_care(response)
        garment['description'] = self.product_description(response)
        garment['industry'] = None
        garment['market'] = 'DE'
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['skus'] = self.product_skus(response)
        garment['date'] = None
        return garment

    def product_name(self, response):
        return response.css('dd.second > h1::text').extract_first()

    def product_category(self, response):
        return response.css('ul.trail-line li:not(li:first-child) a::text').extract()

    def product_currency(self, response):
        currency_pattern = '"priceCurrency": "(.+?)",'
        return response.css('script[type="application/ld+json"]').re_first(currency_pattern)

    def product_care(self, response):
        last_li = response.css('#cbr-details-info li:last-child').extract_first()
        return re.sub('(<[^>]+>)|(<\/\w+>)','',last_li)

    def product_description(self, response):
        return response.css('meta[name="description"]::attr(content)').extract_first()

    def product_retailer_sku(self, response):
        article_data = response.css('input[name="frArticleData"]::attr(value)').extract_first()
        article_data_json = json.loads(article_data)
        return article_data_json['sArtNum']

    def product_color(self, response):
        return response.css('ul.farbe > li.active span.tool-tip > span::text').extract_first()

    def product_skus(self, response):
        skus = {}
        script = response.css('script:contains("var attr")')
        if script:
            json_raw = re.search('(?<=eval\(\()(\{.*\})(?=\)\))', script.extract_first()).group(0)
            sizes_json = json.loads(json_raw)
            color = self.product_color(response)
            currency = self.product_currency(response)
            for size in sizes_json:
                skus[ color + '_'+ size ] = {
                    'size': size,
                    'price': self.sku_price(sizes_json[size]['price']),
                    'currency': currency,
                    'colour': color
                }
        return skus

    def sku_price(self, price):
        if type(price) == str:
            return re.sub('(\d+),(\d+)', '\\1\\2', price)
        elif type(price) == float:
            return str(price).replace('.','')
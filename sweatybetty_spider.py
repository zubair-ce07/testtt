# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sweatybetty.items import SweatybettyItem


class SweatybettySpiderSpider(CrawlSpider):
    name = 'sweatybetty_spider'
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://www.sweatybetty.com/']
    custom_settings = {'FEED_URI': 'tmp/sweatybetty.json'}

    rules = [Rule(LinkExtractor(restrict_css='.megadrop', deny='mailto')),
             Rule(LinkExtractor(restrict_css='.next')),
             Rule(LinkExtractor(restrict_css='.prodlink'), callback='parse_item')]

    def parse_item(self, response):
        product = SweatybettyItem()
        product['brand'] = 'Sweaty Betty'
        product['product_name'] = self.product_name(response)
        product['product_id'] = self.product_id(response)
        product['description'] = self.description(response)
        product['category'] = self.category(response)
        product['image_url'] = self.image_url(response)
        product['gender'] = 'girls'
        product['url'] = response.url
        product['video_url'] = self.video_url(response)
        product['skus'] = self.get_skus(response)
        yield product

    def get_skus(self, response):
        skus = {}
        s_c_reg = "vdata\d\W\d\W=new seldata\Wnew Array\W'(\w+)','([\w\s./-]+)'\W"
        sizes_colors = response.xpath("//div[@class='variant-holder']/script/text()").re(s_c_reg)
        item_list = []
        for item in sizes_colors:
            item_list.append(item)
            if 'Select Your Size' in item:
                item_list.pop()
                item_list.pop()

        size_list = []
        color_list = []
        availability = []
        for i in range(len(item_list)):
            if i % 2:
                size_list.append(item_list[i])
                if 'out of stock' in item_list[i]:
                    availability.append(False)
                else:
                    availability.append(True)
            else:
                color_list.append(item_list[i])

        sizes = []
        for s in size_list:
            sizes.append(s.split(sep='-')[0])
        sizes = set(sizes)

        colors = set(color_list)
        for color in colors:
            for item in zip(sizes, availability):
                key = color + '_' + item[0]
                skus[key] = {}
                skus[key]['color'] = color
                skus[key]['size'] = item[0]
                skus[key]['price'] = response.css('.cont-prodprice::text').extract_first()
                skus[key]['currency'] = 'GBP'
                skus[key]['availability'] = item[1]
        return skus

    def product_name(self, response):
        return response.xpath("//div[@id='productImageContainer']//@title").extract_first()

    def product_id(self, response):
        return response.xpath("//div[contains(@class, 'block valign-baseline')]"
                              "/text()").re_first("code: (\w+\d+)")

    def category(self, response):
        return response.xpath("//div[@itemprop='breadcrumb']/*/a/text()").extract()

    def description(self, response):
        description = response.xpath("//div[@itemprop='description']//text()").extract()
        description = self.clean_list(description)
        return description

    def image_url(self, response):
        return response.xpath("//a[@id='productImageLink']/@href").extract()

    def video_url(self, response):
        return response.xpath("//video[@id='videoId']//@src").extract_first()

    def clean_list(self, dirty_list):
        value_list = []
        for value in dirty_list:
            value = value.strip()
            if value and value not in value_list:
                value_list.append(value)
        return value_list

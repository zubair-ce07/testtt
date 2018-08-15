# -*- coding: utf-8 -*-
"""this is a spider to crawl hypedc website"""
import json
import scrapy


class HypedcSpider(scrapy.Spider):
    """
    this class is a scrapy spider
    """
    name = 'hypedc'
    allowed_domains = ['www.hypedc.com']
    start_urls = ['https://www.hypedc.com/mens/footwear']

    shoes_data = {}

    def parse(self, response):
        """ default callback of scrapy spider """
        for item in response.css('div.item'):
            json_data = json.loads(item.css('a.thumbnail-basic::attr(data-product)')
                                   .extract_first())
            category = json_data['category'].split('/')
            category = category[(len(category) - 1)]

            data = {
                'name': json_data['name'],
                'category': category,
                'brand': json_data['brand'],
                'price': json_data['price'],
                'id': json_data['id'],
                'variant': json_data['variant'],
                'image': item.css('img.unveil::attr(data-src)').extract_first(),
                'image_aletrnate': item.css('img.unveil::attr(data-alternate)').extract_first()
            }
            if category not in self.shoes_data:
                self.shoes_data[category] = []
            self.shoes_data[category].append(data)

        next_page_url = response.css('a.next::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(next_page_url)
        else:
            yield self.shoes_data

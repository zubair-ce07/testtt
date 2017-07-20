# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from web_spider_project.items import HypedcItem


class HypedcSpider(CrawlSpider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = [
        "https://www.hypedc.com/",
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='.next.btn.btn-primary')),
        Rule(LinkExtractor(restrict_css='.nav-primary .dropdown [href]'), callback='parse_items'),
    )
    custom_settings = {
        "ITEM_PIPELINES": {
            'web_spider_project.pipelines.WebSpiderProjectPipeline': 0,
        }
    }

    def parse_items(self, response):
        for product in response.css('#catalog-listing .item'):
            item = HypedcItem()
            self.product_attr = product.css('::attr(data-product)').extract_first()
            product_attr = json.loads(self.product_attr)
            item['item_id'] = product_attr['id']
            item['name'] = product_attr['name']
            item['brand'] = product_attr['brand']
            item['price'] = product_attr['price']
            item['color_name'] = product_attr['variant']
            item['url'] = product.css('::attr(href)').extract_first()
            request = scrapy.Request(item['url'], callback=self.parse_details,
                                     meta={'item': item})
            yield request

    def parse_details(self, response):
        item = response.meta['item']

        item = self.item_description(item, response)
        item = self.item_currency(item, response)
        item = self.item_image_urls(item, response)
        item = self.item_discount(item, response)
        return item

    def item_description(self, item, response):
        item['description'] = str(response.css('.product-description.std::text').extract_first()).strip()
        return item

    def item_currency(self, item, response):
        item['currency'] = response.css('.product-price [itemprop=priceCurrency]::attr(content)').extract_first()
        return item

    def item_image_urls(self, item, response):
        item['image_urls'] = response.css('.img-responsive.unveil::attr(data-src)').extract()
        return item

    def item_discount(self, item, response):
        discounted = response.css('#product_addtocart_form .old-price .price::text')
        if not discounted:
            item['is_discounted'] = False
        else:
            item['is_discounted'] = True
            item['old_price'] = str(
                response.css('#product_addtocart_form .old-price .price::text').extract_first()).strip()
        return item


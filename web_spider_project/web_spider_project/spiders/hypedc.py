# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from web_spider_project.items import HypedcItem
from scrapy.spiders import Rule, CrawlSpider
import json


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

    def parse_items(self, response):
        for item_selector in response.css('#catalog-listing .item'):
            item = HypedcItem()
            raw_items = item_selector.css('::attr(data-product)').extract_first()
            formatted_items = json.loads(raw_items)
            item['item_id'] = formatted_items['id']
            item['name'] = formatted_items['name']
            item['brand'] = formatted_items['brand']
            item['price'] = formatted_items['price']
            item['color_name'] = formatted_items['variant']
            item['url'] = item_selector.css('::attr(href)').extract_first()
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
        item['description'] = response.css('.product-description.std::text').extract_first()
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
            item['old_price'] = response.css('#product_addtocart_form .old-price .price::text').extract()
        return item


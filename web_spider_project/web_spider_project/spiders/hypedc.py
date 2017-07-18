# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from web_spider_project.items import HypedcProductAttr
from scrapy.spiders import Rule, CrawlSpider
import json


class Hypedc2Spider(CrawlSpider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = [
        "https://www.hypedc.com/",
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='a.next.btn.btn-primary')),
        Rule(LinkExtractor(allow='https://www.hypedc.com/womens/'), callback='parse_items'),
        Rule(LinkExtractor(allow='https://www.hypedc.com/mens'), callback='parse_items'),
        Rule(LinkExtractor(allow='https://www.hypedc.com/kids/'), callback='parse_items'),

    )

    def parse_items(self, response):
        for product_class_name in response.css('div.item.col-xs-12.col-sm-6'):
            product_attribute = HypedcProductAttr()
            product_data = product_class_name.css('a::attr(data-product)').extract_first()
            refined_data = json.loads(product_data)
            product_attribute['Item_Id'] = refined_data['id']
            product_attribute['Name'] = refined_data['name']
            product_attribute['Brand'] = refined_data['brand']
            product_attribute['Price'] = refined_data['price']
            product_attribute['Color_Name'] = refined_data['variant']
            product_attribute['Url'] = product_class_name.css('a::attr(href)').extract_first()
            request = scrapy.Request(product_attribute['Url'], callback=self.parse_details)
            request.meta['product_attribute'] = product_attribute
            yield request

    def parse_details(self, response):
        product_attribute = response.meta['product_attribute']
        product_attribute = self.get_product_details(product_attribute, response)
        product_attribute = self.get_product_discount(product_attribute, response)
        return product_attribute

    def get_product_details(self, product_attribute, response):
        product_attribute['Description'] = response.css('div.product-description.std::text').extract()
        product_attribute['Currency'] = response.css('h2.product-price>meta::attr(content)').extract()
        product_attribute['Image_Urls'] = response.css('img.img-responsive.unveil::attr(data-src)').extract()
        return product_attribute

    def get_product_discount(self, product_attribute, response):
        discount_checker = response.css('h2>div>p>span.price')
        if not discount_checker:
            product_attribute['Is_Discounted'] = 'NO'
        else:
            product_attribute['Is_Discounted'] = 'YES'
            product_attribute['Old_Price'] = response.css('h2>div>p>span.price::text').extract_first()
        return product_attribute

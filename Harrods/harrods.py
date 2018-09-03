# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from HarrodsProject.items import HarrodsItem, ProductLoader


class HarrodsSpider(CrawlSpider):
    name = 'harrods'
    allowed_domains = ['harrods.com']
    start_urls = ['http://harrods.com/']
    rules = (
            Rule(LinkExtractor(
                deny=('/designers/', '/style-notes'),
                restrict_css='.nav_list'),
                callback='parse_listing', follow=True),
            )

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield Request(url, cookies={
                    'curr': 'SGD', 'ctry': 'SG'}, callback=self.parse)

    def parse_start_url(self, response):
        pass

    def parse_listing(self, response):
        for url in self.get_product_urls(response):
            yield Request(url=url, callback=self.parse_product)
        for next_page in self.get_next_pages(response):
            yield Request(url=url, callback=self.parse_listing)

    def parse_product(self, response):
        l = ProductLoader(item=HarrodsItem(), response=response)
        l.add_value('url', [response.url])
        l.add_value('brand', 'harrods')
        l.add_css('name', 'input[name="ProductName"]::attr(value)')
        l.add_css('price', '.price_amount::text')
        l.add_css('currency', '.price_currency::text')
        l.add_css('description', '''.product-info_content p::text,
                         .product-info_content li::text''')
        l.add_css('categories', '.breadcrumb_item span::text')
        l.add_value('website_name', 'harrods.com')
        l.add_css('product_type', '.breadcrumb_item span::text')
        l.add_css('price_per_unit', '.price_amount::text')
        l.add_css('image_urls', '.pdp_images-image::attr(src)')
        return l.load_item()

    def get_product_urls(self, response):
        urls = response.css(
            ".product-grid_list .product-card_link::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_next_pages(self, response):
        urls = list(set(response.css(
            ".control_paging-list a::attr(href)").extract()))
        return [response.urljoin(url) for url in urls]

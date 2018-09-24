# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from isetanproject.items import IsetanprojectItem, ProductLoader


class IsetanSpider(scrapy.Spider):
    name = 'isetan'
    allowed_domains = ['isetan.com.sg']
    start_urls = ['http://isetan.com.sg/']

    def parse(self, response):
        for url in self.get_listing_urls(response):
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        for url in self.get_products_urls(response):
            yield Request(url=url, callback=self.parse_product)
        for url in self.get_next_pages(response):
            yield Request(url=url, callback=self.parse_listing)

    def parse_product(self, response):
        l = ProductLoader(item=IsetanprojectItem(), response=response)
        l.add_value('url', [response.url])
        l.add_css('code', '.productView-info')
        l.add_css('brand', '.product-brand::text')
        l.add_css('name', '.product-title::text')
        l.add_css('price', '.price-section span::text')
        l.add_value('currency', 'SGD')
        l.add_css('description', '.tabs-contents p::text')
        l.add_css('categories', '.breadcrumb a::text')
        l.add_css('packaging', '.productView-info-value::text')
        l.add_css('image_urls', '.productView-thumbnail-link::attr(href)')
        l.add_value('website_name', 'www.isetan.com.sg')
        l.add_css('product_type', '.breadcrumb a::text')
        l.add_css('price_per_unit', '.price-section span::text')
        return l.load_item()

    def get_products_urls(self, response):
        return response.css(".card-title a::attr(href)").extract()

    def get_listing_urls(self, response):
        urls = response.css(".navPages-item a::attr(href)").extract()
        return [response.urljoin(url) for url in urls
                if "home-care" not in url and
                "wellness" not in url and
                "departmental" not in url]

    def get_next_pages(self, response):
        urls = response.css(".pagination-item a::attr(href)").extract()
        return list(set([response.urljoin(url) for url in urls]))

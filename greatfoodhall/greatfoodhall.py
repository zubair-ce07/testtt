# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from greatfoodhallproject.items import Product, ProductLoader


class GreatfoodhallSpider(scrapy.Spider):
    name = 'greatfoodhall'
    allowed_domains = ['greatfoodhall.com']
    start_urls = ['http://greatfoodhall.com/']

    def parse(self, response):
        for url in self.get_listings_urls(response):
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        for url in self.get_products_urls(response):
            yield Request(url=url, callback=self.parse_product)
        for page_url in self.get_pagination_urls(response):
            yield Request(url=page_url, callback=self.parse_listing)

    def parse_product(self, response):
        l = ProductLoader(item=Product(), response=response)
        l.add_value('url', [response.url])
        l.add_value('code', response.url)
        l.add_css('brand', 'h1.pL6::text')
        l.add_css('name', '.description::text')
        l.add_css('price', '.itemOrgPrice2::text')
        l.add_value('currency', 'HK')
        l.add_css('description', '.description::text')
        l.add_css('categories', '.breadCrumbArea ul::text')
        l.add_css('packaging', '.w25::attr(value)')
        l.add_css('image_urls', '.productPhoto img::attr(src)')
        l.add_value('website_name', 'http://www.greatfoodhall.com')
        l.add_css('product_type', '.breadCrumbArea ul::text')
        return l.load_item()

    def get_listings_urls(self, response):
        urls = response.css(".item a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_pagination_urls(self, response):
        total_pages = re.findall('\d+', re.search(
            'totalpage = \d+', response.text).group(0))[0]
        next_pages = []
        for page in range(1, int(total_pages)+1):
            next_pages.append(response.urljoin(
                "ShowProductPage.do?curPage_1={}".format(page)))
        return next_pages

    def get_products_urls(self, response):
        return response.css(".productTmb a::attr(href)").extract()

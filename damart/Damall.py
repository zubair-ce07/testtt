# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request


class DamallSpider(CrawlSpider):
    name = 'Damall'
    allowed_domains = ['damart.co.uk']
    start_urls = ['http://damart.co.uk/']
    rules = (
            Rule(LinkExtractor(
                allow=('\d'),
                restrict_css='.ss_menu_bloc'),
                callback='parse_listing',),
            )

    def parse_listing(self, response):
        product_urls = self.get_products_urls(response)
        for url in product_urls:
            yield Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        pass

    def get_products_urls(self, response):
        urls = response.css(".ss_menu_bloc a::attr(href)").extract()
        return [response.urljoin(url) for ulr in urls]

    def get_product_imgs(self, response):
        imgs = response.css(".thumblist a::attr(href)").extract()
        return [response.urljoin(img) for img in imgs]

    def get_product_name(self, response):
        return response.css(".product-data h1::text").extract_first()

    def get_product_description(self, response):
        desc = response.css(
            ".description p::text, .description ul::text").extract()
        return "".join(desc)

    def get_product_price(self, response):
        price = response.css(".no_promo::text, .no_promo span::text").extract()
        return "".join(price).strip()

    def get_product_colors(self, response):
        return response.css(".picto_color img::attr(alt)").extract()

    def get_product_care(self, response):
        care = response.css(".description_frame div::text").extract()
        return "".join(care).strip()

    def get_product_sizes(self, response):
        pass
        
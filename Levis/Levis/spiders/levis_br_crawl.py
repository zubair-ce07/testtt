# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Levis.spiders.product_parser import ProductParser


class LevisBrCrawlSpider(CrawlSpider):
    name = 'levis-br-crawl'
    allowed_domains = ['www.levi.com.br']
    start_urls = ['https://www.levi.com.br/']

    start_time = None

    product_parser = ProductParser()

    rules = (Rule(LinkExtractor(restrict_css=".menu-departamento"), callback='parse_category'), )

    def parse(self, response):
        requests = super().parse(response)
        for request in requests:
            trail = response.meta.get('trail', [])
            trail.append(response.url)
            print("trail", trail)
            request.meta['trail'] = trail
            yield request

    def start_requests(self):
        self.start_time = datetime.datetime.now()
        return super().start_requests()

    def parse_category(self, response):
        pages = response.css(".main script").re_first(".*pagecount_.*=\s(\d+)")
        if not pages:
            return
        pages = int(pages)

        request_url = response.css(".main script").re_first(".*(/buscapagina?.*=)'")
        for page in range(1, pages + 1):
            request = scrapy.Request(response.urljoin(f"{request_url}{page}"), callback=self.parse_listings)
            trail = response.meta['trail'].copy()
            trail.append(response.url)
            request.meta['trail'] = trail
            yield request

    def parse_listings(self, response):
        product_le = LinkExtractor(allow="/p")
        for product in product_le.extract_links(response):
            request = scrapy.Request(product.url, callback=self.parse_product)
            request.meta['trail'] = response.meta['trail']
            yield request

    def parse_product(self, response):
        product = self.product_parser.parse(response)
        product['crawl_start_time'] = self.start_time

        yield product

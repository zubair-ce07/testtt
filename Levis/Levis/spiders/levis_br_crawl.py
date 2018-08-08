# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Levis.spiders.product_parser import ProductParser


class LevisBrCrawlSpider(CrawlSpider):
    name = 'levis-br-crawl'
    allowed_domains = ['www.levi.com.br']
    start_urls = ['https://www.levi.com.br/']

    product_parser = ProductParser()

    rules = (Rule(LinkExtractor(restrict_css=".menu-departamento"), callback='parse_category'),
             Rule(LinkExtractor(restrict_css=".product-name a"), callback=product_parser.parse))

    def parse(self, response):
        requests = super().parse(response)
        for request in requests:
            trail = response.meta.get('trail', []).copy()
            trail.append(response.url)
            request.meta['trail'] = trail
            yield request

    def parse_category(self, response):
        pages = response.css(".main script").re_first(".*pagecount_.*=\s(\d+)")
        if not pages:
            return
        pages = int(pages)

        request_url = response.css(".main script").re_first(".*(/buscapagina?.*=)'")
        for page in range(1, pages + 1):
            request = Request(response.urljoin(f"{request_url}{page}"))
            trail = response.meta['trail'].copy()
            trail.append(response.url)
            request.meta['trail'] = trail
            yield request


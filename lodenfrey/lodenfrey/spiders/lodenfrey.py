import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from .lodenfrey_product import ProductParser


class LodenfreySpider(CrawlSpider):

    name = "lodenfrey-crawl"
    start_urls = [
        'https://www.lodenfrey.com/',
    ]

    listing_css = ['.js-nrnavtoggle', '.nrnavflyout-lvl2', '.level-3', '.showmorebtn']
    product_css = ['.fn', '.js-nrproduct-item.title']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    product_parser = ProductParser()

    def parse(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        for req in super().parse(response):
            trail_ = trail.copy()
            req.meta['trail'] = trail_
            yield req

        for request in self.next_page_urls(response):
            yield request

    def next_page_urls(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        main_url = response.url.split('?')[0]
        url_selector = response.xpath('//script[contains(text(), '
                                      '"sAjaxUrls")]/text()').extract_first()
        if url_selector:
            raw_urls = re.findall('\[".+"\]', url_selector)[0][1:-1]
            next_urls = raw_urls.split(",")
            for url in next_urls:
                next_url = main_url+url[1:-1]
                yield Request(url=next_url, callback=self.parse,
                              method='POST', meta={'trail': trail})

    def parse_product(self, response):
        return self.product_parser.parse(response)

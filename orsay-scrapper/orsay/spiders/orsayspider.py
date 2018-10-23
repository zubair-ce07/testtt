from scrapy import Request
from w3lib.url import url_query_parameter, add_or_replace_parameter
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .ProductParser import ProductParser


class OrsaySpider(CrawlSpider):
    product_parser = ProductParser()
    name = 'orsay-crawl'
    PAGE_SIZE = 72
    product_urls = '.product-image'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    rules = (
        Rule(LinkExtractor(restrict_css=(product_urls)), callback=product_parser.parse),
    )

    def parse(self, response):
        css = '[class*=pagination-product-count]::attr(data-count)'
        total_items = response.css(css).extract_first()
        css = '.load-more-progress-label span::text'
        shown_items = response.css(css).extract_first()

        if int(total_items.replace('.', '')) > int(shown_items.replace('.', '')):
            parameter = url_query_parameter(response.url, "sz", 0)
            url = add_or_replace_parameter(response.url, 'sz', str(int(parameter) + self.PAGE_SIZE))
            yield Request(url=url, callback=self.parse)

        yield from super(OrsaySpider, self).parse(response)

import scrapy

from w3lib.url import url_query_parameter, add_or_replace_parameter
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .ProductParser import ProductParser


class OrsaySpider(CrawlSpider):

    product_parser = ProductParser()
    name = 'orsay-crawl'
    PAGE_SIZE = 72
    navigation_bar_urls = '.navigation-link'
    product_urls = '.product-image'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    my_urls = []

    rules = (
        Rule(
            LinkExtractor(restrict_css=(navigation_bar_urls)),
            callback='parse'),

        Rule(
            LinkExtractor(restrict_css=(product_urls)),
            callback=product_parser.parse),
    )

    def parse(self, response):
        total_items = self.product_parser.extract_total_items(response)
        shown_items = self.product_parser.extract_shown_items(response)

        if int(total_items.replace('.', '')) > int(shown_items.replace('.', '')):
            parameter = url_query_parameter(response.url, "sz")
            if parameter:
                url = add_or_replace_parameter(
                    response.url, 'sz', str(int(parameter) + self.PAGE_SIZE))
            else:
                url = add_or_replace_parameter(response.url, 'sz', '144')

            yield scrapy.Request(url=url, callback=self.parse)

        yield from super(OrsaySpider, self).parse(response)

import scrapy
import w3lib.url

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .ProductParser import ProductParser


class OrsaySpider(CrawlSpider):

    product_parser = ProductParser()
    name = 'orsayspider'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    rules = (
        Rule(
            LinkExtractor(restrict_css=('.level-3')),
            callback='parse'),

        Rule(
            LinkExtractor(restrict_css=('.thumb-link')),
            callback=product_parser.parse),
    )

    def parse(self, response):
        total_items = response.css(
            '[class*=pagination-product-count]::attr(data-count)').extract_first()
        shown_items = response.css(
            '.load-more-progress-label span::text').extract_first()

        if int(total_items.replace('.', '')) > int(shown_items.replace('.', '')):
            parameter = w3lib.url.url_query_parameter(response.url, "sz")
            if parameter:
                url = w3lib.url.add_or_replace_parameter(
                    response.url, 'sz', str(int(parameter) + 72))
            else:
                url = response.url+'?sz=144'

            yield scrapy.Request(url=url, callback=self.parse)

        yield from super(OrsaySpider, self).parse(response)

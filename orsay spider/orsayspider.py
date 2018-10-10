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
            callback='caller_parse_product_details'),
        )
    def caller_parse_product_details(self, response):
        return self.product_parser.parse_product_details(response)

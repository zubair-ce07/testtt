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
        Rule(LinkExtractor(allow=('/de-de/produkte/.*/$', )), 
        callback='parse_product_page'),
    )
    
    def parse_product_page(self, response):
        
        css = 'a[class*=thumb-link]::attr(href)'
        product_page_links = response.css(css).extract()

        for link in product_page_links:
            yield response.follow(url=response.urljoin(link), 
                            callback=self.product_parser.parse_product_details)
        
        css = 'div[class*=load-next-placeholder]'
        load_more = response.css(css).extract_first()

        if load_more:
            parameter = w3lib.url.url_query_parameter(response.url, "sz")
            if parameter:
                link = w3lib.url.add_or_replace_parameter(response.url, 'sz', 
                                                    str(int(parameter)+72))
            else:
                link = response.url + '?sz=72'
                
        yield scrapy.Request(url=response.urljoin( link), 
                            callback=self.parse_product_page)
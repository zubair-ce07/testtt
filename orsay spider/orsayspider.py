import scrapy
import logging
import w3lib.url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor 

from .productclass import Product
from .dataGetter import DataGetterClass

class OrsaySpider(CrawlSpider):

    data_getter_class = DataGetterClass()
    name = 'orsayspider'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    rules = (
        Rule(LinkExtractor(allow=('/de-de/produkte/.*/$', )), 
        callback='parse_product_page'),
    )
    
    def parse_product_page(self, response):
        
        xpath = '//a[contains(@class, "thumb-link")]/@href'
        product_page_links = response.xpath(xpath).extract()

        for link in product_page_links:
            yield response.follow(url=response.urljoin(link), 
                                callback=self.data_getter_class.parse_product_details, 
                                dont_filter=True)
        
        xpath = '//div[contains(@class, "load-next-placeholder")]'
        load_more = response.xpath(xpath).extract_first()

        if load_more:
            parameter = w3lib.url.url_query_parameter(response.url, "sz")
            if parameter:
                link = w3lib.url.add_or_replace_parameter(response.url, 
                                                        'sz', 
                                                        str(int(parameter)+72))
            else:
                link = response.url + '?sz=72'
                
        yield scrapy.Request(response.urljoin( link), callback=self.parse_product_page)
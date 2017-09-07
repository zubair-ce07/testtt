import scrapy


class LindeSpider(scrapy.Spider):
    name = 'lindex'
    allowed_domains = ['https://www.lindex.com/']
    start_urls = ['https://www.lindex.com/']

    def parse(self, response):
        pass

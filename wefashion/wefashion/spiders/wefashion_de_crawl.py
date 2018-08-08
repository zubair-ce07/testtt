import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WefashionDeCrawlSpider(scrapy.Spider):
    name = 'wefashion-de-crawl'
    start_urls = ['http://https://www.wefashion.de//']

    def parse(self, response):
        pass

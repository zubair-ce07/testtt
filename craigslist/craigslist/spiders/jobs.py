import scrapy

from craigslist.items import CraigslistItem
from scrapy.loader import ItemLoader


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://newyork.craigslist.org/search/egr']
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        for selector in response.xpath('//li[@class="result-row"]'):
            item = ItemLoader(CraigslistItem(), selector=selector)
            item.add_xpath('title', './/a[@class="result-title hdrlnk"]')
            item.add_xpath('URL', './/a[@class="result-title hdrlnk"]/@href')
            item.add_xpath('location', './/span[@class="result-hood"]')
            item.add_xpath('datetime', './/time/@datetime')
            yield item.load_item()
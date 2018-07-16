import scrapy

from craigslist.items import CraigslistItem
from scrapy.loader import ItemLoader
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        for selector in response.xpath('//li[@class="result-row"]'):
            item = ItemLoader(CraigslistItem(), selector=selector)
            item.add_xpath('Title', './/a[@class="result-title hdrlnk"]')
            item.add_xpath('URL', './/a[@class="result-title hdrlnk"]/@href')
            item.add_xpath('Location', './/span[@class="result-hood"]')
            item.add_xpath('datetime', './/time/@datetime')
            yield item.load_item()

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        yield Request(absolute_next_url, callback=self.parse)
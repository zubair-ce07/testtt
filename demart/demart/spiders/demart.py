"""
This module crawls pages and gets data.
"""
import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import Product


class DeMart(scrapy.Spider):
    """This class crawls Sheego pages"""
    name = 'demart'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_url = 'http://www.demart.com.pl/'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """This method crawls page urls."""
        category_url = response.css('li>a::attr(href)').extract()
        for link in category_url:
            url = response.urljoin(link)
            yield scrapy.Request(
                url=url, callback=self.parse_item_url)

    def parse_item_url(self, response):
        """This method crawls item detail url."""
        item_url = response.css('.right>a::attr(href)').extract()
        for link in item_url:
            url = response.urljoin(link)
            yield scrapy.Request(
                url=url, callback=self.parse_item_detail)

    def parse_item_detail(self, response):
        """This method crawls item details."""
        information = []
        description = response.css('.trunc>p::text').extract()
        if len(description) == 1:
            description = response.css('.trunc>div::text').extract()
        description = ''.join(description).strip()
        title = response.css('.product::text').extract_first()
        info = response.css('div.info>div>p::text').extract()
        data_found = response.css('div.info>div>p>strong::text').extract()
        series = response.css('p>a::text').extract_first()
        for index, source_data in enumerate(info):
            # storing data in list that is fetched.
            key = data_found[index].strip()
            key = re.split(':', key)[0]
            data = {
                key: source_data.strip(),
            }
            information.append(data)
        if series:
            series = series.strip()
        else:
            series = 'None'
        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('item_detail_link', response.url)
        loader.add_value('title', title.strip())
        loader.add_value('series', series)
        loader.add_value('description', description)
        loader.add_value('information', information)
        return loader.load_item()

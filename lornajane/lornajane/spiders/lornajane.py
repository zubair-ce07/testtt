"""
This module crawls pages and gets data.
"""
import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import Product


class SheegoSpider(scrapy.Spider):
    """This class crawls Sheego pages"""
    name = 'lornajane'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_url = 'https://www.lornajane.sg/'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """This method crawls page urls."""
        level1_link = response.css(
            '.yCmsComponent>a::attr(href)').extract()
        for url in level1_link:
            category_url = response.urljoin(url)
            yield scrapy.Request(
                url=category_url, callback=self.parse_item_url)

    def parse_item_url(self, response):
        """This method crawls item detail url."""
        item_url = response.css('.product-name-price>a::attr(href)').extract()
        for url in item_url:
            item_url = response.urljoin(url)
            yield scrapy.Request(
                url=item_url, callback=self.parse_item_detail)

    def parse_item_detail(self, response):
        """This method crawls item detail information."""
        title = response.css('.pro-heading-sec>h1::text').extract_first()
        full_price = response.css('div.price>span::text').extract()[1]
        sale_price = response.css('div.price::text').extract()[1]
        product_code = response.css('.mobile_toggle>p::text').extract_first()
        description = response.css('.mobile_toggle>p::text').extract()[1]
        description = ''.join(description).strip()
        filter_productcode = re.split(':', product_code)
        if full_price == 'SGD':
            full_price = sale_price
        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('item_detail_url', response.url)
        loader.add_value('title', title.strip())
        loader.add_value('product_code', filter_productcode[1])
        loader.add_value(
            'full_price', full_price)
        loader.add_value(
            'sale_price', sale_price)
        loader.add_xpath(
            'sizes', "//a[@class=' product-detail-swatch-btn']/text()")
        loader.add_value('description', description)
        loader.add_css('more_description', '.mobile_toggle>ul>li::text')
        return loader.load_item()

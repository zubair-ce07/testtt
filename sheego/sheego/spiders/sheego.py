"""
This module crawls pages and gets data.
"""
import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import Product


class SheegoSpider(scrapy.Spider):
    """This class crawls Sheego pages"""
    name = 'sheego'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_url = 'https://www.sheego.de/'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """This method crawls page urls."""
        level1_link = response.css(
            '.cj-mainnav__entry>a::attr(href)').extract()
        for url in level1_link:
            yield scrapy.Request(
                url=url, callback=self.parse_item_url)

    def parse_item_url(self, response):
        """This method crawls item detail url."""
        item_url = response.css(
            '.product__wrapper--bottom>a::attr(href)').extract()
        for url in item_url:
            if url != '#':
                item_url = response.urljoin(url)
                yield scrapy.Request(
                    url=item_url, callback=self.parse_item_detail)
        next_page = response.css(
            '.paging__btn--next>a::attr(href)').extract_first()
        if next_page:
            # checking if there is next page
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page_url, callback=self.parse_item_url)

    def parse_item_detail(self, response):
        """This method crawl item detail information."""
        available_size = []
        pattern = r'^[A-Z\d/\s]+$'
        title = response.css('.p-details__name::text').extract_first()
        item_size = response.css('.c-sizespots>.at-dv-size-button::text').extract()
        full_price = response.css(
            'section.p-details__price>span.product__price__wrong::text').extract_first()
        sale_price = response.css('.at-lastprice::text').extract_first()
        if not full_price:
            full_price = sale_price
        category = response.css(
            '.l-bold.l-text-1::text').extract_first().strip()
        for size in item_size:
            modified_data = re.match(pattern, size, flags=re.MULTILINE)
            if modified_data:
                available_size.append(modified_data.group().strip())
            else:
                available_size.append(size)
        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('item_detail_url', response.url)
        loader.add_value('category', category)
        loader.add_value('product_title', title.strip())
        loader.add_value(
            'full_price', full_price)
        loader.add_value(
            'sale_price', sale_price)
        loader.add_value('sizes', available_size)
        loader.add_css('description', '.l-mb-5>.l-list--nospace>li::text')
        return loader.load_item()

"""
This module crawls pages and gets data.
"""
import scrapy
from scrapy.loader import ItemLoader
from ..items import Product


class SheegoSpider(scrapy.Spider):
    """This class crawls Sheego pages"""
    name = 'damart'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_url = 'https://www.damart.co.uk/'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        """This method crawls page urls."""
        category_link = response.css('ul>li>a::attr(href)').extract()
        for url in category_link:
            category_url = response.urljoin(url)
            yield scrapy.Request(
                url=category_url, callback=self.parse_item_url)

    def parse_item_url(self, response):
        """This method crawls item detail url."""
        item_url = response.css('.photo-data>a::attr(href)').extract()
        for url in item_url:
            item_url = response.urljoin(url)
            yield scrapy.Request(
                url=item_url, callback=self.parse_item_detail)

    def parse_item_detail(self, response):
        """This method crawls item detail information."""
        title = response.css('.product-data>h1::text').extract_first()
        product_id = response.css('.t-zone>p>span::text').extract_first()
        title_description = response.css(
            '.title_description_product>strong::text').extract_first()
        description = response.css(
            '.new_info-desc>.product-info>li::text').extract()
        more_description = response.css(
            '.new_info-desc>.para_hide::text').extract()
        full_price = response.css(
            '.no_promo::text').extract_first()
        if not full_price:
        # if item is on sale
            full_price = response.css(
                '.old-price>span::text').extract_first()
            sale_price = response.css(
                '.price.sale::text').extract_first()
            discount_upto = response.css(
                '.promotion_img>.rate::text').extract_first()
        else:
            discount_upto = '0'
            sale_price = full_price
        full_price = full_price + '00'
        sale_price = sale_price + '00'
        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('item_detail_url', response.url)
        loader.add_value('title', title.strip())
        loader.add_value('product_id', product_id)
        loader.add_value(
            'title_description', title_description)
        loader.add_value(
            'description', description)
        loader.add_value('more_description', more_description)
        loader.add_value('full_price', full_price)
        loader.add_value('sale_price', sale_price)
        loader.add_value('discount_upto', discount_upto)
        return loader.load_item()

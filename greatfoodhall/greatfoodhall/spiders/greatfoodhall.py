"""
This module crawls pages and get data.
"""
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Product


class GreatFoodHallSpider(CrawlSpider):
    """This class crawls greatfoodhall pages"""
    name = 'greatfoodhall'
    allowed_domains = ['greatfoodhall.com']
    start_urls = ['http://www.greatfoodhall.com']
    rules = [
        Rule(LinkExtractor(
            allow=(r'http://www.greatfoodhall.com/eshop/ShowProductPage.do.*')),
             callback='parse_categories')
    ]

    def parse_products(self, response):
        """This method get next page urls"""
        yield scrapy.Request(url=response.url, callback=self.parse_product_details,
                             meta={'cookiejar': response.meta['cookiejar']}, dont_filter=True)

    def parse_categories(self, response):
        """This method crawls product detail urls"""
        item_detail_link = response.css('.productTmb>a::attr(href)').extract()
        for index, url in enumerate(item_detail_link):
            yield scrapy.Request(
                url=url, meta={'cookiejar': index}, callback=self.parse_products)

        total_pages = re.search('totalpage = \d+', response.text).group()
        total_pages = int(re.split(' = ', total_pages)[1])
        for page in range(1, total_pages+1):
            next_page = response.urljoin(
                'ShowProductPage.do?curPage_1={}'.format(page))
            yield scrapy.Request(
                url=next_page, callback=self.parse_categories)

    def parse_product_details(self, response):
        """This method crawls product details"""
        price_data = []
        title = response.css('div.middleArea>h1::text').extract_first()
        desc = response.css('p.description::text').extract_first()
        price = response.css('.itemOrgPrice2::text').extract_first()
        quantity = response.css('.ml.pB5.pL6::text').extract_first()
        if not quantity:
            quantity = response.css('.priceBox>.pB5::text').extract_first()

        if not price:
            old_price = response.css('.oldPrice::text').extract_first()
            new_price = response.css('.newPrice::text').extract_first()
            price = {
                'old_price': old_price,
                'new_price': new_price
            }
            price_data.append(price)
        else:
            price_data.append(price)
        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('item_detail_url', response.url)
        loader.add_value('title', title)
        loader.add_value('description', desc)
        loader.add_value(
            'quantity', quantity)
        loader.add_value(
            'price', price_data)
        return loader.load_item()

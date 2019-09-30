import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

from ..items import ProductsItem

categories = []


def process_links(value):
    categories.append(value.split('/')[-1])
    return value


class BeginningBoutique(CrawlSpider):
    name = "beginning_botique"
    market = 'AU'
    retailer = 'beginningboutique-au'
    start_urls = ['https://www.beginningboutique.com.au/']
    rules = [
        Rule(LinkExtractor(restrict_css=['.site-nav', '.pagination'], process_value=process_links),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=['.product-card'], process_value=process_links),
             callback='parse_product'),
    ]

    def parse_product(self, response):
        item = ProductsItem()
        item['gender'] = 'Women'
        item['currency'] = response.css('.product-wrapper meta::attr(content)').get()
        item['url_original'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['brand'] = response.css('.product-heading__vendor a::text').get()
        item['name'] = response.css('.product-heading__title::text').get()
        item['price'] = response.css('.product__price').xpath("//span[@class='money']/text()").get()
        product_spec = response.css('.product__specs-detail')
        item['categories'] = categories
        item['care'] = product_spec[1].css(".product__specs-detail ::text").getall()
        item['description'] = product_spec[0].css(".product__specs-detail ::text").getall()
        item['image_urls'] = response.css('.product-images__slide').xpath(".//img/@src").getall()
        item['skus'] = dict()
        sizes = response.css('.input--full option::attr(value)').getall()
        for size in sizes:
            if size in item['skus'].keys():
                item['skus'][size].append({'size': size, 'price': item['price'],
                                           'currency': item['currency']})
            else:
                item['skus'][size] = {'size': size, 'price': item['price'],
                                      'currency': item['currency']}

        yield item

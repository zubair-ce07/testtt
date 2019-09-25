import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import ProductsItem


class BeginningBoutique(CrawlSpider):
    name = "beginning_botique"
    market = 'AU'
    retailer = 'beginningboutique-au'
    start_urls = ['https://www.beginningboutique.com.au/']
    rules = [
           Rule(LinkExtractor(restrict_css=['.site-nav', '.pagination']), callback='parse'),
           Rule(LinkExtractor(restrict_css=['.product-card']), callback='parse_product'),
         ]

    def parse_product(self, response):
        item = ProductsItem()
        item['gender'] = 'Women'
        item['currency'] = 'AUD'
        item['url_original'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['brand'] = response.css('.product-heading__vendor a::text')[0].extract()
        item['name'] = response.css('.product-heading__title::text')[0].extract()
        item['price'] = response.css('.product__price').xpath("//span[@class='money']/text()").extract_first()
        product_spec = response.css('.product__specs-detail')
        item['care'] = product_spec[1].xpath(".//ul//div//li/text()").extract()
        item['description'] = product_spec[0].xpath(".//p/text()").extract()
        item['description'].extend(product_spec[0].xpath(".//ul//li/text()").extract())
        item['image_urls'] = response.css('.product-images__slide').xpath(".//img/@src").extract()
        yield item



import json
import math
import re
from datetime import datetime
import scrapy
import w3lib.url

class OrsaySpider(scrapy.Spider):
    name = "orsay_spider"
    start_urls = ['http://www.orsay.com/de-de/produkte/']
    product_url = "http://www.orsay.com"
    page_size = 72
    crawl_start_time = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')

    def parse(self, response): 
        for url in response.css('.product-tile .product-image > a::attr(href)').extract():
            yield scrapy.Request(url=self.product_url + url, callback=self.parse_details)
        if "?sz" not in response.url:
            total_products = int(re.search(r'\d+', response.css('.load-more-progress-label::text').extract()[1] \
                                .replace('.', '')).group())
            for size in range(2, math.ceil(total_products / self.page_size)):
                yield scrapy.Request(url=w3lib.url.add_or_replace_parameter(response.url, "sz", self.page_size * size)) 

    def parse_details(self, response):
        product_detail = json.loads(response.css('.js-product-content-gtm::attr(data-product-details)').extract_first())
        yield{
            "pid" : product_detail["idListRef6"],
            "gender" : "women",
            "category" : response.css('.breadcrumb-element-link > span::text').extract(),
            "url" : response.url,
            "name" : product_detail["name"],
            "description" : response.css('.with-gutter::text, .product-info-title::text, .product-material > p::text').extract(),
            "skus" : self.skus(response, product_detail),
            "image_urls" : [w3lib.url.url_query_cleaner(img_url) for img_url in response.css('.js-thumb > img::attr(src)').extract()],
            "crawl_start_time" : self.crawl_start_time
        }      

    def skus(self, response, product_detail):
        skus = []
        for size, availibility in zip(response.css('.size > li > a::text').extract(), \
                                      response.css('.size > li').xpath("@class").extract()):
            if size and availibility:
                sku_item = {"price" : product_detail["grossPrice"],
                            "currency" : product_detail["currency_code"],
                            "colour" : product_detail["color"],
                            "size" : size.strip('\n'),
                            "out_of_stock" : "true" if availibility is 'selectable' or 'selectable selected' else "false",
                            "sku_id" : product_detail["idListRef6"] + '_' + size.strip('\n')}
                skus.append(sku_item)
        return skus

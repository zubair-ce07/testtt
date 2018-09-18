import json
import math
import re
from datetime import datetime
import scrapy

class OrsaySpider(scrapy.Spider):
    name = "orsay_spider"
    start_urls = ['http://www.orsay.com/de-de/produkte/']
    product_url = "http://www.orsay.com"
    per_page_products = 72

    def parse(self, response):
        for url in response.css('div.product-tile div.product-image > a::attr(href)').extract():
            yield scrapy.Request(url = self.product_url + url, callback=self.parse_details)
        if "?sz" not in response.url:
            total_products = int(re.search(r'\d+', response.css('div.load-more-progress-label::text').extract()[1].replace('.', '')).group())
            for page_size in range(2, math.ceil(total_products / self.per_page_products)):
                yield scrapy.Request(url = response.urljoin("?sz=" + str(self.per_page_products * page_size))) 

    def parse_details(self, response):
        crawl_start_time = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')
        product_detail = json.loads(response.css('div.js-product-content-gtm::attr(data-product-details)').extract_first())
        yield{
            "pid" : product_detail["idListRef6"],
            "gender" : "women",
            "category" : response.css('a.breadcrumb-element-link > span::text').extract(),
            "url" : response.url,
            "name" : product_detail["name"],
            "description" : response.css('.js-collapsible > .with-gutter::text, div.product-info-title::text, .product-material > p::text').extract(),
            "skus" : self.skus(response, product_detail),
            "image_urls" : [img_url[:img_url.index("?")] for img_url in response.css('div.js-thumb > img::attr(src)').extract()],
            "crawl_start_time" : crawl_start_time
        }      

    def skus(self, response, product_detail):
        skus = []
        for size, availibility in zip(response.css('ul.size > li >a::text').extract(),response.css('.size > li').xpath("@class").extract()):
            if size and availibility:
                sku_item = {"price" : product_detail["grossPrice"],
                            "currency" : product_detail["currency_code"],
                            "colour" : product_detail["color"],
                            "size" : size.strip('\n'),
                            "out_of_stock" : True if availibility is 'selectable' or 'selectable selected' else False,
                            "sku_id" : product_detail["idListRef6"] + '_' + size.strip('\n')}
                skus.append(sku_item)
        return skus

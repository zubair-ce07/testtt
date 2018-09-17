import scrapy
import json
import re

class OrsaySpider(scrapy.Spider):
    name = "orsay_spider"
    start_urls = ['http://www.orsay.com/de-de/produkte/']
    product_url = "http://www.orsay.com"

    def parse(self, response):
        for url in response.css('div.product-tile div.product-image > a::attr(href)').extract():
            yield scrapy.Request(url = self.product_url + url, callback=self.parse_details)
        total_products = int(re.search(r'\d+', response.css('div.load-more-progress-label::text').extract()[1].replace('.', '')).group())
        if "?sz" not in response.url:
            for page_size in range(2, total_products/72):
                yield scrapy.Request(url = response.urljoin("?sz=" + (72 * page_size))) 

    def parse_details(self, response):
        product_detail = json.loads(response.css('div.js-product-content-gtm::attr(data-product-details)').extract_first())
        yield{
            "pid" : product_detail["idListRef6"],
            "gender" : "women",
            "category" : response.css('a.breadcrumb-element-link > span::text').extract(),
            "url" : response.url,
            "name" : product_detail["name"],
            "description" : response.css('.js-collapsible > .with-gutter::text, div.product-info-title::text, .product-material > p::text').extract(),
            "skus" : self.skus(response, product_detail),
            "image_urls" : [img_url[:img_url.index("?")] for img_url in response.css('div.js-thumb > img::attr(src)').extract()]
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

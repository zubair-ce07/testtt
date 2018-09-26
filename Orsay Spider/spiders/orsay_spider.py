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
        css = '.product-tile .product-image > a::attr(href)'
        urls = response.css(css).extract()
        for u in urls:
            url = w3lib.url.urljoin(self.product_url, u)
            yield scrapy.Request(url, callback=self.parse_details)

        if "?sz" not in response.url:
            css = '.load-more-progress-label::text'
            total_products = response.css(css).extract()[1]
            total_products = int(re.search(r'\d+', total_products.replace('.', '')).group())
            total_pages = math.ceil(total_products / self.page_size)

            for size in range(2, total_pages):
                url = w3lib.url.add_or_replace_parameter(response.url, "sz", self.page_size * size)
                yield scrapy.Request(url) 

    def parse_details(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        product_detail = json.loads(response.css(css).extract_first())
        skus = self.skus(response, product_detail)

        css = '.breadcrumb-element-link > span::text'
        category = response.css(css).extract()

        css = '.with-gutter::text, .product-info-title::text, .product-material > p::text'
        description = response.css(css).extract()

        css = '.js-thumb > img::attr(src)'
        image_urls = [w3lib.url.url_query_cleaner(url) for url in response.css(css).extract()]

        yield{
            "pid" : product_detail["idListRef6"],
            "gender" : "women",
            "category" : category,
            "url" : response.url,
            "name" : product_detail["name"],
            "description" : description,
            "skus" : skus,
            "image_urls" : image_urls,
            "crawl_start_time" : self.crawl_start_time
        }      

    def skus(self, response, product_detail):
        skus = []
        sizes = response.css('.size > li > a::text').extract()
        availablities = response.css('.size > li::attr(class)').extract()
        
        for size, availability in zip(sizes, availablities):
            if size.strip('\n') and availability:
                size = size.strip('\n')
                sku_id = product_detail["idListRef6"] + '_' + size
                out_of_stock = availability is 'selectable' or availability is 'selectable selected'

                sku_item = {"price" : product_detail["grossPrice"],
                            "currency" : product_detail["currency_code"],
                            "colour" : product_detail["color"],
                            "size" : size,
                            "out_of_stock" : out_of_stock,
                            "sku_id" : sku_id}
                skus.append(sku_item)
        return skus

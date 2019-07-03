import json
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ProductsSpider(CrawlSpider):
    name = "check"
    start_urls = [
        'https://www.woolrich.com/mens-light-flannel-shirt-john-rich-bros-wx0005/'
    ]
    
    def parse(self, response):
        myvar = 'hello'
        yield scrapy.FormRequest(url="https://www.woolrich.com/remote/v1/product-attributes/1505",
                        formdata={
                            'action': 'add',
                            'attribute[3025]': '11112',
                            'attribute[3026]': '11120',
                            'product_id': '1505',
                            'qty[]': '1'
                        },
                        meta={'word':myvar},
                        callback=self.parse_type)

    def parse_type(self, response):
        data = json.loads(response.text)
        yield{
            'sku': data['data']['sku'],
            'word': response.meta['word']
        }
        
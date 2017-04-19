import scrapy
import json
import re
from kith.items import KithItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ShoppingCartSpider(CrawlSpider):
    name = "shoping"
    start_urls = ['https://kith.com']
    rules = (
            Rule(LinkExtractor(restrict_css=".ksplash-header-upper-items>li>a",), follow=True),
            Rule(LinkExtractor(restrict_xpaths="//*[@class='main-nav-list-subtitle']/parent::li[1]//following-sibling::li/a",), follow=True),
            Rule(LinkExtractor(restrict_css="li.main-nav-list-item:nth-child(2)>a",),follow=True),
            Rule(LinkExtractor(restrict_css="a[class='product-card-info']",),callback='final_products_details',follow=True)
            )

    def final_products_details(self, response):
        #final products detail
        item = KithItem()
        item['image_link'] = response.css(".full-width::attr(src)").extract()
        prod_detail_dict = response.xpath(".//script[contains(., 'var meta')]/text()").re('var\s*meta\s*=\s*([^;]+)')[0]
        loads_prod_data = json.loads(prod_detail_dict)
        new_dict = {}
        for x in loads_prod_data['product']['variants']:
            new_dict[x['sku']]={
                            'id'   :x['id'],
                            'name' :x['name'],
                            'price':x['price'],
                            'size' :x['public_title']
                                }
        item['skus'] = new_dict
        yield item
























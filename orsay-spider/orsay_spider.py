import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from orsay.items import OrsayItem

class ShoppingCartSpider(CrawlSpider):
    name = "shoping"
    start_urls = ['http://www.orsay.com/de-de/']
    rules = (
            Rule(LinkExtractor(restrict_css=".level1>li>a", ), follow=True),
            Rule(LinkExtractor(restrict_css=".product-colors.product-item-color>li>a",),callback='final_product_detail',follow=True),
            )

    def final_product_detail(self,response):
        item = OrsayItem()
        product_dict = {}
        item_id = response.css(".product-main-info>.sku::text").re('(?:Artikel-Nr).:\s(\d{10})')
        size = response.css(".sizebox-wrapper>ul>li::text").extract()
        new_size = (x.strip() for x in size)
        size_list = [x for x in new_size if x]
        style = response.css(".sizebox-wrapper>ul>li::attr(style)").extract()
        name = response.css(".product-name::text").extract()[0].strip()
        colour = response.css(".has-tip::attr(title)").extract()[0].strip()
        price = response.css(".price::text").extract()[0].strip()
        stock = response.css(".sizebox-wrapper>ul>li::attr(data-qty)").extract()[0].strip()
        for x in size_list:
                for y in item_id:
                        product_dict["%s_%s"%(y,x)]= {
                        'name'  :  name,
                        'size'  : 'OneSize' if style else x,
                        'colour':  colour,
                        'price' :  price,
                        'stock' :  stock
                }
        item['skus'] = product_dict
        item['image_urls'] = response.css('.product-image-gallery-thumbs>a::attr(href)').extract()
        yield item












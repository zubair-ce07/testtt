import scrapy
import json
import re
from kith.items import KithItem

class ShoppingCartSpider(scrapy.Spider):
    name = "shoping"
    start_urls = ['https://kith.com']
    def parse(self, response):
        urls = response.css('.ksplash-header-upper-items>li>a::attr(href)').extract()
        for url in urls:
            absolute_urls = response.urljoin(url)
            yield scrapy.Request(url=absolute_urls, callback=self.main_categories_links)

    def main_categories_links(self, response):
        # Fetch main categories for all genders

        category_url = response.xpath("//*[@class='main-nav-list-subtitle']"
                                      "/parent::li[1]//following-sibling::li/a/@href").extract()
        if category_url:
            for cat_url in category_url:
                absolute_cat_urls = 'https://kith.com{}'.format(cat_url)
                yield scrapy.Request(url=absolute_cat_urls, callback=self.products_main_page)
        else:
            kid_cat_url = response.css("li.main-nav-list-item:nth-child(2)>a::attr(href)").extract()
            for kid_url in kid_cat_url:
                absolute_kid_urls = 'https://kith.com{}'.format(kid_url)
                yield scrapy.Request(url=absolute_kid_urls, callback=self.products_main_page)

    def products_main_page(self, response):
        #creats all the products link for further use

        product_links = response.xpath("//a[@class='product-card-info']/@href").extract()
        for prod_link in product_links:
            absolute_products_link =  'https://kith.com{}'.format(prod_link)
            yield scrapy.Request(url=absolute_products_link, callback=self.final_products_details)

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













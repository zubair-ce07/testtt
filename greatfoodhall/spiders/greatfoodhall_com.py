# -*- coding: utf-8 -*-

import re
import math
from scrapy.http.cookies import CookieJar
import scrapy
from greatfoodhall.items import GreatfoodhallItem


class GreatfoodhallComSpider(scrapy.Spider):
    name = 'greatfoodhall.com'
    start_urls = ['http://www.greatfoodhall.com/eshop/LoginPage.do']

    def parse(self, response):
        nav_links = response.xpath("//td/div[contains(@class, 'item')]/a/@href").extract()
        for i, link in enumerate(nav_links):
            yield scrapy.Request("http://www.greatfoodhall.com/eshop/LoginPage.do", self.go_to_products, meta={'product_link':link, 'cookiejar':i}, dont_filter=True)
    
    def go_to_products(self, response):
        yield scrapy.Request(response.urljoin(response.meta['product_link']), self.get_items, meta={'cookiejar':response.meta['cookiejar'], 'items' : 0})

    def get_items(self, response):
        product_description_links = response.xpath("//div[@class='productDisplayArea']/table//div[@class='productTmb']/a/@href").extract()
        for link in product_description_links:
            yield scrapy.Request(link, self.get_item_details, meta={'cookiejar': response.meta['cookiejar']})

        total_items = int(response.meta['items'])
        if total_items == 0:
            total_items = int(response.xpath("//b[@class='totalItem']/text()").extract_first())
        if total_items is not None:
            page = re.findall(r'curPage_1=[\d]+', response.url)
            last_page = math.ceil(total_items/9)
            if page:
                page = re.findall(r'=[\d]+', page[0])
                current_page = int(re.findall(r'[\d]+', page[0])[0])
            else:
                current_page = 1
        else:
            current_page = 1
            last_page = 0
        if current_page < last_page:
            current_page = current_page + 1
            link = "http://www.greatfoodhall.com/eshop/ShowProductPage.do?curPage_1="+str(current_page)
            yield scrapy.Request(link, self.get_items, meta={'cookiejar': response.meta['cookiejar'], 'items': total_items}, dont_filter=True)
        
        
    def get_item_details(self, response):
        item = GreatfoodhallItem()
        item['name'] = self.get_item_name(response)
        item['price'] = self.get_item_price(response)
        item['category'] = self.get_item_category(response)
        item['image_url'] = self.get_item_image_url(response)
        item['description'] = self.get_item_description(response)
        item['nutrition'] = self.get_item_nutrition(response)
        item['type_weight'] = self.get_item_type_weight(response)
        item['stock'] = self.get_item_stock_availability(response)
        item['url'] = response.url

        yield item
    
    def get_item_stock_availability(self, response):
        stock = response.xpath("//div[contains(@class, 'btnAddToCart')]/a").extract()
        if stock:
            return True
        else:
            return False

    def get_item_price(self, response):
        price = response.xpath("//div[@class='itemOrgPrice2']/text()").extract_first()
        if price is None:
            price = response.xpath("//div[contains(@class, 'newPrice')]/text()").extract_first()
        return price

    def get_item_category(self, response):
        return response.xpath("//ul[@class='clearFix']//a/text()").extract()[1].strip()

    def get_item_image_url(self, response):
        return response.xpath("//div[@class='productPhoto']/img/@src").extract_first()
    
    def get_item_description(self, response):
        return response.xpath("//div[@class='productPhoto']/img/@alt").extract_first()

    def get_item_nutrition(self, response):
        return response.xpath("//div[@id='nutrition']//td/text()").extract_first()
    
    def get_item_name(self, response):
        return response.xpath("//h1[@class='pL6']/text()").extract_first()

    def get_item_type_weight(self, response):
        return response.xpath("//span[contains(@class, 'ml')]/text()").extract_first()

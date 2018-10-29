# -*- coding: utf-8 -*-
import json
from parsel import Selector
import scrapy
from damart_crawling.items import DamartCrawlingItem


class DamartSpider(scrapy.Spider):
    name = 'damart'
    allowed_domains = ['damart.co.uk']
    start_urls = ['http://damart.co.uk/']

    def parse(self, response):
        all_links = response.xpath("//nav/ul//a/@href").extract()
        for url in all_links:
            if "C-" in url:
                yield scrapy.Request(response.urljoin(url+"/I-Page1_2000"), self.parse_items)

    def parse_items(self, response):
        item_detail_links = response.xpath("//div[@id='articleZone']//section[2]/ul//div[@class='k-product']/a/@href").extract()[::3]
        for url in item_detail_links:
            yield scrapy.Request(response.urljoin(url), self.parse_item_details)

    def parse_item_details(self, response):
        product = DamartCrawlingItem()
        product['category'], product['name'] = self.get_item_name_and_category(response)
        product['ref_code'] = self.get_item_ref_code(response)
        product['description'] = self.get_item_description(response)
        product['benefits'] = self.get_item_benefits(response)
        product['composition'] = self.get_item_composition(response)
        product['care'] = self.get_item_care(response)
        product['image_urls'] = self.get_item_image_urls(response)
        product['url'] = response.url
        product['colors'] = dict()
        color_urls = response.xpath("//ul[contains(@class, 'picto_color')]//a/@href").extract()
        meta_dict = {
            'color_urls': color_urls,
            'product': product,
        }
        header_dict = {
            'x-requested-with': "XMLHttpRequest",
        }
        yield scrapy.Request(color_urls[0], self.get_item_colors, meta=meta_dict, headers=header_dict, dont_filter=True)

    def get_item_colors(self, response):
        product = response.meta['product']
        color_urls = response.meta['color_urls']
        product_data = json.loads(response.text)
        product_dd_data = product_data['inits'][2]['initDDdSlickComponent']
        color_name = product_dd_data[0]['ddData'][0]['caracs']
        product['colors'][color_name.replace(' ', '')] = {
            'color': color_name,
            'price': self.get_item_price(product_data)[1:],
            'currency_code': self.get_item_price_code(product_data),
        }
        for ddData in product_dd_data:
            key  = "available_" + ddData['ddData'][0]['value']
            product['colors'][color_name.replace(' ', '')].update({key:[data['text'] for data in ddData['ddData']]})
        
        color_urls = color_urls[1:]
        if color_urls:
            meta_dict = {
                'color_urls': color_urls,
                'product': product,
            }
            header_dict = {
                'x-requested-with': "XMLHttpRequest",
            }
            yield scrapy.Request(color_urls[0], self.get_item_colors, meta=meta_dict, headers=header_dict, dont_filter=True)
        else:
            yield product

    def get_item_image_urls(self, response):
        return response.xpath("//div[@id='galleryZone']//ul/li//a/@href").extract()

    def get_item_name_and_category(self, response):
        temp = response.xpath("//div[contains(@class, 'breadcrum')]//span//text()").extract()
        return temp[-3], temp[-1]
    
    def get_item_price(self, product_data):
        priceZone = product_data['zones']['priceZone']
        priceZone = Selector(priceZone)
        if priceZone.xpath("//p[@class='price sale']").extract():
            temp = priceZone.xpath("//p[@class='price sale']//text()").extract()
        else:
            temp = priceZone.xpath("//p[contains(@class, 'price')]//text()").extract()
        return temp[0].strip()+temp[1]

    def get_item_price_code(self, product_data):
        priceZone = product_data['zones']['priceZone']
        priceZone = Selector(priceZone)
        return priceZone.xpath("//meta/@content").extract_first()

    def get_item_ref_code(self, response):
        return response.xpath("//span[@itemprop='productID']/text()").extract_first().strip()
    
    def get_item_description(self, response):
        return response.xpath("//div[@itemprop='description']/p//text()").extract_first().strip()

    def get_item_benefits(self, response):
        benefits = response.xpath("//div[@itemprop='description']/ul//text()").extract()
        return benefits[0:len(benefits)/2]

    def get_item_composition(self, response):
        careZone = response.xpath("//div[@id='careAdvicesZoneNew']//span/text()").extract()
        if "Composition" in careZone:
            if response.xpath("//div[@id='careAdvicesZoneNew']/ul[2]//div[@class='maintenance_txt']/text()").extract(): 
                return response.xpath("//div[@id='careAdvicesZoneNew']/ul[2]//div[@class='maintenance_txt']/text()").extract_first().strip()
            else:
                return response.xpath("//div[@id='careAdvicesZoneNew']/ul[1]//div[@class='maintenance_txt']/text()").extract_first().strip()
        else:
            return None;
    def get_item_care(self, response):
        careZone = response.xpath("//div[@id='careAdvicesZoneNew']//span/text()").extract()
        if "Care instructions" in careZone:
            return response.xpath("//div[@id='careAdvicesZoneNew']/ul[1]//li//div[contains(@style, 'font-family')]//text()").extract()[::2]
        else:
            return None
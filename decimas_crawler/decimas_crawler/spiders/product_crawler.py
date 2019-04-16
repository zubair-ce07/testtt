# -*- coding: utf-8 -*-
import scrapy
from ..items import DecimasCrawlerItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import json
import re

class ProductCrawlerSpider(scrapy.spiders.CrawlSpider):
    name = 'product_crawler'
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es']
    rules = [
            Rule(
            LinkExtractor(
                restrict_css = ".clever-mega-menu",
            ),
    
            callback = 'parse',
            follow = True,
        ),

        Rule(
            LinkExtractor(
                restrict_css = "li.product-item",
            ),
    
            callback = 'parse_item',
            follow=True,
        ),
    ]

    def parse_product(self, response):
        yield scrapy.Request(response.url, callback=self.parse_item)    
    
    def parse_item(self, response):
        previous_price = None
        skus =[]
        item = DecimasCrawlerItem()

        currency_conversion = {'€':"EUR", '$':"Dollar" }
        genders = ['MAN', 'WOMAN', 'BOY', 'GIRL', 'MAGAZINE', 'JUNIORA']
        
        brands = response.css('a.brand img::attr(title)').extract()
        objs = response.css("script[type='text/x-magento-init']::text").extract()
        
        json_object = json.loads(objs[10])
        data = json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]
        image_sources = data['images']
        
        currency = data['currencyFormat']
        currency = (currency.replace("%s",u' ')).strip()
        currency = currency_conversion[currency]
        
        for color in data['attributes']['93']['options']:
            for size in data['attributes']['154']['options']:
                for k in color['products']:
                    for t in size['products']:
                        if k==t:
                            skus.append(self.make_sku(data['optionPrices'][t]['finalPrice']['amount'], \
                            currency, color['label'], size['label'], k))
        
        all_image = self.img_source_extractor(image_sources, data['attributes']['93']['options'])
        print(f'***{all_image}')
        product_titile = response.css('div.attribute.name h1::text').extract_first()
    
        brand = self.brand_name_extractor(brands, product_titile)
        
        current_price = response.css('span.price::text').extract()
        current_price = [x.replace(u'\xa0€', u' ') for x in current_price if x]
        current_price = [float(x.replace(u',', u'.')) for x in current_price]
        if len(current_price) >= 2:
            current_price = min(current_price)
        product_description = response.css('div.value::text').extract_first()
        gender = self.gender_extractor(genders, product_titile)
        item['retailer_sku'] = response.css('div.price-box::attr(data-product-id)').extract_first()
        item['gender'] = gender
        item['brand'] = brand
        item['url'] = response.url
        item['retailer'] = "Decimas.es"
        item['name'] = product_titile
        item['description'] = product_description
        item['old_price'] = previous_price
        item['skus']=skus
        item['currency'] = currency
        item['final_price'] = current_price
       
        yield item

    def img_source_extractor(self, image_sources, products):
        all_images = []
        for color in products:
            for product in color['products']:
                for x in product:
                    print(f'****{image_sources[x]}')    
        return all_images    
    
    def make_sku(self, price, currency, color, size, sku_id):
        skus = {}
        skus['price'] = price
        skus['currency'] = currency
        skus['size'] = size
        skus['color'] = color
        skus['sku_id'] = sku_id
        
        return skus
    
    def brand_name_extractor(self, brand_names, product_name):
        for brand in brand_names:
            if brand.lower() in product_name.lower():
                return brand
        
    def gender_extractor(self, genders, product_name):
        for gender in genders:
            if gender in product_name:
                return gender
    
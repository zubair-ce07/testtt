# -*- coding: utf-8 -*-
from ..items import DecimasCrawlerItem
from ..mappings import Mapping
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import json


class ProductCrawlerSpider(scrapy.spiders.CrawlSpider):
    name = 'decimas_crawler'
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es']
    rules = (
        Rule(LinkExtractor(restrict_css=".clever-mega-menu"), callback='parse', follow=True),
        Rule(LinkExtractor(restrict_css="li.product-item"), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response): 
        item = DecimasCrawlerItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['gender'] = self.extract_gender(response)
        item['brand'] = self.extract_brand(response)
        item['url'] = self.extract_url(response)
        item['retailer'] = self.extract_retailer()
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['old_price'] = self.extract_old_price(response)
        item['img_urls'] = self.extract_img_urls(response)
        item['skus'] = self.extract_sku(response)
        item['currency'] = self.extract_currency(response)
        item['final_price'] = self.extract_final_price(response)
        yield item

    def extract_retailer_sku(self, response):
        return response.css('div.price-box::attr(data-product-id)').extract_first()
        
    def extract_gender(self, response):
        genders = ['MAN', 'WOMAN', 'BOY', 'GIRL', 'MAGAZINE', 'JUNIORA']
        product_name = response.css('div.attribute.name h1::text').extract_first()
        
        for gender in genders:
            if gender in product_name:
                return gender

    def extract_brand(self, response):
        brand_names = response.css('a.brand img::attr(title)').extract()
        product_name = response.css('div.attribute.name h1::text').extract_first()
        
        for brand in brand_names:
            if brand.lower() in product_name.lower():
                return brand
    
    def extract_url(self, response):
        return response.url
    
    def extract_retailer(self):
        return "Decimas.es"

    def extract_name(self, response):
        return response.css('div.attribute.name h1::text').extract_first()    
        
    def extract_description(self, response):
        return response.css('div.value::text').extract_first()

    def extract_old_price(self, response):
        previous_price = None 
        current_price = response.css('span.price::text').extract()
        current_price = [x.replace(u'\xa0€', u' ') for x in current_price if x]
        current_price = [float(x.replace(u',', u'.')) for x in current_price]
        if len(current_price) >= 2:
            previous_price = current_price.remove(min(current_price))         
        
        return previous_price
    
    def extract_img_urls(self, response):
        all_images = []
        script_text = response.css("script[type='text/x-magento-init']::text").extract()
        json_object = json.loads(script_text[10])
        image_sources = json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]['images']
        data = json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]

        for color in data['attributes']['93']['options']:
            for product in color['products']:
                product_images = image_sources[product]
                for product_image in product_images:
                    all_images.append(product_image['full'])       
        return all_images    
    
    def extract_sku(self, response):
        skus =[]
        script_text = response.css("script[type='text/x-magento-init']::text").extract()
        json_object = json.loads(script_text[10])
        data = json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]
        currency = data['currencyFormat']
        currency = (currency.replace("%s",u' ')).strip()
        currency = Mapping.currency_map[currency]
    
        for color in data['attributes']['93']['options']:
            for size in data['attributes']['154']['options']:
                for k in color['products']:
                    for t in size['products']:
                        if k==t:
                            skus.append(self.make_sku(data['optionPrices'][t]['finalPrice']['amount'], \
                            currency, color['label'], size['label'], k))
        return skus

    def extract_currency(self, response):
        script_text = response.css("script[type='text/x-magento-init']::text").extract()
        json_object = json.loads(script_text[10])
        data = json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]
        currency = data['currencyFormat']
        currency = (currency.replace("%s",u' ')).strip()
        return Mapping.currency_map[currency]
        

    def extract_final_price(self, response):
        current_price = response.css('span.price::text').extract()
        current_price = [x.replace(u'\xa0€', u' ') for x in current_price if x]
        current_price = [float(x.replace(u',', u'.')) for x in current_price]
        if len(current_price) >= 2:
            current_price = min(current_price)         
        return current_price
    
    def make_sku(self, price, currency, color, size, sku_id):
        skus = {}
        skus['price'] = price
        skus['currency'] = currency
        skus['size'] = size
        skus['color'] = color
        skus['sku_id'] = sku_id
        return skus

# -*- coding: utf-8 -*-
import scrapy
import json
import re

from items import GoSportItem


class GoSportSpider(scrapy.Spider):
    name = 'go-sport'
    allowed_domains = ['go-sport.pl']
    start_urls = ['https://www.go-sport.pl/']

    download_delay = 1

    genders = {'Mężczyzna': "Man", 'Kobieta': "Woman",
               'Dziewczynka': "Girl", 'Chłopiec': "Boy",
               'Dla dzieci': "Children"}

    def parse(self, response):
        category_links = response.css('.level-top::attr(href)').extract()  
        yield from (response.follow(l, self.parse_products) for l in category_links)

    def parse_products(self, response):
        item_links =  response.css(".product-item h2 > a::attr(href)").extract()
        yield from (response.follow(l, self.parse_item) for l in item_links)

        next_page = response.css(".next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_products)
        
    def parse_item(self, response):
        item = GoSportItem()

        item['url'] = response.url
        item['retailer_sku'] = self._get_retailer_sku(response)
        item['gender'] = self._get_gender(response)
        item['category'] = self._get_category(response)
        item['brand'] = self._get_brand(response)
        item['name'] = self._get_name(response)
        item["description"] = self._get_description(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = self._get_skus(response)

        return item

    def _get_retailer_sku(self, response):
        return response.css('.product_id::text').extract_first()

    def _get_gender(self, response):
        gender = response.xpath('//span[contains(., "gender")]/text()').extract_first().split(":")[-1]
        
        return self.genders.get(gender, "No")
    
    def _get_category(self, response):
        return response.css('.category::text').extract_first().split('/')[1:]
    
    def _get_brand(self, response):
        return response.css('.brand::text').extract_first()
    
    def _get_name(self, response):
        return response.css('.name::text').extract_first()
    
    def _get_description(self, response):
        descriptions = response.css('div.description').xpath('descendant-or-self::*/text()').extract()    

        return [self.clean_text(d) for d in descriptions if len(d.strip()) > 1]
    
    def _get_image_urls(self, response):
        return response.css('.alternate_image_url::text').extract()

    def _get_skus(self, response):      
        item = {}
        item['color'] = response.css('.color_web::text').extract_first()
        item['price'] = response.css('.price::text').extract_first()
        item['currency'] = response.css('.price_currency_code::text').extract_first()
        item['previous_price'] = response.css('.list_price::text').extract_first()

        skus_selector = response.css('.nosto_sku')

        if not skus_selector:
            item['size'] = "Single Size"
            item['id'] = response.css('.product_id::text').extract_first()

            return [item]

        skus_in_stock = self._get_skus_in_stock(response)

        skus = []
        for sku in skus_selector:
            sku_item = item.copy()
            sku_item['size'] = sku.css('.size::text').extract_first()
            sku_item['id'] = sku.css('.id::text').extract_first()

            if sku_item['id'] not in skus_in_stock:
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus

    def _get_skus_in_stock(self, response):
        xpath = '//script[contains(., "Magento_Swatches/js/swatch-renderer-custom")]/text()'
        raw_product = response.xpath(xpath).extract_first()
        raw_product = json.loads(raw_product)

        return  raw_product["[data-role=swatch-options]"]\
                           ["Magento_Swatches/js/swatch-renderer-custom"]\
                           ["jsonConfig"]["optionPrices"]

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)

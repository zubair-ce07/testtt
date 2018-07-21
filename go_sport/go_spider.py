# -*- coding: utf-8 -*-
import scrapy
import json
import re

from items import GoSportItem


class GoSportSpider(scrapy.Spider):
    name = 'go-sport'
    allowed_domains = ['go-sport.pl']
    start_urls = ['https://www.go-sport.pl/']

    download_delay = 0.2

    genders = {'Mężczyzna': "Man", 'Kobieta': "Woman",
               'Dziewczynka': "Girl", 'Chłopiec': "Boy",
               'Dla dzieci': "Children"}

    def parse(self, response):
        category_links = response.css('a.level-top::attr(href)').extract()
        
        yield from (response.follow(l, self.parse_products) for l in category_links)

    def parse_products(self, response):
        item_links =  response.css("div.product-item h2 > a::attr(href)").extract()

        yield from (response.follow(l, self.parse_item) for l in item_links)
        
        next_page = response.css("a.action.next::attr(href)").extract_first()
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
        return response.css('span.product_id::text').extract_first()

    def _get_gender(self, response):
        gender = response.xpath('//span[contains(., "gender")]/text()').extract_first().split(":")[-1]
        
        return self.genders.get(gender, "No")
    
    def _get_category(self, response):
        return response.css('span.category::text').extract_first().split('/')[1:]
    
    def _get_brand(self, response):
        return response.css('span.brand::text').extract_first()
    
    def _get_name(self, response):
        return response.css('span.nosto_product span.name::text').extract_first()
    
    def _get_description(self, response):
        descriptions = response.css('div.description').xpath('descendant-or-self::*/text()').extract()    

        return list(self.clean_text(d) for d in descriptions if len(d.strip()) > 1)
    
    def _get_image_urls(self, response):
        return response.css('span.alternate_image_url::text').extract()

    def _get_skus(self, response):
        color, price, currency, previous_price = self._get_sku_static_attrs(response)
        
        item = {}
        item['color'] = color
        item['price'] = price
        item['currency'] = currency
        item['previous_price'] = previous_price

        skus_selector = response.css('span.nosto_sku')

        if not skus_selector:
            item['size'] = "Single Size"
            item['id'] = response.css('span.product_id::text').extract_first()

            return [item]

        skus_in_stock = self._get_skus_in_stock(response)

        skus = []
        for sku in skus_selector:
            sku_item = item.copy()
            sku_item['size'] = sku.css('span.size::text').extract_first()
            sku_item['id'] = sku.css('span.id::text').extract_first()

            if sku_item['id'] not in skus_in_stock:
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus

    def _get_sku_static_attrs(self, response):
        color = response.css('span.color_web::text').extract_first()
        price = response.css('span.price::text').extract_first()
        currency = response.css('span.price_currency_code::text').extract_first()
        previous_price = response.css('span.list_price::text').extract_first()

        return color, price, currency, previous_price

    def _get_skus_in_stock(self, response):
        megento_json = response.xpath('//script[contains\
                       (., "Magento_Swatches/js/swatch-renderer-custom")]/text()').extract_first()
        megento_json = json.loads(megento_json)

        return  megento_json["[data-role=swatch-options]"]\
                                    ["Magento_Swatches/js/swatch-renderer-custom"]\
                                    ["jsonConfig"]["optionPrices"]

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)

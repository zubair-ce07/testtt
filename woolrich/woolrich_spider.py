# -*- coding: utf-8 -*-
import scrapy
import re

from urllib.parse import urljoin

from items import WoolrichItem


class WoolrichSpider(scrapy.Spider):
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/details/men-s-arctic-parka-detachable-fur-john-rich-bros/_/R-WO1674',
                'http://www.woolrich.com/woolrich/details/shady-cove-stripe-100-soft-wool-blanket-54-x70/_/R-990214',
                'http://www.woolrich.com/woolrich/details/women-s-bell-canyon-embroidered-t-shirt-100-organic-cotton/_/R-7059']

    def parse(self, response):

        item = WoolrichItem()
        item['retailer_sku'] = self._get_retailer_sku(response)
        item['gender'] = self._get_gender(response)
        item['category'] = self._get_category(response)
        item['brand'] = self._get_brand(response)
        item['url'] = response.url
        item['name'] = self._get_name(response)
        item["description"] = self._get_description(response)
        item['care'] = self._get_care(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = self._get_skus(response)

        yield item
    
    def _get_retailer_sku(self, response):
        return response.css('[itemprop="productID"]::text').extract_first()

    def _get_gender(self, response):
        genders = ['Men', 'Women']
        prod_name = self._get_name(response)
        for gender in genders:
            if gender in prod_name:
                return gender       
    
    def _get_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]
    
    def _get_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').extract_first()
    
    def _get_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()
    
    def _get_description(self, response):
        description = response.css('[itemprop="description"]::text').extract()
        return [self.clean_text(d) for d in description]

    def _get_care(self, response):
        care = response.css('.span4 .text li::text').extract()
        return [self.clean_text(c) for c in care]
    
    def _get_image_urls(self, response):
        img_links = response.css('.zoom .product-image-link img::attr(src)').extract()
        return [urljoin(response.url, l) for l in img_links]

    def _get_skus(self, response):
        item = {}
        item['color'] = self._extract_color(response)
        item['price'] = self._extract_price(response)
        item['currency'] = self._extract_currency(response)
        previous_price = self._extract_prev_price(response)

        if previous_price:
            item['previous price'] = previous_price

        sizes = response.css('.sizelist li a::attr(title)').extract()
        size_ids = response.css('.sizelist li a::attr(id)').extract()
        stock_levels = response.css('.sizelist li a::attr(stocklevel)').extract()

        skus = []
        for size, size_id, stock_level in zip(sizes, size_ids, stock_levels):
            sku_item = item.copy()
            sku_item['size'] = size
            sku_item['id'] = size_id

            if stock_level == '0':
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        return skus
    
    def _extract_color(self, response):
        return response.css('.colorName::text').extract_first().strip()
    
    def _extract_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def _extract_price(self, response):
        return response.css('[itemprop="price"]::attr(content)').extract_first()

    def _extract_prev_price(self, response):
        previous_price = response.css('#productDetails .strikethrough::text').extract_first()

        if previous_price:
            return previous_price.strip().split(',')[-1]

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)

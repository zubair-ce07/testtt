# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from urllib.parse import urljoin

from items import WoolrichItem


class WoolrichSpider(CrawlSpider):
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com/mens-oxbow-bend-plaid-flannel-shirt-100-cotton-6111/',
    			  'https://www.woolrich.com/mens-arctic-parka-tone-on-tone-john-rich-bros-wf1024/']

    download_delay = 0.2

    request_url = 'http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp'
    genders = ['Men', 'Women']

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
        item['skus'] = []
        return item
    
    def _get_retailer_sku(self, response):
        return response.css('[name="product_id"]::attr(value)').extract_first()

    def _get_gender(self, response):
        prod_name = self._get_name(response)

        for gender in self.genders:
            if gender in prod_name:
                return gender

        return 'unisex-adults'   
    
    def _get_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]
    
    def _get_brand(self, response):
    	item_name = self._get_name(response)
    	brand = 'John Rich & Bros'
    	return brand if brand in item_name else 'Woolrich'
    
    def _get_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()
    
    def _get_description(self, response):
        description = response.css('#details-content::text').extract()
        return [self.clean_text(d) for d in description]

    def _get_care(self, response):
        care = response.css('#features-content').xpath('descendant-or-self::*/text()').extract()
        return [self.clean_text(c) for c in care if len(c.strip()) > 1]
    
    def _get_image_urls(self, response):
        return [set(response.css('.productView-image img::attr(src)').extract())]

    # def _get_skus(self, response):
    #     raw_item = self._extract_sku_pricing(response)
    #     raw_item['color'] = self._extract_color(response)

    #     sizes = response.css('.sizelist li a::attr(title)').extract()
    #     size_ids = response.css('.sizelist li a::attr(id)').extract()
    #     stock_levels = response.css('.sizelist li a::attr(stocklevel)').extract()

    #     skus = []
    #     for size, size_id, stock_level in zip(sizes, size_ids, stock_levels):
    #         sku_item = raw_item.copy()
    #         sku_item['size'] = size
    #         sku_item['id'] = size_id

    #         if stock_level == '0':
    #             sku_item['out_of_stock'] = True

    #         skus.append(sku_item)

    #     if len(skus) == 1:
    #         skus[0]['size'] = 'ONE-SIZE'
    #     return skus

    # def _extract_sku_pricing(self, response):
    #     return {
    #         'price': self._extract_price(response),
    #         'previous price': self._extract_prev_price(response),
    #         'currency': self._extract_currency(response)
    #     }
    
    # def _extract_color(self, response):
    #     return response.css('.colorName::text').extract_first().strip()
    
    # def _extract_currency(self, response):
    #     return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    # def _extract_price(self, response):
    #     return response.css('[itemprop="price"]::attr(content)').extract_first()

    # def _extract_prev_price(self, response):
    #     previous_price = response.css('.strikethrough::text').extract_first()

    #     if previous_price:
    #         return self.clean_text(previous_price).split()[-1]

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)

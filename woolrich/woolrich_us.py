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

    listing_css = ['#primary', '.pagination-item--next']
    rules = (
                Rule(LinkExtractor(restrict_css=listing_css), follow=True),
                Rule(LinkExtractor(restrict_css=('.card-title')), callback='parse_item'),
            )

    def parse_item(self, response):
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

    def _get_skus(self, response):
        pass

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)

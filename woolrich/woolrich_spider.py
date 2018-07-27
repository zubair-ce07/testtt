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
    start_urls = ['http://www.woolrich.com/woolrich/?countryCode=CA']

    download_delay = 0.5

    request_url = 'http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp'
    genders = ['Men', 'Women', 'Unisex-Adults']

    listing_css = ['.nav.navbar-nav .upper', '.clear.addMore']
    rules = (
                Rule(LinkExtractor(restrict_css=listing_css, tags=('a', 'div'), attrs=('href', 'nextpage'))),
                Rule(LinkExtractor(restrict_css=('.productCard')), callback='parse_item')
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
        item['skus']=[]

        color_ids = response.css('.colorlist .link img::attr(colorid)').extract()
        return self._process_colors(item, color_ids)
    
    def _process_colors(self, item, color_ids):
        if color_ids:
            formdata = {
                        'productId': item['retailer_sku'], 
                        'colorId': color_ids.pop()
                        }
            return FormRequest(url=self.request_url, callback=self._get_color_skus,\
                              formdata=formdata, meta = {'item': item, 'color_ids': color_ids})
        return item

    def _get_color_skus(self, response):
        item = response.meta.get('item')
        color_ids = response.meta.get('color_ids')

        item['skus'] += self._get_skus(response)

        return self._process_colors(item, color_ids)
    
    def _get_retailer_sku(self, response):
        return response.css('[itemprop="productID"]::text').extract_first().strip()

    def _get_gender(self, response):
        prod_name = self._get_name(response)

        for gender in self.genders:
            if gender in prod_name:
                return gender

        return self.genders[-1]   
    
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
        raw_item = self._extract_sku_pricing(response)
        raw_item['color'] = self._extract_color(response)

        sizes = response.css('.sizelist li a::attr(title)').extract()
        size_ids = response.css('.sizelist li a::attr(id)').extract()
        stock_levels = response.css('.sizelist li a::attr(stocklevel)').extract()

        skus = []
        for size, size_id, stock_level in zip(sizes, size_ids, stock_levels):
            sku_item = raw_item.copy()
            sku_item['size'] = size
            sku_item['id'] = size_id

            if stock_level == '0':
                sku_item['out_of_stock'] = True

            skus.append(sku_item)

        if len(skus) == 1:
            skus[0]['size'] = 'ONE-SIZE'
        return skus

    def _extract_sku_pricing(self, response):
        return {
            'price': self._extract_price(response),
            'previous price': self._extract_prev_price(response),
            'currency': self._extract_currency(response)
        }
    
    def _extract_color(self, response):
        return response.css('.colorName::text').extract_first().strip()
    
    def _extract_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def _extract_price(self, response):
        return response.css('[itemprop="price"]::attr(content)').extract_first()

    def _extract_prev_price(self, response):
        previous_price = response.css('.strikethrough::text').extract_first()

        if previous_price:
            return self.clean_text(previous_price).split()[-1]

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)

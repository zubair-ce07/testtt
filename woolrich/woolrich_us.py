# -*- coding: utf-8 -*-
import json
import re
from urllib.parse import parse_qsl, urljoin

import scrapy
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import WoolrichItem


class WoolrichSpider(CrawlSpider):
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com']

    custom_settings = {'DOWNLOAD_DELAY': 0.5, 'HTTPCACHE_ENABLED': True}

    request_api_url = 'https://www.woolrich.com/remote/v1/product-attributes/{}'
    genders = ['Men', 'Women']

    listing_css = ['#primary', '.pagination-item--next']
    rules = (
                Rule(LinkExtractor(restrict_css=listing_css), follow=True),
                Rule(LinkExtractor(restrict_css=('.card-title')), callback='parse_item'),
            )

    def parse_item(self, response):
        item = WoolrichItem()
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = self.get_gender(response)
        item['category'] = self.get_category(response)
        item['brand'] = self.get_brand(response)
        item['url'] = response.url
        item['name'] = self.get_name(response)
        item["description"] = self.get_description(response)
        item['care'] = self.get_care(response)
        item['image_urls'] = self.get_image_urls(response)
        item['skus'] = []

        item['meta'] = {'queued_requests': self.color_requests(response, item['retailer_sku'])}
        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if item['meta']['queued_requests']:
            req = item['meta']['queued_requests'].pop()
            req.meta['item'] = item
            return req

        del item['meta']
        return item

    def color_requests(self, response, product_id):
        attributes_map = self.get_product_attrs(response)

        color_map = attributes_map.pop('color')
        attr_value = color_map.get('value')

        formdata = {'action': 'add', 'product_id': product_id}
        color_reqs = []
        for color, color_id in color_map['varients']:
            formdata[attr_value] = color_id
            
            raw_sku = {'color': color, 'currency': attributes_map.get('currency')}
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            url = self.request_api_url.format(product_id)

            request = FormRequest(url=url, meta=meta, formdata=formdata, 
                            callback=self.parse_color)
            color_reqs += [request]
        
        return color_reqs

    def parse_color(self, response):
        item = response.meta.get('item')

        size_reqs = self.size_requests(response)
        if not size_reqs:
            item['skus'].append(self.make_sku(response))
            
        item['meta']['queued_requests'] += size_reqs
        return self.next_request_or_item(item)
    
    def size_requests(self, response):
        attributes_map = response.meta.get('attributes_map')
        sku_common = response.meta.get('raw_sku')

        raw_item = json.loads(response.text)['data']
        in_stock_attributes = raw_item['in_stock_attributes']

        size_map = attributes_map.get('size', {})
        attr_value = size_map.get('value')
        size_reqs = []
        for size, size_id in size_map.get('varients', []):
            if int(size_id) not in in_stock_attributes:
                continue

            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata[attr_value] = size_id

            raw_sku = sku_common.copy()
            raw_sku['size'] = size
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            request = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_size)
            size_reqs += [request]
        
        return size_reqs

    def parse_size(self, response):
        item = response.meta.get('item')

        fit_requests = self.fitting_requests(response)
        if not fit_requests:
            item['skus'].append(self.make_sku(response))
            
        item['meta']['queued_requests'] += fit_requests
        return self.next_request_or_item(item)
    
    def fitting_requests(self, response):
        attributes_map = response.meta.get('attributes_map')
        sku_common = response.meta.get('raw_sku')

        raw_item = json.loads(response.text)['data']
        in_stock_attributes = raw_item['in_stock_attributes']

        fit_map = attributes_map.get('fit', {})
        attr_value = fit_map.get('value')
        fitting_reqs = []
        for fit, fit_id in fit_map.get('varients', []):
            if int(fit_id) not in in_stock_attributes:
                continue

            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata[attr_value] = fit_id

            raw_sku = sku_common.copy()
            raw_sku['size'] = f'{raw_sku["size"]}/{fit}'
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            request = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_fitting)
            fitting_reqs += [request]
        
        return fitting_reqs
    
    def parse_fitting(self, response):
        item = response.meta.get('item')

        item['skus'].append(self.make_sku(response))
        return self.next_request_or_item(item)
    
    def make_sku(self, response):
        sku = response.meta.get('raw_sku')
        raw_item = json.loads(response.text)['data']
        prev_price, price = self.sku_pricing(raw_item)

        sku['id'] = raw_item['sku']
        sku['price'] = price

        if prev_price:
            sku['previous_price'] = prev_price
        
        sku['size'] = sku.get('size', 'One Size')        
        return sku

    def sku_pricing(self, raw_sku):
        price = self.to_cent(raw_sku['price']['without_tax']['value'])
        prev_price = raw_sku['price'].get('non_sale_price_without_tax', {}).get('value')
        if prev_price:
            prev_price = self.to_cent(prev_price)

        return prev_price, price


    def get_retailer_sku(self, response):
        return response.css('[name="product_id"]::attr(value)').extract_first()

    def get_gender(self, response):
        prod_name = self.get_name(response)

        for gender in self.genders:
            if gender in prod_name:
                return gender

        return 'unisex-adults'   
    
    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]
    
    def get_brand(self, response):
    	item_name = self.get_name(response)
    	brand = 'John Rich & Bros'
    	return brand if brand in item_name else 'Woolrich'
    
    def get_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()
    
    def get_description(self, response):
        description = response.css('#details-content::text').extract()
        return [self.clean_text(d) for d in description]

    def get_care(self, response):
        care = response.css('#features-content').xpath('descendant-or-self::*/text()').extract()
        return [self.clean_text(c) for c in care if len(c.strip()) > 1]
    
    def get_image_urls(self, response):
        raw_script = response.css('[data-sku]::attr(data-images)').extract_first()
        image_urls = json.loads(raw_script)
        
        return [u['data'].replace('{:size}', '1200x1318') for u in image_urls if not "thumbnail" in u['alt']]

    def get_product_attrs(self, response):
        product_attrs_sel = response.css('.productView-options [data-product-attribute]')
        attr_name_r = re.compile('color|size|fit', flags=re.I)

        attributes_map = {}
        for attr_sel in product_attrs_sel:
            attr_name = attr_sel.css('.form-label span::text').re_first(attr_name_r).lower()

            attributes_map[attr_name] = {}
            attributes_map[attr_name]['value'] = attr_sel.css('.form-radio::attr(name)').extract_first()

            attr_titles_css = '.form-option-variant::attr(title), .form-option-variant::text'
            attr_titles = attr_sel.css(attr_titles_css).extract()
            attr_titles_ids = attr_sel.css('.form-radio::attr(value)').extract()

            attributes_map[attr_name]['varients'] = list(zip(attr_titles, attr_titles_ids))

        currency_css = '[itemprop="priceCurrency"]::attr(content)'
        attributes_map['currency'] = response.css(currency_css).extract_first()
        return attributes_map

    def to_cent(self, price):
        return round(price*100)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)

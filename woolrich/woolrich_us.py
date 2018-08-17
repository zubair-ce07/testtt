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

    request_url = 'https://www.woolrich.com/remote/v1/product-attributes/{}'
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

        item['meta'] = {'queued_requests': self.color_requests(response, item['retailer_sku'])}
        return self.next_request(item)

    def next_request(self, item):
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
            url = self.request_url.format(product_id)

            req = FormRequest(url=url, meta=meta, formdata=formdata, 
                            callback=self.parse_color)
            color_reqs.append(req)
        
        return color_reqs

    def parse_color(self, response):
        item = response.meta.get('item')
        attributes_map = response.meta.get('attributes_map')
        raw_sku = response.meta.get('raw_sku')

        size_reqs = self.size_requests(response, attributes_map, raw_sku)
        if not size_reqs:
            raw_sku['size'] = 'One size'
            item['skus'].append(self.make_sku(response, raw_sku))
            
        item['meta']['queued_requests'] += size_reqs
        return self.next_request(item)
    
    def size_requests(self, response, attributes_map, sku_common):
        sku_details = json.loads(response.text)['data']
        in_stock_attributes = sku_details['in_stock_attributes']

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
            req = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_size)
            size_reqs.append(req)
        
        return size_reqs

    def parse_size(self, response):
        item = response.meta.get('item')
        attributes_map = response.meta.get('attributes_map')
        raw_sku = response.meta.get('raw_sku')

        fit_requests = self.fitting_requests(response, attributes_map, raw_sku)
        if not fit_requests:
            item['skus'].append(self.make_sku(response, raw_sku))
            
        item['meta']['queued_requests'] += fit_requests
        return self.next_request(item)
    
    def fitting_requests(self, response, attributes_map, sku_common):
        sku_details = json.loads(response.text)['data']
        in_stock_attributes = sku_details['in_stock_attributes']

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
            req = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_fitting)
            fitting_reqs.append(req)
        
        return fitting_reqs
    
    def parse_fitting(self, response):
        item = response.meta.get('item')
        raw_sku = response.meta.get('raw_sku')

        item['skus'].append(self.make_sku(response, raw_sku))
        return self.next_request(item)
    
    def make_sku(self, response, sku):
        sku_details = json.loads(response.text)['data']
        pprice, price = self.sku_pricing(sku_details)

        sku['id'] = sku_details['sku']
        sku['price'] = price

        if pprice:
            sku['previous_price'] = pprice
        
        return sku

    def sku_pricing(self, raw_sku):
        price = self.to_cent(raw_sku['price']['without_tax']['value'])
        pprice = raw_sku['price'].get('non_sale_price_without_tax', {}).get('value')
        if pprice:
            pprice = self.to_cent(pprice)

        return pprice, price


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
        raw_script = response.css('[data-sku]::attr(data-images)').extract_first()
        image_urls = json.loads(raw_script)
        
        return [u['data'].replace('{:size}', '1200x1318') for u in image_urls if not "thumbnail" in u['alt']]

    def get_product_attrs(self, response):
        product_attrs_sel = response.css('.productView-options [data-product-attribute]')

        attributes_map = {}
        for attr_sel in product_attrs_sel:
            attr_name = attr_sel.css('.form-label span::text').extract()[1].lower()

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

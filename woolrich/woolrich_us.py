# -*- coding: utf-8 -*-
import scrapy
import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from urllib.parse import urljoin

from items import WoolrichItem


class WoolrichSpider(CrawlSpider):
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = [
        'https://www.woolrich.com/woolrich-x-the-hill-side-backpack-bag-4139/',
        'https://www.woolrich.com/mens-cotton-check-shirt-john-rich-bros-ws6009/',
        ]

    custom_settings = {'DOWNLOAD_DELAY': 0.2, 'HTTPCACHE_ENABLED': True}

    genders = ['Men', 'Women']
    currency = 'USD'

    # listing_css = ['#primary', '.pagination-item--next']
    # rules = (
    #             Rule(LinkExtractor(restrict_css=listing_css), follow=True),
    #             Rule(LinkExtractor(restrict_css=('.card-title')), callback='parse_item'),
    #         )

    def parse(self, response):
        self.currency = response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

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

        item['meta'] = {'queued_reqs': self._get_color_skus_req(response)}
        return self.next_request(item)

    def next_request(self, item):
        if item['meta']['queued_reqs']:
            req = item['meta']['queued_reqs'].pop()
            req.meta['item'] = item
            return req

        del item['meta']
        return item
    
    def _extract_sku(self, response):
        item = response.meta.get('item')
        sku_item = response.meta.get('raw_sku')

        sku_details = json.loads(response.text)['data']
        sku_item['id'] = sku_details['sku']
        sku_item['price'] = sku_details['price']['without_tax']['value']

        if sku_details['price'].get('non_sale_price_without_tax'):
            sku_item['previous price'] = sku_details['price']['non_sale_price_without_tax']['value']

        if not sku_details['instock']:
            sku_item['out_of_stock'] = True

        item['skus'].append(sku_item)
        return self.next_request(item)

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

    def _get_color_skus_req(self, response):
        color_key = self.get_attr_key(response, 0)

        colors_css = '.productView-options .form-option-swatch span::attr(title)'
        color_ids_css = '.productView-options .form-option-swatch::attr(data-product-attribute-value)'
        colors = response.css(colors_css).extract()
        colors_ids = response.css(color_ids_css).extract()

        color_requests = []
        for color, color_id in zip(colors, colors_ids):
            formdata = {color_key: color_id}
            color_requests += self._get_size_skus_req(response, color, formdata)
        
        return color_requests

    def _get_size_skus_req(self, response, color, formdata):
        size_key = self.get_attr_key(response, 1)

        size_ids = response.css(f'[name="{size_key}"]::attr(value)').extract()
        if not size_ids:
            return [self._make_raw_sku(response, color, ['ONE-SIZE'], formdata)]

        size_requests = []
        for size_id in size_ids:
            formdata[size_key] = size_id

            size_css = f'[for="attribute_{size_id}"] span::text'
            size = response.css(size_css).extract_first()
            size_requests += self._get_fitting_skus_req(response, color, size, formdata)
        
        return size_requests
    
    def _get_fitting_skus_req(self, response, color, raw_size, formdata):
        fit_key = self.get_attr_key(response, 2)

        fit_ids = response.css(f'[name="{fit_key}"]::attr(value)').extract()
        if not fit_ids:
            return [self._make_raw_sku(response, color, [raw_size], formdata)]

        fit_requests = []
        for fit_id in fit_ids:
            formdata[fit_key] = fit_id

            fit_css = f'[for="attribute_{fit_id}"] span::text'
            size = [raw_size, response.css(fit_css).extract_first()]
            request = self._make_raw_sku(response, color, size, formdata)
            fit_requests.append(request)
        
        return fit_requests
    
    def _make_raw_sku(self, response, color, size, formdata):
        raw_sku = {'color': color}
        raw_sku['currency'] = self.currency
        raw_sku['size'] = '/'.join(size)

        return self._make_sku_request(response, raw_sku, formdata)     
    
    def _make_sku_request(self, response, raw_sku, formdata):
        product_id = self._get_retailer_sku(response)
        formdata['action'] = 'add'
        formdata['product_id'] = product_id
        request_url = f'https://www.woolrich.com/remote/v1/product-attributes/{product_id}'

        return FormRequest(url=request_url, formdata=formdata, 
                           callback=self._extract_sku, meta={'raw_sku': raw_sku})

    def get_attr_key(self, response, attr_type):
        attr_value = int(response.css('.form-option-swatch::attr(data-swatch-id)').extract_first())
        return f'attribute[{attr_value + attr_type}]'

    def clean_text(self, text):
            return re.sub(r'\s+', ' ', text)

# -*- coding: utf-8 -*-
import json
import re

import demjson
import scrapy

from items import GapItem


class GapParser:
    gender_map = [('女孩', 'girl'),
                  ('男装', 'men'),
                  ('女装', 'women'),
                  ('男孩', 'boy'),
                  ('孕妇装', 'women'),
                  ('幼儿', 'children'),
                  ('婴儿', 'baby')]
    care_words = ['洗', '棉', '干', '熨', '聚酯', '面料', '纤', '%']

    def _parse_item(self, response):
        raw_item = self._extract_raw_product(response)

        item = GapItem()
        item['retailer_sku'] = raw_item['identifier']
        item['category'] = raw_item['category']
        item['brand'] = raw_item['brand']
        item['name'] = raw_item['fn']
        item['url'] = response.url
        item['gender'] = self._get_gender(raw_item['category'])
        item['care'] = self._get_care(response)
        item["description"] = self._get_description(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = self._get_skus(response, raw_item['currency'])

        return self._stock_status_request(response, item)

    def _parse_stock_status(self, response):
        item = response.meta.get('item')
        stock = json.loads(response.text)

        item['skus'] = self._update_skus_status(stock, item['skus'])
        return item

    def _stock_status_request(self, response, item):
        url = f'https://www.gap.cn/catalog/product/getstock?entityId={item["retailer_sku"]}'
        return scrapy.Request(url=url, callback=self._parse_stock_status, meta={'item': item})
    
    def _update_skus_status(self, stock, skus):
        for sku in skus:
            if not stock[sku['id']]:
                sku['out_of_stock'] = True

        return skus

    def _get_gender(self, categories):
        for token, gender in self.gender_map:
            if token in categories:
                return gender
        return 'unisex-adults'

    def _get_care(self, response):
        css = '.pdp-mainImg td::text, #materialFeatures td::text'
        raw_care = response.css(css).extract()
        return [self._clean_text(care) for care in raw_care if self._is_care(care)]
    
    def _get_description(self, response):
        description = response.css('#short_description').xpath(
            'descendant-or-self::*/text()').extract()
        css = '.pdp-mainImg td::text, #materialFeatures td::text'
        raw_description = response.css(css).extract()

        description += [desc for desc in raw_description if not self._is_care(desc)]
        return [self._clean_text(d) for d in description if len(d.strip()) > 1]

    def _get_image_urls(self, response):
        return response.css('.more-views a::attr(href)').extract()

    def _get_skus(self, response, currency):
        skus = []

        colors = response.css('.onelist a::attr(title)').extract()
        color_ids = response.css('.onelist a::attr(key)').extract()
        for color, color_id in zip(colors, color_ids):
            css = f'.size_list_{color_id} a'
            sizes_selectors = response.css(css)

            for sel in sizes_selectors:
                sku = {
                    'currency': currency,
                    'price': self._get_price(sel),
                    'previous_price': self._get_previous_price(sel),
                    'color': color,
                    'size': sel.css('::attr(data-title)').extract_first(),
                    'id': sel.css('::attr(data-id)').extract_first()
                }

                skus += [sku]
        
        return skus

    def _get_price(self, selector):
        price = float(selector.css('::attr(data-final_price)').extract_first())
        return self._to_cent(price)
    
    def _get_previous_price(self, selector):
        previous_price = float(selector.css('::attr(data-price)').extract_first())
        return self._to_cent(previous_price)

    def _extract_raw_product(self, response):
        xpath = '//script[contains(., "var product = {")]/text()'
        script = response.xpath(xpath).extract_first()
        raw_item = re.findall(r"({.*?})", self._clean_text(script))[0]
        return demjson.decode(raw_item)

    def _is_care(self, care_text):
        return any(word in care_text for word in self.care_words)

    def _to_cent(self, price):
        return round(price*100)

    def _clean_text(self, text):
        return re.sub(r'\s+', ' ', text.strip())

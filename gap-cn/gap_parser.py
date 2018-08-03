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
    currency = 'CNY'

    def parse_item(self, response):
        raw_item = self._extract_raw_product(response)
        self.currency = raw_item['currency']

        item = GapItem()
        item['retailer_sku'] = raw_item['identifier']
        item['category'] = raw_item['category']
        item['brand'] = raw_item['brand']
        item['name'] = raw_item['fn']
        item['url'] = response.url
        item['gender'] = self._get_gender(raw_item['category'])
        item["description"] = self._get_description(response)
        item['care'] = self._get_care(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = self._get_skus(response)

        url = 'https://www.gap.cn/catalog/product/getstock?entityId=' + item['retailer_sku']
        return scrapy.Request(url=url, callback=self._skus_availability, meta={'item': item})

    def _skus_availability(self, response):
        item = response.meta.get('item')
        stocks = json.loads(response.text)
        for sku in item['skus']:
            if not stocks[sku['id']]:
                sku['out_of_stock'] = True
        return item

    def _get_gender(self, categories):
        for text, gender in self.gender_map:
            if text in categories:
                return gender
        return 'unisex-adults'

    def _get_description(self, response):
        description = response.css('#short_description').xpath(
            'descendant-or-self::*/text()').extract()
        return [self.clean_text(d) for d in description if len(d.strip()) > 1]

    def _get_care(self, response):
        css = '.pdp-mainImg td::text, #materialFeatures td::text'
        cares = response.css(css).extract()

        def is_care(c): return any(word in c for word in self.care_words)
        return [self.clean_text(care) for care in cares if is_care(care)]

    def _get_image_urls(self, response):
        return response.css('.more-views a::attr(href)').extract()

    def _get_skus(self, response):
        colors = response.css('.onelist a::attr(title)').extract()
        color_ids = response.css('.onelist a::attr(key)').extract()
        skus = []
        for color, color_id in zip(colors, color_ids):
            skus += self._get_color_skus(response, color, color_id)
        return skus

    def _get_color_skus(self, response, color, color_id):
        css = '.size_list_{} a'.format(color_id)
        sizes_sel = response.css(css)
        return [self._make_sku(color, sel) for sel in sizes_sel]

    def _make_sku(self, color, selector):
        return {
            'color': color,
            'currency': self.currency,
            'price': selector.css('::attr(data-final_price)').extract_first(),
            'previous price': selector.css('::attr(data-price)').extract_first(),
            'size': selector.css('::attr(data-title)').extract_first(),
            'id': selector.css('::attr(data-id)').extract_first()
        }

    def _extract_raw_product(self, response):
        xpath = '//script[contains(., "var product = {")]/text()'
        script = response.xpath(xpath).extract_first()
        raw_item = re.search(r"({.*?})", self.clean_text(script)).group(1)
        return demjson.decode(raw_item)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)

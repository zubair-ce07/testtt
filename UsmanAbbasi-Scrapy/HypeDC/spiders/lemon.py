# -*- coding: utf-8 -*-

import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from HypeDC.items import LululemonItem


class LemonSpider(CrawlSpider):
    name = 'lululemon'
    allowed_domains = ['shop.lululemon.com']
    start_urls = ["http://shop.lululemon.com/"]
    denied_keywords = 'login|inspiration|help|features|designs|stores|community'
    custom_settings = {'ITEM_PIPELINES': {'HypeDC.pipelines.LululemonPipeline': 1},
                       'DOWNLOADER_MIDDLEWARES': {'HypeDC.middlewares.ProxyMiddleware': 10}
    }

    rules = (
        Rule(LinkExtractor(restrict_css=('.large-menu li a',), deny=(denied_keywords,))),
        Rule(LinkExtractor(restrict_css=('.submenu li a',), deny=(denied_keywords,))),
        Rule(LinkExtractor(allow=('prod[0-9]+',), deny=(denied_keywords,)), callback='parse_item'),
    )

    def parse_item(self, response):
        item = LululemonItem()
        print("Current proxy:", response.meta['proxy'])
        item['url'] = response.url
        item['item_id'] = self.get_item_id(response)
        item['name'] = response.css('.product-description .OneLinkNoTx::text').extract_first()
        item['brand'] = 'lululemon'
        item['description'] = self.get_description(response)
        color_map = self.get_color_map(response)
        item['image_urls'] = self.get_image_urls(color_map)
        item['sku'], item['currency'] = self.get_sku_and_currency(response, color_map)
        yield item

    def get_description(self, response):
        description = []
        description.append(response.css('.ellipsis div::text').extract_first().strip())
        description.append(response.css('#fabric p::text').extract_first().strip())
        description.append(response.css('#fabric li::text').extract())
        care = json.loads(response.css('head script::text').re_first(r'styleColorMap = (.*);'))
        for care_details in care[0]['care']:
            description.append(care_details['careDescription'])
        return description

    def get_sku_and_currency(self, response, color_map):
        sku_info = json.loads(response.css('head > script::text').re_first('colorDriverString = (.*);'))
        currency = ""
        skus = []
        for sku_color_code, details_per_color in sku_info.items():
            for color_detail in details_per_color:
                for style_code in color_map:
                    if sku_color_code in style_code:
                        sku = {}
                        sku['size_name'] = color_detail[0]
                        sku['color_name'] = color_map[style_code]['name']
                        sku['price'] = color_detail[2]
                        sku['old_price'], sku['is_discounted'] = self.get_item_price(response)
                        skus.append(sku)
                        currency = sku['old_price'][0]
        return skus, currency

    def get_image_urls(self, color_map):
        image_urls = {}
        image_url_pattern = 'https://images.lululemon.com/is/image/lululemon/{color_code}_{number}'
        for style_code in color_map:
            urls_per_color = []
            for iteration in range(color_map[style_code]['count']):
                url = image_url_pattern.format(color_code=style_code, number=iteration+1)
                urls_per_color.append(url)
            image_urls[color_map[style_code]['name']] = urls_per_color
        return image_urls

    def get_color_map(self, response):
        color_map = {}
        colors_names = response.css('.section-color-swatch img::attr(alt)').extract()
        style_codes = response.css('.section-color-swatch img::attr(data-stylenumber)').extract()
        images_per_color = json.loads(response.css('head > script::text').re_first(r'styleCountDriverString = (.*);'))
        for color_name, style_code, in zip(colors_names, style_codes):
            color_code = style_code.split('_')[1]
            color_map[style_code] = {'name': color_name,
                                     'code': color_code,
                                     }
        for style_code, image_count in images_per_color.items():
            for color_map_style_code in color_map:
                if color_map_style_code == style_code:
                    color_map[style_code]['count'] = int(image_count[0][0])
        return color_map

    def get_item_id(self, response):
        item_id_match = re.search('prod[0-9]*', response.url)
        return item_id_match.group(0)

    def get_item_price(self, response):
        if response.css('.price-sale'):
            old_price = response.css('.price-original::text').extract_first()
            old_price = old_price.strip()
            is_discounted = True
        else:
            old_price = response.css('.price-fixed::text').extract_first()
            old_price = old_price.strip()
            is_discounted = False
        return old_price, is_discounted

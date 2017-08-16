# -*- coding: utf-8 -*-

import re
import json

from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule

from HypeDC.items import LululemonItem


class LemonSpider(CrawlSpider):
    name = 'lululemon'
    allowed_domains = ['shop.lululemon.com']
    start_urls = ["http://shop.lululemon.com/"]
    denied_keywords = 'login|inspiration|help|features|designs|stores|community'
    custom_settings = {'ITEM_PIPELINES': {'HypeDC.pipelines.LululemonPipeline': 1}}

    rules = (
        Rule(LinkExtractor(restrict_css=('.large-menu li a',), deny=(denied_keywords,))),
        Rule(LinkExtractor(restrict_css=('.submenu li a',), deny=(denied_keywords,))),
        Rule(LinkExtractor(allow=('prod[0-9]+',), deny=(denied_keywords,)), callback='parse_item'),
    )

    def parse_item(self, response):
        item = LululemonItem()
        item['url'] = response.url
        item['item_id'] = self.get_item_id(response)
        item['name'] = response.css('.product-description .OneLinkNoTx::text').extract_first()
        item['brand'] = 'lululemon'
        item['description'] = self.set_description(response)
        images_per_color = self.set_images_per_color(response)
        color_map = self.set_color_map(response)
        item['image_urls'] = self.set_image_urls(images_per_color, color_map)
        item['sku'], item['currency'] = self.set_sku_and_currency(response, color_map)
        yield item

    def set_description(self, response):
        fabric = response.css('.fabric.tab-content.selected p::text').extract_first()
        fabric_points = response.css('.fabric.tab-content.selected li::text').extract()
        fabric1 = '. '.join(fabric_points)
        fabric = fabric + ". " + fabric1
        description = response.css('.ellipsis div::text').extract_first()
        description = description + fabric
        description = description.replace('\n', '')
        care_head_info = response.css('head script::text').re_first(r'styleColorMap = (.*)')
        json_string = care_head_info[:-1]
        parsed_json = json.loads(json_string)
        for care_details in parsed_json[0]['care']:
            description = description + ". " + care_details['careDescription']
        return description

    def set_sku_and_currency(self, response, color_map):
        head_info = response.css('head > script::text').re_first('colorDriverString = (.*)')
        parsed_json = json.loads(head_info[:-1])
        currency = ""
        sku = []
        for parsed_json_key, parsed_json_values in parsed_json.items():
            for value in parsed_json_values:
                sku_dic = {}
                sku_dic['color_name'] = parsed_json_key
                sku_dic['size_name'] = value[0]
                sku_dic['price'] = value[2]
                sku_dic['old_price'], sku_dic['is_discounted'] = self.set_item_price(response)
                sku.append(sku_dic)
                currency = sku_dic['old_price'][0]

        for readings in sku:
            for code_key, value in color_map.items():
                if readings['color_name'] in code_key:
                    readings['color_name'] = value
        return sku, currency

    def set_image_urls(self, images_per_color, color_map):
        image_urls = {}
        image_url_pattern = 'https://images.lululemon.com/is/image/lululemon/{color_code}_{number}'
        for key, value in images_per_color.items():
            image_num = 1
            urls_per_color = []
            while image_num <= value:
                url_pattern = image_url_pattern.format(color_code=key, number=image_num)
                urls_per_color.append(url_pattern)
                image_num += 1
            image_urls[key] = urls_per_color

        for url_key in image_urls:
            for color_map_key, color_map_value in color_map.items():
                if url_key == color_map_key:
                    image_urls[color_map_value] = image_urls[url_key]
                    del image_urls[url_key]
        return image_urls

    def set_color_map(self, response):
        color_map = {}
        colors_list = response.css('.section-color-swatch img::attr(alt)').extract()
        colors_codes = response.css('.section-color-swatch img::attr(data-stylenumber)').extract()
        for color, code in zip(colors_list, colors_codes):
            color_map[code] = color
        return color_map

    def set_images_per_color(self, response):
        head_info = response.css('head > script::text').re_first(r'styleCountDriverString = (.*)')
        parsed_json = json.loads(head_info[:-1])
        images_per_color = {}
        for color_code, image_num in parsed_json.items():
            images_per_color[color_code] = int(image_num[0][0])
        return images_per_color

    def get_item_id(self, response):
        item_id_match = re.search('prod[0-9]*', response.url)
        return item_id_match.group(0)

    def set_item_price(self, response):
        if response.css('.price-sale'):
            old_price = response.css('.price-original::text').extract_first()
            old_price = old_price.strip()
            is_discounted = True
        else:
            old_price = response.css('.price-fixed::text').extract_first()
            old_price = old_price.strip()
            is_discounted = False
        return old_price, is_discounted

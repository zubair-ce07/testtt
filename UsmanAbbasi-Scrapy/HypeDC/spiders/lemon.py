# -*- coding: utf-8 -*-

import re
import json

from scrapy.linkextractors import LinkExtractor

from HypeDC.items import LululemonItem

from scrapy.spiders import CrawlSpider, Rule


class LemonSpider(CrawlSpider):
    name = 'lemon'
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
        item['item_id'] = self.set_item_id(response)
        item['name'] = response.css('.product-description .OneLinkNoTx::text').extract_first()
        item['brand'] = 'lululemon'
        description = response.css('.ellipsis div::text').extract_first()
        item['description'] = description.replace('\n', '')
        images_per_color = self.set_images_per_color(response)
        image_code = self.set_image_code(response)
        item['image_urls'] = self.set_image_urls(response, images_per_color, image_code)
        item['sku'], item['currency'] = self.set_sku_and_currency(response, image_code)
        yield item

    def set_sku_and_currency(self, response, image_code):
        head_info = response.css('head > script::text').re_first(r'colorDriverString.*')
        head_info_json = head_info.split("=")
        json_string = head_info_json[1]
        json_string = json_string[:-1]
        parsed_json = json.loads(json_string)
        currency = ""
        sku = []
        for key, values in parsed_json.items():
            for value in values:
                sku_dic = {}
                sku_dic['color_name'] = key
                sku_dic['size_name'] = value[0]
                sku_dic['price'] = value[2]
                sku_dic['old_price'], sku_dic['is_discounted'] = self.set_item_price(response)
                sku.append(sku_dic)
                currency = sku_dic['old_price'][0]
        for readings in sku:
            for code_key, value in image_code.items():
                if readings['color_name'] in code_key:
                    readings['color_name'] = value
        return sku, currency

    def set_image_urls(self, response, images_per_color, image_code):
        image_url_pattern = response.css('.product-images li::attr(data-preview)').extract_first()
        image_urls = {}
        for key, value in images_per_color.items():
            temp_value = 1
            urls_per_image = []
            while temp_value <= value:
                url_pattern = "lululemon/" + key + "_" + str(temp_value)
                img_url = re.sub('lululemon/.*', url_pattern, image_url_pattern)
                urls_per_image.append(img_url)
                temp_value += 1
            image_urls[key] = urls_per_image

        for url_key in image_urls:
            for code_key, value in image_code.items():
                if url_key == code_key:
                    image_urls[value] = image_urls[url_key]
                    del image_urls[url_key]
        return image_urls

    def set_image_code(self, response):
        image_code = {}
        colors_list = response.css('.section-color-swatch img::attr(alt)').extract()
        colors_codes = response.css('.section-color-swatch img::attr(data-stylenumber)').extract()
        for color, code in zip(colors_list, colors_codes):
            image_code[code] = color
        return image_code

    def set_images_per_color(self, response):
        head_info = response.css('head > script::text').re_first(r'styleCountDriverString.*')
        head_info_readings = head_info.split("=")
        head_info_formatting = head_info_readings[1].split("\"")
        index = 1
        images_per_color = {}
        while index != len(head_info_formatting):
            index2 = index + 2
            images_per_color[head_info_formatting[index]] = int(head_info_formatting[index2])
            index += 4
        return images_per_color

    def set_item_id(self, response):
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

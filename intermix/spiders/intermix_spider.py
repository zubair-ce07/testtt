# -*- coding: utf-8 -*-
from intermix.items import IntermixItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import copy
import json
import scrapy


class ThomaspinkSpider(CrawlSpider):
    name = "intermix"
    allowed_domains = ["intermixonline.com", "s7d2.scene7.com"]
    start_urls = ["https://www.intermixonline.com/basket.do?method=updateCountry&loc=landing&country=us"]
    rules = (Rule(LinkExtractor(restrict_xpaths=("//*[@id='navbarUl']",))),
             Rule(LinkExtractor(restrict_xpaths=("//*[@class= 'ml-thumb-image']",)), callback='parse_product'),)

    def parse_product(self, response):
        item = IntermixItem()
        item['description'] = self.get_description(response)
        item['name'] = self.get_product_name(response)
        item['url'] = response.url
        item['care'] = self.get_care(response)
        item['skus'] = self.get_sku(response)
        item['category'] = self.get_category(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = 'Women'
        item['brand'] = 'INTERMIX'
        item['market'] = 'US'
        item['image_urls'] = []
        return self.prepare_request(response, item)

    def get_description(self, response):
        des = self.clean_list(response.xpath("//*[@id='productDetailDescription']//div/text()").extract())
        return " ".join(des)

    def get_care(self, response):
        return self.clean_list(
                response.xpath("//*[@id='productDetailDescription']//div/text()").re('Fabric:\s(\w.*)\s'))

    def get_image_urls(self, response):
        return response.xpath(".//*[@id='detailViewContainer']//img/@src").extract()

    def get_product_name(self, response):
        return self.clean_list(response.xpath("//*[@class='detailDesigner']/text()").extract())

    def get_sku(self, response):
        sku = {}
        colors = self.get_colors(response)
        price = self.clean_list(self.get_price(response))
        previous_price = self.clean_list(self.get_previous_price(response))
        availability = self.check_availability(response)
        size = self.get_size(response)
        self.sku(price, colors, sku, size, availability, previous_price)
        return sku

    def get_price(self, response):
        return response.xpath("//*[@class='ml-item-price']/text()").extract()

    def get_previous_price(self, response):
        return response.xpath("//*[@class='ml-item-price-was']/text()").extract()

    def get_colors(self, response):
        color = {}
        product_info = json.loads(response.xpath(
                "//script[contains(text(),'buildEnhancedDependentOptionMenuObjects')]/text()").re(
                'buildEnhancedDependentOptionMenuObjects\((\{.*?})\);')[0])
        for item_color in range(len(product_info['aOptionTypes']['1']['options'])):
            color[product_info['aOptionTypes']['1']['options'][str(item_color)]['iOptionPk']] = \
                product_info['aOptionTypes']['1']['options'][str(item_color)]['sOptionName']
        return color

    def get_size(self, response):
        sizes = {}
        product_info = json.loads(response.xpath(
                "//script[contains(text(),'buildEnhancedDependentOptionMenuObjects')]/text()").re(
                'buildEnhancedDependentOptionMenuObjects\((\{.*?})\);')[0])
        for size in range(len(product_info['aOptionTypes']['0']['options'])):
            sizes[product_info['aOptionTypes']['0']['options'][str(size)]['iOptionPk']] = \
                product_info['aOptionTypes']['0']['options'][str(size)]['sOptionName']
        return sizes

    def get_category(self, response):
        return response.xpath("//*[@class ='detailbrand']//a/text()").extract()[0].strip()

    def get_retailer_sku(self, response):
        product_info = json.loads(response.xpath(
                "//script[contains(text(),'buildEnhancedDependentOptionMenuObjects')]/text()").re(
                'buildEnhancedDependentOptionMenuObjects\((\{.*?})\);')[0])
        return product_info['iProductPk']

    def clean_list(self, data):
        text = []
        to_remove = ['\t', '\n', '\r']
        for s in data:
            for pattern in to_remove:
                s = re.sub(pattern, '', s)
            text.append(s)
        return text

    def currency(self, price):
        if u'$' in price:
            return 'AUD'

    def sku(self, price, colors, sku, sizes, availability, previous_price):
        currency = self.currency(price[0])
        price[0] = re.sub('\$', '', price[0])
        if previous_price:
            previous_price[0] = re.sub('\$', '', previous_price[0])
        for color in colors:
            item = self.common_sku(colors[color], price, previous_price, currency)
            for size in sizes:
                if size + color in availability and availability[size + color] == True:
                    pass
                else:
                    item['out of stock'] = True
                item['size'] = sizes[size]
                sku[colors[color] + '_' + sizes[size]] = copy.deepcopy(item)
        return sku

    def common_sku(self, color, price, previous_price, currency):
        if previous_price:
            item = {'currency': currency, 'price': price[0], 'previous_price': previous_price[0],
                    'color': color}
        else:
            item = {'currency': currency, 'price': price[0], 'color': color}
        return item

    def check_availability(self, response):
        sku = {}
        product_info = json.loads(response.xpath(
                "//script[contains(text(),'buildEnhancedDependentOptionMenuObjects')]/text()").re(
                'buildEnhancedDependentOptionMenuObjects\((\{.*?})\);')[0])
        for item_no in range(len(product_info['aOptionSkus'])):
            sku[product_info['aOptionSkus'][str(item_no)]['skuOptions']['0']['iOptionPk'] +
                product_info['aOptionSkus'][str(item_no)]['skuOptions']['1']['iOptionPk']] = \
                product_info['aOptionSkus'][str(item_no)]['inStock']
        return sku

    def prod_color_id(self, response):
        colors_ids = {}
        product_info = json.loads(response.xpath(
                "//script[contains(text(),'buildDetailImageSwatchObjects')]/text()").re(
                'buildDetailImageSwatchObjects\((\{.*)\)')[0])
        for item_color in range(len(product_info['oOptionType']['options'])):
            colors_ids[item_color] = product_info['oOptionType']['options'][str(item_color)]['optionDetailImageLoc']
        return colors_ids

    def get_prod_image_urls(self, response):
        item = response.meta['item']
        product_info = json.loads(re.findall('\((\{.*)\,', response.body, flags=0)[0])
        for item_image in range(len(product_info['set']['item'])):
            item['image_urls'].append(
                    "https://intermix.scene7.com/is/image/" + product_info['set']['item'][item_image]['i']['n'])
        if response.meta['request']:
            yield scrapy.Request(response.meta['request'][0],
                                 meta={'item': item, 'request': response.meta['request'][1:]},
                                 callback=self.get_prod_image_urls)
        else:
            yield item

    def prepare_request(self, response, item):
        request = []
        color_id = self.prod_color_id(response)
        for id in color_id:
            color = color_id[id].split('?')
            request.append(
                    "https://s7d2.scene7.com/is/image/Intermix/" + color[
                        0] + "?req=set,json,UTF-8&labelkey=label&handler=s7sdkJSONResponse")
        yield scrapy.Request(request[0], meta={'item': item, 'request': request[1:]},
                             callback=self.get_prod_image_urls)

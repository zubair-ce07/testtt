# -*- coding: utf-8 -*-
from intermix.items import IntermixItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
from scrapy.http.request import Request


class IntermixSpider(CrawlSpider):
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
        product_info = self.get_product_info(response)
        item['skus'] = self.get_sku(response, product_info)
        item['category'] = self.get_category(response)
        item['retailer_sku'] = self.get_retailer_sku(product_info)
        item['gender'] = 'Women'
        item['brand'] = 'INTERMIX'
        item['market'] = 'US'
        item['image_urls'] = []
        return self.request_for_product_images(response, item)

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

    def get_sku(self, response, product_info):
        sku = {}
        colors = self.get_colors(product_info)
        price = self.clean_list(self.get_price(response))
        previous_price = self.clean_list(self.get_previous_price(response))
        sizes = self.get_size(product_info)
        price[0] = re.sub('\$', '', price[0])
        if previous_price:
            previous_price[0] = re.sub('\$', '', previous_price[0])
        for item_no in product_info['aOptionSkus']:
            color = colors[product_info['aOptionSkus'][str(item_no)]['skuOptions']['1']['iOptionPk']]
            size = sizes[product_info['aOptionSkus'][str(item_no)]['skuOptions']['0']['iOptionPk']]
            sku[color + '_' + size] = self.common_sku(color, price, previous_price, self.currency(price[0]), size)
        if len(colors) * len(sizes) > len(sku):
            for color in colors:
                for size in sizes:
                    if colors[color] + '_' + sizes[size] not in sku:
                        sku[colors[color] + '_' + sizes[size]] = self.common_sku(colors[color], price, previous_price,
                                                                                 self.currency(price[0]), sizes[size])
                        sku[colors[color] + '_' + sizes[size]]['out_of_stock'] = True
        return sku

    def get_price(self, response):
        return response.xpath("//*[@class='ml-item-price']/text()").extract()

    def get_previous_price(self, response):
        return response.xpath("//*[@class='ml-item-price-was']/text()").extract()

    def get_colors(self, product_info):
        color = {}
        for item_color in product_info['aOptionTypes']['1']['options']:
            color[product_info['aOptionTypes']['1']['options'][str(item_color)]['iOptionPk']] = \
                product_info['aOptionTypes']['1']['options'][str(item_color)]['sOptionName']
        return color

    def get_size(self, product_info):
        sizes = {}
        for size in product_info['aOptionTypes']['0']['options']:
            sizes[product_info['aOptionTypes']['0']['options'][str(size)]['iOptionPk']] = \
                product_info['aOptionTypes']['0']['options'][str(size)]['sOptionName']
        return sizes

    def get_category(self, response):
        return response.xpath("//*[@class ='detailbrand']//a/text()").extract()[0].strip()

    def get_retailer_sku(self, product_info):
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

    def common_sku(self, color, price, previous_price, currency, size):
        if previous_price:
            item = {'currency': currency, 'price': price[0], 'previous_price': previous_price[0],
                    'color': color, 'size': size}
        else:
            item = {'currency': currency, 'price': price[0], 'color': color}
        return item

    def prod_color_id(self, response):
        colors_ids = {}
        product_color_info = json.loads(response.xpath(
                "//script[contains(text(),'buildDetailImageSwatchObjects')]/text()").re(
                'buildDetailImageSwatchObjects\((\{.*)\)')[0])
        for item_color in product_color_info['oOptionType']['options']:
            colors_ids[item_color] = product_color_info['oOptionType']['options'][str(item_color)][
                'optionDetailImageLoc']
        return colors_ids

    def get_prod_image_urls(self, response):
        item = response.meta['item']
        product_info = json.loads(re.findall('\((\{.*)\,', response.body, flags=0)[0])
        for item_image in product_info['set']['item']:
            item['image_urls'].append(
                    "https://intermix.scene7.com/is/image/" + item_image['i']['n'])
        if response.meta['request']:
            yield Request(response.meta['request'].pop(),
                          meta={'item': item, 'request': response.meta['request']},
                          callback=self.get_prod_image_urls)
        else:
            yield item

    def request_for_product_images(self, response, item):
        request_url = []
        color_id = self.prod_color_id(response)
        for id in color_id:
            color = color_id[id].split('?')
            request_url.append('https://s7d2.scene7.com/is/image/Intermix/{0}?req=set,json,UTF-8&labelkey=\
                                label&handler=s7sdkJSONResponse'.format(color[0]))
        yield Request(request_url.pop(), meta={'item': item, 'request': request_url},
                      callback=self.get_prod_image_urls)

    def get_product_info(self, response):
        return json.loads(response.xpath(
                "//script[contains(text(),'buildEnhancedDependentOptionMenuObjects')]/text()").re(
                'buildEnhancedDependentOptionMenuObjects\((\{.*?})\);')[0])

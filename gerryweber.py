__author__ = 'sayyeda'

import scrapy
import json

from scrapy.spider import CrawlSpider, Rule
from gerrywebber.items import GerrywebberItem
from scrapy.linkextractor import LinkExtractor

class GerryScrapper(CrawlSpider):
    name = "Gerry_Webber"
    allowed_domains = ["house-of-gerryweber.de"]
    start_urls = ["http://www.house-of-gerryweber.de/Gerry-Weber/gerry,de,sc.html"]

    category_listing = ".//*[@id='cont_catmenu']/ul//li"

    # this is to enlist all product pages
    rules = [Rule(LinkExtractor(restrict_xpaths=category_listing), ),
             Rule(LinkExtractor(restrict_xpaths=['//ul[@class="cat_products"]/li']),callback='parse_product_details')
            ]

    # this is to retrieve required product details
    def parse_product_details(self, response):
        garment = GerrywebberItem()

        garment['spider_name'] = 'Gerry_Webber',
        garment['retailer'] = 'house_of_gerry_webber'
        garment['currency'] = 'EUR',
        garment['market'] = 'de'
        garment['brand'] = 'house of gerry webber'
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['selected_color'] = self.current_color(response)
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['price'] = self.product_price(response)
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['image_urls'] = response.xpath(".//*[contains(@id, 'zoom')]/@href").extract()
        garment['gender'] = 'female'
        garment['skus'] = {}
        colors_dict = self.color_mapping(response)

        # this request is to get all the skus f one product
        yield scrapy.Request(url=self.requesting_for_skus(response),
                            meta={'garment': garment, 'color_dict': colors_dict},
                            callback=self.product_skus)

    # this is to get response of json request to get skus.
    def requesting_for_skus(self, response):
        product_ID = response.xpath("//*[contains(@id,'recommendations')]/@data-pid").extract()[0]
        req_link = 'http://www.house-of-gerryweber.de/on/demandware.store/Sites-DE-Site/de/Product-GetVariants?pid=&format=json'
        tokens = req_link.split('=')
        req_href = tokens[0] + '=' + product_ID + tokens[1] + tokens[2]
        return req_href

    # calculating skus
    def product_skus(self, response):
        garment = response.meta['garment']
        color_dict = response.meta['color_dict']
        sku = {}
        variant = response.text
        variant_dict_string = str(variant)
        variant_dict = json.loads(variant_dict_string)
        variants_list = variant_dict['variations']['variants']

        for items in variants_list:
            size = self.get_size(items)
            for key in color_dict:
                if items['attributes']['color'] in color_dict:
                    sku_details = {}
                    sku_details['size'] = size
                    sku_key = (color_dict[key] + '_' + size)
                    sku_details['color'] = color_dict[key]
                    sku_details['price'] = items['pricing']['sale']
                    sku_details['in_stock'] = items['avLevels']['IN_STOCK']
                    sku_details['previous_price'] = [items['pricing']['standard']]
                    sku[sku_key] = sku_details

        garment['skus'] = sku
        yield garment

    def get_size(self, Dict):
        if Dict['attributes']['size']:
            return Dict['attributes']['size']
        return 'ONE'

    # this is to get the dictionary of colors, with color_id as key &
    # title as its value
    def color_mapping(self, response):
        sel = response.xpath("//*[@class='swatches color']/ul//li/div/a")
        color_dict = {}
        for item in sel:
            data_value = item.xpath("./@data-value").extract()[0]
            title = item.xpath("./@title").extract()[0]


            color_dict[data_value] = title

        return color_dict

    def product_name(self, response):
        return response.xpath("//*[contains(@class, 'productname')]//span[@itemprop='name']/text()").extract()[0]

    def product_description(self, response):
        return response.xpath("//*[@class='longdesc']//span/text()").extract()[0]

    def current_color(self, response):
        return response.xpath("//*[@class='selected swatchimage']//a/text()").extract()[0]

    def product_retailer_sku(self, response):
        return response.xpath("//*[contains(@class, 'productid')]/span/text()").extract()[0]

    def product_price(self, response):
        return response.xpath("//*[contains(@class, 'productinfo')]//span[@itemprop='price']/text()").extract()[0]

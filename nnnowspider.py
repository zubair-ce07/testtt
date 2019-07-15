import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json


class Nnnow(CrawlSpider):

    name = 'Nnnowspider'
    start_urls = ['https://www.nnnow.com/']
    all_gender_paths = '/men', '/women', '/kids', '/footwear'
    product_css = '.nwc-grid-col .nw-productlist '

    rules = (
        Rule(LinkExtractor(allow=all_gender_paths)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        item = NnnowRecord()

        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['price'] = self.get_price(response)
        item['previous_prices'] = self.get_previous_prices(response)
        item['size'] = self.get_size(response)
        item['color'] = self.get_color(response)
        item['category'] = self.get_category(response)
        item['image_urls'] = self.get_image_urls(response)
        item['currency'] = self.get_currency(response)
        item['sku_id'] = self.get_sku_id(response)
        item['url'] = self.get_url(response)
        item['care'] = self.get_care(response)
        item['description'] = self.get_description(response)

        return item

    def get_name(self, response):
        return response.css('.nw-product-name .nw-product-title::text').get()

    def get_brand(self, response):
        return response.css('.nw-product-name .nw-product-brandtxt::text').get()

    def get_price(self, response):
        return response.css('.nw-priceblock span.nw-priceblock-amt::text').get()

    def get_previous_prices(self, response):
        return response.css('.nw-priceblock del.nw-priceblock-amt::text').get()

    def get_size(self, response):
        return response.css('.nw-sizeblock-container   button.nw-size-chip::text').getall()

    def get_color(self, response):
        return response.css('.nw-color-title span.nw-color-name::text').get()

    def get_category(self, response):
        return response.css('.nw-breadcrumblist-list .nw-breadcrumb-listitem::text').getall()

    def get_image_urls(self, response):
        return response.css('.nw-maincarousel-wrapper img::attr(src)').getall()

    def get_currency(self, response):
        return response.css('.nw-sizeblock-container  span::attr(content)').get()

    def get_sku_id(self, response):
        return response.css('.nw-sizeblock-container  .nwc-btn span::text').get()

    def get_url(self, response):
        return response.css("meta[name='og_url']::attr(content)").get()

    def get_care(self, response):
        care = response.xpath('//script[contains(text(), "specs")]/text()').re_first("DATA= (.+)")
        converted_care = json.loads(care)

        return converted_care['ProductStore']['PdpData']['mainStyle']['finerDetails']['compositionAndCare']['list']

    def get_description(self, response):
        description = response.xpath('//script[contains(text(), "specs")]/text()').re_first("DATA= (.+)")
        converted_description = json.loads(description)

        return converted_description['ProductStore']['PdpData']['mainStyle']['finerDetails']['specs']['list']



class NnnowRecord(scrapy.Item):

    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    previous_prices = scrapy.Field()
    size = scrapy.Field()
    color = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    currency = scrapy.Field()
    sku_id = scrapy.Field()
    url = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()


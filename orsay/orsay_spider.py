"""
this modeule will scrape orsay.com website
"""
from __future__ import absolute_import
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
import json

MAX_DISPLAY = 72

class OrsaySpider(CrawlSpider):
    """ This crawler will extract all products of website """

    name = "orsay"
    start_urls = ['http://www.orsay.com/de-de/produkte/']
    allowed_domains = ['www.orsay.com']

    rules = (
        Rule(LinkExtractor(restrict_css="ul.refinement-category-list a"),
             callback='parse_pages',
            follow=True),
        Rule(LinkExtractor(restrict_css=".product-image>a"), callback='parse_product')
    )

    def parse_pages(self, response):
        """It is dealing with pagination"""

        max_items = self.get_max_items(response)
        for items_count in range(MAX_DISPLAY, max_items, MAX_DISPLAY):
            next_url = response.url + "?sz=" + str(items_count)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        """It is a parser for product"""
        for function in self.handle_product_variations(response):
            yield function

    def handle_product_variations(self, response):
        """This function will attach all sku to the product"""

        product = response.meta.get('curr_item')
        if not product:
            product = self.get_product(response)
            colors_url = self.get_colors_url(response)
            response.meta["colors_url"] = colors_url
            response.meta['curr_item'] = product
        else:
            json_data = self.get_product_variation_json(response)
            if json_data:
                self.get_sku(json_data, response, product)
        colors_url = response.meta.get('colors_url')
        if colors_url:
            color = colors_url.pop(0)
            yield scrapy.Request(url=color,
                                 callback=self.handle_product_variations,
                                 meta={'curr_item': product,
                                       'colors_url':colors_url},
                                 dont_filter=True)
        else:
            yield product

    def get_product(self, response):
        """this function will return product information from data"""

        product_detail_json = self.get_product_detail(response)
        product = {}
        product_detail_json = json.loads(product_detail_json)
        product['brand'] = 'Orsay'
        product['gender'] = 'women'
        product["name"] = product_detail_json["name"]
        product["description"] = self.get_description(response)
        product["retailer_sku"] = product_detail_json["idListRef6"]
        product["category"] = product_detail_json["categoryName"]
        product["currency"] = product_detail_json["currency_code"]
        product["price"] = product_detail_json["grossPrice"]
        product["urls"] = response.url
        product['care'] = self.get_care(response)
        product['images_url'] = self.get_images_url(response)
        product['skus'] = {}
        return product

    def get_sku(self, json_data, response, product):
        """this function will return sku from data"""

        product_variation = json.loads(json_data)
        color_value = product_variation["color"]["value"]
        color_name = self.get_color_name(response)
        size_li = response.css('ul.size li')
        for li in size_li:
            sku = {}
            sku["outOfStock"] = self.is_in_stock(li)
            size = self.get_size(li)
            sku["color"] = color_name
            sku["price"] = self.get_price(response)
            sku["size"] = size
            product['skus'][color_value + '_' + sku["size"]] = sku

    def get_description(self, response):
        description = response.css('.with-gutter::text').extract()
        return ' '.join(description) if description else ""

    def get_images_url(self, response):
        return response.css('.productthumbnail::attr(src)').extract()

    def get_product_variation_json(self, response):
        return response.css(
            '::attr(data-attributes)').extract_first()

    def get_price(self, response):
        return response.css('span.price-sales::text').extract_first().strip('\n')

    def get_size(self, li_response):
        return (li_response.css(' a::text').extract_first()).strip('\n')

    def get_colors_url(self, response):
        return response.css('.color a::attr(href)').extract()

    def get_max_items(self, response):
        return int(response.css(
            '.load-more-progress::attr(data-max)').extract_first())

    def get_care(self, response):
        return response.css('.product-info-block p::text').extract_first()

    def get_product_detail(self, response):
        return response.css(
            '::attr(data-product-details)').extract_first()

    def get_color_name(self, response):
        return response.css('.selected-value::text').extract_first()

    def is_in_stock(self, li_response):
        class_list = li_response.css('::attr(class)').extract_first()
        if "unselectable" in class_list:
            return True
        else:
            return False

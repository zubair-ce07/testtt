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
    name = "orsay"
    start_urls = ['http://www.orsay.com/de-de/produkte']
    allowed_domains = ['www.orsay.com']
    
    sub_categories_extractor = LinkExtractor(
        restrict_css="ul.refinement-category-list a")

    rules = (
        Rule(sub_categories_extractor, callback='parse_categories', follow=True),
    )

    def parse_categories(self, response):
        max_items = self.get_max_items(response)
        last_items = 0
        # check for more items or further pages and create request
        for items_count in range(MAX_DISPLAY, max_items, MAX_DISPLAY):
            last_items = items_count
            yield self.get_next_page_request(response, items_count)
        if max_items % MAX_DISPLAY:
            last_items +=  MAX_DISPLAY
            yield self.get_next_page_request(response, last_items)

    def parse_products(self, response):
        """
        this function will parse the main category page and extract
        urls of all products of that category
        """
        for product_div in response.css('div.product-tile'):
            product_detail_json = self.get_product_detail_json(product_div)
            if product_detail_json:
                product = self.get_product(product_detail_json, product_div)
                colors_url = self.get_colors_url(product_div)
                for color in colors_url:
                    color_url = color.css('a::attr(href)').extract_first()
                    
                    #if condition as there are some relative urls
                    if "//" not in color_url:
                        color_url = urljoin("http: // www.orsay.com", color_url)
                    yield scrapy.Request(url=color_url,
                                         callback=self.parse_color,
                                         meta={'curr_item': product})

    def parse_color(self, response):
        """this function is a parser for size and color"""
        product = response.meta['curr_item']
        product["urls"].append(response.url)
        product['images_url'].append(self.get_images_url(response))
        json_data = self.get_product_detail_json(response)
        if json_data:
            self.get_sku(self, json_data, response)
        yield product

    def get_product(self, product_detail_selector, response):
        """this function will form a product dict from data"""
        product = {}
        product_detail_json = json.loads(product_detail_selector)
        product["name"] = product_detail_json["name"]
        product["description"] = self.get_description(response)
        product["retailer_sku"] = product_detail_json["idListRef6"]
        product["category"] = product_detail_json["categoryName"]
        product["currency"] = product_detail_json["currency_code"]
        product["price"] = product_detail_json["grossPrice"]
        product["urls"] = []
        product['images_url']=[]
        product['colors'] = []
        product['skus'] = {}
        return product

    def get_sku(self, json_data, response, product):
        product_variation = json.loads(json_data)
        color_value = product_variation["color"]["value"]
        color_name = product_variation["color"]["displayName"]
        size_li = response.css('ul.size li')
        for li in size_li:
            sku = {}
            sku["outOfStock"] = self.is_in_stock(response)
            size = self.get_size(li)
            sku["color"] = color_name
            sku["price"] = self.get_price(response)
            sku["size"] = size
            product['skus'][color_value + '_' + sku.size] = dict(sku)

    def get_product_detail_json(self, product_div):
        return product_div.css(
            '::attr(data-product-details)').extract_first()

    def get_description(self, response):
        return response.css('div.product-info-title::text').extract()

    def get_images_url(self, response):
        return response.css('img.primary-image::attr(src)').extract_first()

    def get_product_detail_json(self, response):
        return response.css(
            'div.product-variations::attr(data-attributes)').extract_first()

    def get_price(self, response):
        response.css('span.price-sales::text').extract_first().strip('\n')

    def get_size(self, li_response):
        return (li_response.css(' a::text').extract_first()).strip('\n')

    def get_colors_url(self, product_div):
        product_div.css('ul.product-swatch-list li')

    def get_max_items(self, response):
        return int(response.css(
            'div.load-more-progress::attr(data-max)').extract_first())

    def get_next_page_request(self, response, count):
        next_url = response.url + "?sz=" + str(count)
        return scrapy.Request(url=next_url, callback=self.parse_products)

    def is_in_stock(self, li_response):
        class_list = li_response.css('::attr(class)').extract()
        if "unselectable" in class_list:
            return  True
        else:
            return False

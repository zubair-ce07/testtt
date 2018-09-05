"""
this modeule will scrape orsay.com website
"""
from __future__ import absolute_import
from urllib.parse import urljoin
import scrapy
import json


class OrsaySpider(scrapy.Spider):
    name = "orsay"
    start_urls = ['http://www.orsay.com/de-de/produkte']
    allowed_domains = ['www.orsay.com']
    product_list = []

    first_iter = True
    max_display = 0
    main_url = ""
    max_items = 0
    current_items = 0


    def parse(self, response):
        """this function will parse the main category page and extract
            urls of all products of that category"""
        for product_div in response.css('div.product-tile'):
            product_url = product_div.css(
                'div.product-name a::attr(href)').extract_first()
            product_url = urljoin('http://www.orsay.com/', product_url)
            yield scrapy.Request(url=product_url,
                                 callback=self.parse_product_page)


        current_item_response = response.css(
            'div.load-more-progress-label span::text').extract_first()
        if current_item_response:
            current_items = int(current_item_response)

            if self.first_iter:
                self.max_items = int(response.css(
                    'div.load-more-progress::attr(data-max)').extract_first())
                self.main_url = response.url
                self.max_display = current_items
                self.current_items = current_items
                self.first_iter = False

            if current_items < self.max_items:
                self.current_items = self.current_items + self.max_display
                next_url = self.main_url + "?sz=" + str(self.current_items)
                yield scrapy.Request(url=next_url,
                                     callback=self.parse)


    def parse_product_page(self, response):
        """this function will parse product page and extract
           all information of product """
        product_detail_selector = response.css(
            'div.js-product-content-gtm::attr(data-product-details)'
        ).extract_first()
        if product_detail_selector:
            product = self.get_product(product_detail_selector,
                                       response)
            colors_url = response.css('ul.color li')
            for color in colors_url:
                color_url = color.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=color_url,
                                     callback=self.parse_color,
                                     meta={'curr_item': product})
            self.product_list.append(product)


    def parse_color(self, response):
        """this function is a parser for size and color"""
        json_data = response.css(
            'div.product-variations::attr(data-attributes)').extract_first()
        product = response.meta['curr_item']
        if json_data:
            product_variation = json.loads(json_data)
            color_value = product_variation["color"]["value"]
            color_name = product_variation["color"]["displayName"]
            
            size_li = response.css('ul.size li')
            for li in size_li:
                sku = {}
                class_list = li.css('::attr(class)').extract()
                if "unselectable" in class_list:
                    sku["outOfStock"] = True
                else:
                    sku["outOfStock"] = False
                size = (li.css(' a::text').extract_first()).strip('\n')
                sku["color"] = color_name
                sku["currency"] = product.get("currency")
                sku["price"] = product.get("price")
                sku["size"] = size
                product['skus'][color_value + '_' + size] = dict(sku)


    def get_product(self, product_detail_selector, response):
        """this function will form a product dict from data"""
        product = {}
        product_detail_json = json.loads(product_detail_selector)
        product["name"] = product_detail_json["name"]
        product["description"] = response.xpath(
            "//div[@class='with-gutter']/following-sibling::text()"
        ).extract_first()
        product["retailer_sku"] = product_detail_json["idListRef6"]
        product["category"] = product_detail_json["categoryName"]
        product["url"] = response.url
        product["currency"] = product_detail_json["currency_code"]
        product["price"] = product_detail_json["grossPrice"]
        product['images_url'] = response.css(
            'img.productthumbnail::attr(src)').extract()
        product['skus'] = {}
        return product


    def closed(self, reason):
        """this function will convert list to json"""
        json_data = json.dumps(self.product_list)


"""
this modeule will scrape orsay.com website
"""
from __future__ import absolute_import
from urllib.parse import urljoin
import scrapy
import json


class OrsaySpider(scrapy.Spider):
    name = "orsay"
    start_urls = ['http://www.orsay.com/de-de/']
    allowed_domains = ['www.orsay.com']
    product_list = []

    def parse(self, response):
        """this function will parse the main page and extract
           all categories url"""
        products_urls = response.css('li.js-accordion-item a.has-sub-m'
                                     'enu::attr(href)').extract()
        for product_url in products_urls:
            yield response.follow(product_url,
                                  callback=self.parse_category_page)

    def parse_category_page(self, response):
        """this function will parse the main category page and extract
            urls of all products of that category"""
        for product_div in response.css('div.product-tile'):
            product_url = product_div.css(
                'div.product-name a::attr(href)').extract_first()
            product_url = urljoin('http://www.orsay.com/', product_url)
            yield scrapy.Request(url=product_url,
                                 callback=self.parse_product_page)

    def parse_product_page(self, response):
        """this function will parse product page and extract
           all information of product """
        product_detail_selector = response.css(
            'div.js-product-content-gtm::attr(data-product-details)'
        ).extract_first()
        if product_detail_selector:
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

            colors_url = response.css('ul.color li')
            for color in colors_url:
                color_url = color.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=color_url,
                                     callback=self.parse_color,
                                     meta={'curr_item': product})

    def parse_color(self, response):
        """this function is a parser for size and color"""
        sizes = response.css('ul.size li.selectable a::text').extract()
        product_variation = json.loads(response.css(
            'div.product-variations::attr(data-attributes)').extract_first())
        color_value = product_variation["color"]["value"]
        color_name = product_variation["color"]["displayName"]
        product = response.meta['curr_item']

        for size in sizes:
            size = size.strip('\n')
            sku = {}
            sku["color"] = color_name
            sku["currency"] = product.get("currency")
            sku["price"] = product.get("price")
            sku["size"] = size
            product['skus'][color_value + '_' + size] = dict(sku)
        self.product_list.append(product)

    def closed(self, reason):
        """this function will call at the end to conevrt list into json"""
        json_data = json.dumps(self.product_list)
        print(json_data)

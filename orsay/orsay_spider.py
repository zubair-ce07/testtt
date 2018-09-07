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

    first_iter = True
    max_items_in_stock = 0
    main_url = ""

    def parse(self, response):
        """this function will parse the main category page and extract
        urls of all products of that category
        """
        for product_div in response.css('div.product-tile'):
            product_detail_selector = product_div.css(
                '::attr(data-product-details)').extract_first()
            if product_detail_selector:
                product = self.get_product(product_detail_selector,
                                           product_div)
                colors_url = product_div.css('ul.product-swatch-list li')

                for color in colors_url:
                    color_url = color.css('a::attr(href)').extract_first()

                    # if condition as there are some relative urls
                    if "//" not in color_url:
                        color_url = urljoin("http: // www.orsay.com", color_url)
                    yield scrapy.Request(url=color_url,
                                         callback=self.parse_color,
                                         meta={'curr_item': product})

        next_items_count = response.css(
            'div.load-next-placeholder::attr(data-quantity)').extract_first()
        if next_items_count:
            yield self.handle_paginition(response, next_items_count)

    def parse_color(self, response):
        """this function is a parser for size and color"""
        json_data = response.css(
            'div.product-variations::attr(data-attributes)').extract_first()
        product = response.meta['curr_item']
        if json_data:
            product_variation = json.loads(json_data)
            color_value = product_variation["color"]["value"]
            color_name = product_variation["color"]["displayName"]
            product['colors'].append(color_name)
            product['images_url'].append(
                response.css('img.primary-image::attr(src)').extract_first())
            size_li = response.css('ul.size li')
            for li in size_li:
                sku = {}
                sku["outOfStock"] = False
                class_list = li.css('::attr(class)').extract()
                if "unselectable" in class_list:
                    sku["outOfStock"] = True
                size = (li.css(' a::text').extract_first()).strip('\n')
                sku["color"] = color_name
                sku["price"] = response.css(
                    'div.product-price span.price-sales::text'
                ).extract_first().strip('\n')
                sku["size"] = size
                product['skus'][color_value + '_' + size] = dict(sku)
        yield product

    def get_product(self, product_detail_selector, response):
        """this function will form a product dict from data"""
        product = {}
        product_detail_json = json.loads(product_detail_selector)
        product["name"] = product_detail_json["name"]
        product["description"] = response.css(
            'div.product-info-title::text').extract()
        product["retailer_sku"] = product_detail_json["idListRef6"]
        product["category"] = product_detail_json["categoryName"]
        product["url"] = response.css(
            'div.product-image > a::attr(href)').extract_first()
        product["currency"] = product_detail_json["currency_code"]
        product["price"] = product_detail_json["grossPrice"]
        product['images_url']=[]
        product['colors'] = []
        product['skus'] = {}
        return product

    def handle_paginition(self, response, next_items_count):
        next_items_count = round(float(next_items_count))
        if self.first_iter:
            # if first iteration save url and max items.
            self.max_items = int(response.css(
                'div.load-more-progress::attr(data-max)').extract_first())
            self.main_url = response.url
            self.first_iter = False

        # check for more items or further pages and create request
        if next_items_count < self.max_items:
            next_url = f"{self.main_url}?sz={str(next_items_count)}"
            return scrapy.Request(url=next_url, callback=self.parse)

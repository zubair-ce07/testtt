import json
import re
import scrapy
from copy import deepcopy
from scrapy import Request
from items import JeniespiderItem
from spiders.mixin import Mixin


class Parser(scrapy.Spider, Mixin):
    product_ids = []
    name = 'product_spider'
    gender_map = [
        'Girl', 'Baby Girl',
        'Boy', 'Baby Boy'
    ]

    def parse(self, response):
        product = JeniespiderItem()
        product_id = self.product_id(response)
        if product_id not in self.product_ids:
            self.product_ids.append(product_id)
            product['product_id'] = product_id
            product['url'] = response.url
            product['gender'] = self.gender(response)
            product['title'] = self.title(response)
            product['market'] = 'US'
            product['brand'] = 'Janie And Jack'
            product['retailer'] = 'janieandjack-us'
            product['description'] = self.description(response)
            product['category'] = self.category(response)
            product['skus'] = list()
            response.meta['product'] = product
            return self.requests_image_urls(response)

    def gender(self, response):
        xpath = "//span//a//span[contains(@itemprop, 'name')]/text()"
        category = response.xpath(xpath).extract()
        a = [x for x in self.gender_map if x in category]
        if a:
            return a[0]
        return "unisex-kids"

    @staticmethod
    def product_id(response):
        xpath = "//div[@class='product-number']//span[@class='visually-hidden']/text()"
        return response.xpath(xpath).extract_first(default='')

    def requests_image_urls(self, response):
        xpath = "//a[@class='swatchanchor ']/@href"
        sizes = response.xpath(xpath).extract()
        pending_requests = []
        for size in sizes:
            pending_requests.append(Request(size,
                                            callback=self.parse_sizes))
        meta = deepcopy(response.meta)
        product_id = response.meta['product']._values['product_id']
        meta['size_url'] = pending_requests
        url = "http://i1.adis.ws/s/janieandjack/" + product_id + "_SET.js"
        return Request(url,
                       meta=meta,
                       callback=self.parse_image)

    def parse_image(self, response):
        product = response.meta['product']
        product["image_urls"] = self.image_src(response)
        return self.next_action(response, product)

    @staticmethod
    def image_src(response):
        body = response.body_as_unicode()
        body = re.search(r'imgSet\(({.+})\)', body).group(1)
        image_src = json.loads(body)
        img_src = [img.get('src') for img in image_src.get('items')]
        return img_src

    @staticmethod
    def title(response):
        title = response.css('h1.product-name::text').extract_first(default='')
        return title.strip()

    @staticmethod
    def description(response):
        xpath = "//div[contains(@class, 'longDescription')]//ul//li/text()"
        description = response.xpath(xpath).extract()
        description = [descript.strip() for descript in description]
        return description

    @staticmethod
    def category(response):
        xpath = "//span//a//span[contains(@itemprop, 'name')]/text()"
        category = response.xpath(xpath).extract()
        return category[-1]

    def parse_sizes(self, response):
        product = response.meta['product']
        item = dict()
        item['price'] = self.price(response)
        item['currency'] = 'USD'
        item['previous_prices'] = self.previous_prices(response)
        colour = self.colour(response)
        size = self.size(response)
        item['colour'] = colour
        item['size'] = size
        item['sku_id'] = str(colour) + "_" + str(size)
        product['skus'].append(item)
        return self.next_action(response, product)

    @staticmethod
    def next_action(response, product):
        size_url = response.meta['size_url']
        if size_url:
            request = size_url.pop()
            request.meta['size_url'] = response.meta['size_url']
            request.meta['product'] = response.meta['product']
            return request
        else:
            return product

    @staticmethod
    def price(response):
        xpath = "//span[@class='price-sales']/text()"
        price = response.xpath(xpath).extract_first()
        price = price.replace('$', '')
        price = str(round(float(price) * 100))
        return price

    @staticmethod
    def colour(response):
        xpath = "//span[contains(@class, 'selected-value') " \
                "and contains(@class, 'color')]/text()"
        colour = response.xpath(xpath).extract_first().replace('\n', '')
        return colour

    @staticmethod
    def size(response):
        xpath = "//li[contains(@class, 'selectable') " \
                "and contains(@class, 'selected')]" \
                "//a[@class='swatchanchor ']/text()"
        size = response.xpath(xpath).extract()
        return "".join(e for e in size[len(size) - 1] if e.isalnum())

    @staticmethod
    def previous_prices(response):
        xpath = "//span[@class='price-standard']/text()"
        previous_prices = response.xpath(xpath).extract()
        return previous_prices

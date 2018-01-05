import json
import re
import scrapy
from copy import deepcopy
from scrapy import Request
from jeniespider.items import JeniespiderItem
from jeniespider.spiders.mixin import Mixin


class Parser(scrapy.Spider, Mixin):
    product_ids = []
    name = 'product_spider'
    gender_map = [
        ('Girl', 'girl'),
        ('Boy', 'boy')
    ]

    def parse(self, response):
        product = JeniespiderItem()
        product_id = self.product_id(response)
        if product_id in self.product_ids:
            return
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
        product['skus'] = {}
        return self.requests_image_urls(response, product)

    def gender(self, response):
        xpath = "//span//a//span[contains(@itemprop, 'name')]/text()"
        category = response.xpath(xpath).extract()
        for gender, l_gender in self.gender_map:
            if gender in category:
                return l_gender
        return "unisex-kids"

    @staticmethod
    def product_id(response):
        xpath = "//div[@class='product-number']//span[@class='visually-hidden']/text()"
        return response.xpath(xpath).extract_first(default='')

    def requests_image_urls(self, response, product):
        link = "http://i1.adis.ws/s/janieandjack/"
        sizes = self.size_urls(response)
        pending_requests = []
        for size in sizes:
            pending_requests.append(Request(size,
                                            callback=self.parse_sizes))
        product['size_urls'] = pending_requests
        url = "{}{}_SET.js".format(link, product['product_id'])
        response.meta['product'] = product
        meta = deepcopy(response.meta)
        return Request(url,
                       meta=meta,
                       callback=self.parse_image)

    @staticmethod
    def size_urls(response):
        xpath = "//a[@class='swatchanchor ']/@href"
        return response.xpath(xpath).extract()

    def parse_image(self, response):
        product = response.meta['product']
        product["image_urls"] = self.image_src(response)
        return self.next_action(response, product)

    @staticmethod
    def image_src(response):
        body = response.text
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
        return [descript.strip() for descript in description]

    @staticmethod
    def category(response):
        xpath = "//span//a//span[contains(@itemprop, 'name')]/text()"
        category = response.xpath(xpath).extract()
        return category[-1]

    def parse_sizes(self, response):
        product = response.meta['product']
        product['skus'].update(self.skus_items(response))
        return self.next_action(response, product)

    def skus_items(self, response):
        item = dict()
        item['price'] = self.price(response)
        item['currency'] = 'USD'
        item['previous_prices'] = self.previous_prices(response)
        colour = self.colour(response)
        size = self.size(response)
        item['colour'] = colour
        item['size'] = size
        sku_id = "{}_{}".format(colour, size)
        return {sku_id: item}

    @staticmethod
    def next_action(response, product):
        product_size = response.meta['product']
        if product_size['size_urls']:
            request = product_size['size_urls'].pop()
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
        return "".join(e for e in size[-1] if e.isalnum())

    @staticmethod
    def previous_prices(response):
        xpath = "//span[@class='price-standard']/text()"
        previous_prices = response.xpath(xpath).extract()
        return previous_prices

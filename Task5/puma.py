import json
import math
import re

from scrapy import Spider, Request
from w3lib import url

from Task5.items import Product


class PumaSpider(Spider):
    name = 'puma'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['in.puma.com']
    start_urls = ['https://in.puma.com']

    items_per_page = 12
    image_url_t = "https://in.puma.com/ajaxswatches/ajax/update?pid={}"
    gender_map = {
        'unisex': 'Unisex',
        'men': 'Men',
        'women': 'Women',
        'girl': 'Girl',
        'boy': 'Boy',
        'kids': 'Kids'
    }

    def parse(self, response):
        adult_categories_links = response.css('p.category-title2 a::attr(href)').re('(.+)\?')
        kids_categories_links = response.xpath('//a[text()="Kids"]/@href').re('(.+)\?')
        all_categories_links = adult_categories_links + kids_categories_links

        yield from [Request(category_link, callback=self.parse_categories)
                    for category_link in all_categories_links]

    def parse_categories(self, response):
        product_types = response.css('a::attr(href)').re('product_type=([\d+]+)')
        yield from [Request(url.add_or_replace_parameter(response.url, "product_type", product_type),
                            callback=self.parse_pagination)
                    for product_type in product_types]

    def parse_pagination(self, response):
        total_items = response.css('b.only::text').extract_first()
        total_pages = int(math.ceil(int(total_items)/self.items_per_page)) if total_items else 0

        product_type = response.xpath('//*[text()="Product Type:"]/following-sibling::span[1]/text()').extract_first()
        menu_category = re.search('/([-\w+]+)\.html', response.url).group(1)

        for page_number in range(1, total_pages+1):
            yield Request(url.add_or_replace_parameter(response.url, "p", page_number), callback=self.parse_item_links,
                          meta={"product_type": product_type, "menu_category": menu_category})

    def parse_item_links(self, response):
        item_urls = response.css('.product-image::attr(href)').extract()
        yield from [Request(item_url, callback=self.parse_item, meta=response.meta) for item_url in item_urls]

    def parse_item(self, response):
        item = Product()

        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['brand'] = 'puma'
        item['url'] = response.url
        item['price'] = self.extract_price(response)
        item['description'] = self.extract_description(response)
        item['gender'] = self.detect_gender(response)
        item["category"] = self.extract_categories(response)
        item['skus'] = self.extract_skus(response)

        item["image_urls"] = set()
        image_urls_json_requests = []
        image_urls_json_requests.extend([Request(self.image_url_t.format(product_id), callback=self.parse_image_urls,
                                                 meta={"json_requests": image_urls_json_requests, "item": item})
                                         for product_id in self.extract_product_options(response)["childProducts"]])

        return image_urls_json_requests.pop()

    def parse_image_urls(self, response):
        item = response.meta.get("item")

        for image_url in json.loads(response.body):
            item["image_urls"].add(image_url["image"])

        image_urls_json_requests = response.meta.get("json_requests")
        if image_urls_json_requests:
            return image_urls_json_requests.pop()

        return item

    def extract_retailer_sku(self, response):
        item_options = self.extract_product_options(response)
        return item_options["productId"]

    def extract_name(self, response):
        item_options = self.extract_product_options(response)
        return item_options["productName"]

    def detect_gender(self, response):
        name = f'{self.extract_name(response)} {response.url}'.lower()

        for gender in self.gender_map:
            if gender in name:
                return self.gender_map[gender]

        return 'Unisex'

    def extract_price(self, response):
        item_options = self.extract_product_options(response)
        return float(item_options["basePrice"]) * 100

    def extract_description(self, response):
        item_options = self.extract_product_options(response)
        return item_options["description"].split("\n")

    def extract_categories(self, response):
        item_gender = self.detect_gender(response)
        item_type = response.meta.get("product_type")
        item_menu_category = response.meta.get("menu_category")
        return [item_gender, item_type, item_menu_category]

    def extract_product_options(self, response):
        return json.loads(response.css('script').re_first(r'Product.Config\((.+)\);'))

    def extract_skus(self, response):
        item_options = self.extract_product_options(response)

        if item_options["attributes"]:
            colors = self.extract_colors(item_options)
            sizes = self.extract_sizes(item_options)
            skus = []

            for sku_id, prices in item_options["childProducts"].items():
                color_label, size_label = self.extract_color_size_lables(sku_id, colors, sizes)

                skus.append({"sku_id": f'{color_label}_{size_label}', "color": color_label, 'size': size_label,
                             "currency": item_options["template"][0], "previous_price": prices["price"],
                             "price": prices["finalPrice"]
                })

            return skus

    def extract_colors(self, item_options):
        for attr in item_options["attributes"].values():
            if attr["code"] == 'color':
                return attr["options"]

    def extract_sizes(self, item_options):
        for attr in item_options["attributes"].values():
            if attr["code"] == 'size':
                return attr["options"]

    def extract_color_size_lables(self, sku_id, colors, sizes):
        color_label = None
        size_label = None

        for color in colors:
            if sku_id in color["products"]:
                color_label = color["label"]

        for size in sizes:
            if sku_id in size["products"]:
                size_label = size["label"]

        return color_label, size_label

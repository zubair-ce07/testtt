import json
import math
import re

from scrapy import Spider, Request
from w3lib import url

from Task5.items import ProductItem


class PumaSpider(Spider):
    name = 'puma'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['in.puma.com']
    start_urls = ['https://in.puma.com/']

    items_per_page = 12
    item_sizes = ['xs', 's', 'm', 'l', 'x', 'xl', 'xxl', 'one size', 'adult']
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

        for product_type in product_types:
            link = url.add_or_replace_parameter(response.url, "product_type", product_type)
            yield Request(link, callback=self.parse_pagination)

    def parse_pagination(self, response):
        total_items = response.css('b.only::text').extract_first()
        total_pages = int(math.ceil(int(total_items)/self.items_per_page)) if total_items else 0
        product_type = response.xpath('//*[text()="Product Type:"]/following-sibling::span[1]/text()').extract_first()
        menu_category = re.search('/([-\w+]+)\.html', response.url).group(1)

        for page_number in range(1, total_pages+1):
            yield Request(url.add_or_replace_parameter(response.url, "p", page_number),
                          callback=self.parse_item_links,
                          meta={"product_type": product_type, "menu_category": menu_category})

    def parse_item_links(self, response):
        item_urls = response.css('.product-image::attr(href)').extract()
        yield from [Request(item_url, callback=self.parse_item, meta=response.meta) for item_url in item_urls]

    def parse_item(self, response):
        item = ProductItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['brand'] = 'puma'
        item['url'] = response.url
        item['price'] = self.extract_price(response)
        item['gender'] = self.detect_gender(response)
        item["category"] = self.get_categories(response)
        item['description'] = self.extract_description(response)
        item['skus'] = self.extract_skus(response)
        product_ids = self.extract_product_options(response).get("base_image")

        if not product_ids:
            return item

        item["image_urls"] = set()
        image_urls_json_requests = []
        image_urls_json_requests.extend([Request(self.image_url_t.format(product_id), callback=self.parse_image_urls,
                                                 meta={"json_requests": image_urls_json_requests, "item": item})
                                        for product_id in product_ids.keys()])
        return image_urls_json_requests.pop()

    def parse_image_urls(self, response):
        image_urls = {image_url["image"] for image_url in json.loads(response.body)}
        image_urls_json_requests = response.meta.get("json_requests")
        item = response.meta.get("item")

        for image_url in image_urls:
            item["image_urls"].add(image_url)

        if not image_urls_json_requests:
            return item

        return image_urls_json_requests.pop()

    def extract_retailer_sku(self, response):
        return response.css('.style_no::text').extract_first()

    def extract_name(self, response):
        return response.css('.product-name span::text').extract_first()

    def detect_gender(self, response):
        name = (self.extract_name(response) + response.url).lower()

        for gender in self.gender_map.keys():
            if gender in name:
                return self.gender_map[gender]

        return 'Unisex'

    def extract_price(self, response):
        raw_price = response.css('span[id^="product-price-"]::text').re_first('[\d+,]+')
        raw_price = raw_price if raw_price else response.css('span.price::text').re_first('[\d+,]+')
        return float(raw_price.replace(',', '')) * 100

    def get_categories(self, response):
        item_gender = self.detect_gender(response)
        item_type = response.meta.get("product_type")
        item_menu_category = response.meta.get("menu_category")
        return [item_gender, item_type, item_menu_category]

    def extract_description(self, response):
        descriptions = response.css('.product-collateral .std *::text').extract()
        return ''.join(descriptions)

    def extract_skus(self, response):
        item_options = self.extract_product_options(response).get("option_labels")
        if item_options:
            sizes = [label for label in item_options.keys() if label in self.item_sizes or not label.isalpha()]
            colors = [label for label in item_options.keys() if label not in sizes]
            skus = []

            for color in colors:
                products = item_options[color]["products"]

                for size in sizes:
                    sku = {"sku_id": f"{color}_{size}", "color": color, 'size': size}

                    if all([product not in products for product in item_options[size]["products"]]):
                        sku["out_of_stock"] = True

                    if response.css('span[id^="old-price-"]::text').extract():
                        sku["previous_prices"] = [price.strip("\n").strip(" ") for price in
                                                  response.css('span[id^="old-price-"]::text').extract()]
                        sku["currency"] = sku["previous_prices"][0][0]

                    skus.append(sku)

            return skus

    def extract_product_options(self, response):
        return json.loads(response.css('script').re_first(r'.*parseJSON\(\'(.+)\'\)\);'))

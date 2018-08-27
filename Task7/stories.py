import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import js2py
from w3lib.url import add_or_replace_parameter

from Task7.items import Product


class StoriesSpider(CrawlSpider):
    name = 'stories'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['stories.com']

    allowed_r = ('/clothing', '/shoes', '/bags', '/jewellery', '/accessories',
                 '/swimwear', '/lingerie', '/stationery', '/beauty')
    rules = (Rule(LinkExtractor(allow=allowed_r, restrict_css=".categories"), callback='parse_pagination'),)

    skus_request_t = 'https://www.stories.com/en_{0}/getAvailability?variants={1}'
    cookies = {
        'HMCORP_locale': 'en_GB',
        'HMCORP_currency': 'GBP'
    }

    def start_requests(self):
        urls = ['https://www.stories.com']
        return [Request(url, cookies=self.cookies) for url in urls]

    def parse_pagination(self, response):
        total_items = int(response.css("#productCount::attr(class)").extract_first())
        products_per_page = int(response.css("#productPerPage::attr(class)").extract_first())
        base_url = response.css("#productPath::attr(class)").extract_first()

        pages_urls = [add_or_replace_parameter(base_url, "start", start)
                      for start in range(0, total_items, products_per_page)]

        return [response.follow(url, callback=self.parse_items_links) for url in pages_urls]

    def parse_items_links(self, response):
        items_links = response.css("a::attr(href)").extract()
        return [response.follow(items_link, callback=self.parse_item) for items_link in items_links]

    def parse_item(self, response):
        raw_product = self.extract_raw_product(response)
        current_item = raw_product[raw_product["articleCode"]]
        item = Product()

        item["retailer_sku"] = self.extract_retailer_sku(raw_product)
        item["name"] = self.extract_name(raw_product)
        item["url"] = self.extract_url(current_item)
        item["brand"] = self.extract_brand(current_item)
        item["price"] = self.extract_price(current_item)
        item["gender"] = "Women"
        item["description"] = self.extract_description(current_item)
        item["image_urls"] = self.extract_image_urls(current_item)
        item["care"] = self.extract_care(current_item)
        item["category"] = self.extract_categories(raw_product)

        color_variants = self.extract_article_ids(response)
        variants = self.extract_variants(raw_product, color_variants)

        return Request(self.skus_request_t.format(self.cookies["HMCORP_currency"].lower(), variants),
                       cookies=self.cookies, callback=self.parse_skus, dont_filter=True,
                       meta={'item': item, 'raw_product': raw_product, 'color_variants': color_variants})

    def parse_skus(self, response):
        item = response.meta["item"]
        item["skus"] = self.extract_skus(response)

        return item

    def extract_raw_product(self, response):
        return js2py.eval_js(response.css("[class*='o-page-content '] script::text").extract_first())

    def extract_retailer_sku(self, raw_product):
        return re.findall('(\d+)', raw_product['baseProductCode'])[0]

    def extract_name(self, raw_product):
        return raw_product["name"]

    def extract_url(self, current_item):
        return current_item["pdpLink"]

    def extract_brand(self, current_item):
        return current_item["brandName"]

    def extract_price(self, current_item):
        return float(current_item["priceValue"])*100

    def extract_description(self, current_item):
        return current_item["description"]

    def extract_image_urls(self, current_item):
        return [f'https:{image_url["fullscreen"]}' for image_url in current_item["images"]]

    def extract_care(self, current_item):
        return current_item["careInstructions"]

    def extract_categories(self, item_details):
        return item_details["mainCategorySummary"]

    def extract_variants(self, raw_product, color_variants):
        variant_codes= []

        for color_variant in color_variants:
            variant_codes.extend(raw_product[color_variant])

        return ','.join(variant_codes)

    def extract_article_ids(self, response):
        raw_article_ids = js2py.eval_js(response.css('script::text').
                                        re_first('var articlesIds=\{[\d\w\s\t\n,:"]+};'))

        return [key for key in raw_article_ids]

    def extract_skus(self, response):
        raw_product = response.meta["raw_product"]
        color_variants = [raw_product[key] for key in response.meta["color_variants"]]
        available_variants = response.css('item::text').extract()

        skus = []
        for color_variant in color_variants:
            for sku_variant in color_variant["variants"]:
                sku = {"size": sku_variant["sizeName"], "color": color_variant["name"]}
                sku["price"] = color_variant["price"]
                sku["currency"] = self.cookies["HMCORP_currency"]
                sku["sku_id"] = sku_variant["variantCode"]

                if color_variant["priceOriginal"]:
                    sku["previous_prices"] = [color_variant["priceOriginal"]]

                if sku_variant["variantCode"] not in available_variants:
                    sku["out_of_stock"] = True

                skus.append(sku)

        return skus

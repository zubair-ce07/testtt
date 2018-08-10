import json

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from Task5.items import Product


class PumaSpider(CrawlSpider):
    name = 'puma'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['in.puma.com']
    start_urls = ['https://in.puma.com']

    allowed_r = ('men/\w+/', 'women/\w+/', 'kids/', 'sale/\w+/')
    rules = (Rule(LinkExtractor(allow=allowed_r, restrict_css=".mp-level li a"), callback='parse_pagination'),)

    image_url_t = "https://in.puma.com/ajaxswatches/ajax/update?pid={}"
    gender_map = {
        'unisex': 'Unisex',
        'men': 'Men',
        'women': 'Women',
        'girl': 'Girl',
        'boy': 'Boy',
        'kids': 'Kids'
    }

    def parse_pagination(self, response):
        response.meta["categories"] = response.css('.breadcrumbs a::text, .breadcrumbs strong::text').extract()
        item_urls = response.css('.product-image::attr(href)').extract()

        yield from [Request(item_url, callback=self.parse_item, meta=response.meta) for item_url in item_urls]

        next_page_url = response.css('a.next::attr(href)').extract_first()

        if next_page_url:
            return Request(next_page_url, callback=self.parse_pagination)

    def parse_item(self, response):
        item_options = self.extract_item_options(response)
        item = Product()

        item['retailer_sku'] = self.extract_retailer_sku(item_options)
        item['name'] = self.extract_name(item_options)
        item['brand'] = 'puma'
        item['url'] = response.url
        item['price'] = self.extract_price(item_options)
        item['description'] = self.extract_description(item_options)
        item['gender'] = self.detect_gender(item_options, response)
        item["category"] = self.extract_categories(response)
        item['skus'] = self.extract_skus(item_options)
        item["image_urls"] = set()
        item["requests_queue"] = self.get_image_urls_requests(item_options, item)

        return item["requests_queue"].pop()

    def get_image_urls_requests(self, item_options, item):
        product_ids = item_options["childProducts"]
        image_url_requests = [self.image_url_t.format(product_id) for product_id in product_ids]

        return [Request(url, callback=self.parse_image_urls, meta={"item": item}) for url in image_url_requests]

    def parse_image_urls(self, response):
        item = response.meta.get("item")
        item["image_urls"] |= self.extract_image_urls(response)

        if item["requests_queue"]:
            return item["requests_queue"].pop()

        del item["requests_queue"]
        return item

    def extract_image_urls(self, response):
        return {image_url["image"] for image_url in json.loads(response.text)}

    def extract_item_options(self, response):
        return json.loads(response.css('script').re_first(r'Product.Config\((.+)\);'))

    def extract_retailer_sku(self, item_options):
        return item_options["productId"]

    def extract_name(self, item_options):
        return item_options["productName"]

    def extract_price(self, item_options):
        return float(item_options["basePrice"]) * 100

    def extract_description(self, item_options):
        return item_options["description"].split("\n")

    def detect_gender(self, item_options, response):
        name = f'{self.extract_name(item_options)} {response.url}'.lower()

        for gender in self.gender_map:
            if gender in name:
                return self.gender_map[gender]

        return 'Unisex'

    def extract_categories(self, response):
        return response.meta["categories"]

    def extract_skus(self, item_options):
        colors = [attr["options"] for attr in item_options["attributes"].values() if attr["code"] == 'color'][0]
        sizes = [attr["options"] for attr in item_options["attributes"].values() if attr["code"] == 'size'][0]
        skus = []

        for sku_id, prices in item_options["childProducts"].items():
            color_label = [color["label"] for color in colors if sku_id in color["products"]][0]
            size_label = [size["label"] for size in sizes if sku_id in size["products"]][0]

            skus.append({"sku_id": f'{color_label}_{size_label}',
                         "color": color_label,
                         'size': size_label,
                         "currency": "INR",
                         "previous_prices": [prices["price"]],
                         "price": prices["finalPrice"]
            })

        return skus

import json
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode
from w3lib.url import add_or_replace_parameter

from Task6.items import Product


class MarkhamSpider(CrawlSpider):
    name = 'markham'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['markham.co.za']
    start_urls = ['https://www.markham.co.za']

    allowed_links = ('plp/clothing/', 'plp/shoes/', '/plp/accessories/')
    rules = [Rule(LinkExtractor(allow=allowed_links, restrict_css=".nav__item-title"), callback='parse_pagination')]

    skus_request_t = 'https://www.markham.co.za/product/generateProductJSON.jsp?productId={}'
    category_request_t = 'https://www.markham.co.za/search/ajaxResultsList.jsp?N={0}&baseState={0}'

    def parse_pagination(self, response):
        products_details = json.loads(response.css('#product-listing-static-data::text').extract_first()).get("data")
        total_pages = products_details["totalPages"]

        category_id = re.search('N-([\w+]+);', response.url).group(1)
        category_request = self.category_request_t.format(category_id)

        url_parameters = [urlencode({"No": page*15, "page": page}) for page in range(1, total_pages+1)]

        pages_urls = [f'{category_request}&{url_parameter}' for url_parameter in url_parameters]

        return [Request(page_url, callback=self.parse_item_links) for page_url in pages_urls]

    def parse_item_links(self, response):
        products = json.loads(response.text)["data"]["products"]
        item_urls = [response.urljoin(product["pdpLinkUrl"]) for product in products]

        return [Request(item_url, callback=self.parse_item) for item_url in item_urls]

    def parse_item(self, response):
        item = Product()
        item_detail = json.loads(response.css('#product-static-data::text').extract_first())

        item["retailer_sku"] = self.extract_retailer_sku(item_detail)
        item["name"] = self.extract_name(item_detail)
        item["price"] = self.extract_price(item_detail)
        item["brand"] = self.extract_brand(item_detail)
        item["url"] = response.url
        item["category"] = self.extract_categorie(response)
        item["gender"] = "Men"
        item["description"] = self.extract_description(response)
        item["image_urls"] = self.extract_image_urls(item_detail)
        item["skus_requests"] = self.get_skus_requests(item_detail, item)

        return item["skus_requests"].pop()

    def get_skus_requests(self, item_detail, item):
        colors = item_detail["colors"]
        sku_request = self.skus_request_t.format(item_detail["id"])
        skus_requestes = [add_or_replace_parameter(sku_request, "selectedColor", color["id"]) for color in colors]

        item["skus"] = []

        return [Request(url, callback=self.parse_skus, meta={"item": item}) for url in skus_requestes]

    def parse_skus(self, response):
        item = response.meta["item"]
        sku_detail = json.loads(response.text)

        item["skus"].extend(self.create_sku(sku_detail))

        if item["skus_requests"]:
            item["skus_requests"].pop()

        del item["skus_requests"]
        return item

    def create_sku(self, sku_detail):
        skus = []

        if not sku_detail.get("sizes"):
            sku_detail["sizes"] = [{"name": "One Size", "available": True}]

        for size in sku_detail["sizes"]:
            sku = {"color": sku_detail["colors"][0]["name"],
                   "size": size["name"],
                   "price": sku_detail["price"],
                   "sku_id": f'{sku_detail["colors"][0]["name"]}_{size["name"]}'}

            if not size["available"]:
                sku["out_of_stock"] = True

            if sku_detail.get("oldPrice"):
                sku["previous_price"] = sku_detail["oldPrice"]

            skus.append(sku)

        return skus

    def extract_retailer_sku(self, item_detail):
        return item_detail["id"]

    def extract_name(self, item_detail):
        return item_detail["name"]

    def extract_price(self, item_detail):
        return float(re.search('([\d+,]+)', item_detail["price"]).group(1).replace(",", "")) * 100

    def extract_brand(self, item_detail):
        return item_detail["brand"]

    def extract_categorie(self, response):
        return response.css('.breadcrumbs__item a::text').extract()[1:-1]

    def extract_description(self, response):
        return response.css('meta[itemprop="description"]::attr(content)').extract_first()

    def extract_image_urls(self, item_detail):
        return [img["large"] for img in item_detail["images"]]

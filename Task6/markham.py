import json
import re
from scrapy import Spider, Request
from w3lib import url
from Task6.items import Product


class MarkhamSpider(Spider):
    name = 'markham'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['markham.co.za']
    start_urls = ['https://www.markham.co.za']

    category_items_request_t = 'https://www.markham.co.za/search/ajaxResultsList.jsp?baseState={}&N={}'
    item_detail_request_t = 'https://www.markham.co.za/product/generateProductJSON.jsp?productId={}'

    def parse(self, response):
        category_urls = [self.category_items_request_t.format(category_id, category_id) for category_id in
                         response.css('.nav__item-title::attr(href)').re('-([\w+]+);')]
        yield from [Request(category_url, callback=self.parse_categories) for category_url in category_urls]

    def parse_categories(self, response):
        try:
            product_detail = json.loads(response.body).get("data")
        except:
            product_id = re.search('_/\w+-(.+)', response.url, re.DOTALL).group(1)
            return Request(self.item_detail_request_t.format(product_id), callback=self.parse_item)
        else:
            categories = self._extract_categories(product_detail)
            if categories:
                yield from [Request(url.add_or_replace_parameter(response.url, "N", category["value"]),
                                    callback=self.parse_categories) for category in categories]
            else:
                total_pages = json.loads(response.body)["data"]["totalPages"]
                yield from [Request(url.add_or_replace_parameter(response.url, "page", page_number),
                                    callback=self.parse_pagination)
                            for page_number in range(1, total_pages + 1)]

    def _extract_categories(self, product_detail):
        for categories in product_detail["filterSets"]:
            if categories["name"] == "Shop By Category":
                return categories["items"]

    def parse_pagination(self, response):
        item_detail = json.loads(response.body).get("data")
        products = item_detail["products"]
        yield from [Request(self.item_detail_request_t.format(product["id"]), callback=self.parse_item)
                    for product in products]

    def parse_item(self, response):
        item = Product()
        item_detail = json.loads(response.body)

        item["retailer_sku"] = item_detail.get("productId")
        item["name"] = item_detail.get("name")
        item["brand"] = item_detail.get("brand")
        item["url"] = response.urljoin(item_detail.get("pdpURL"))
        item["price"] = self.extract_price(item_detail)
        item["image_urls"] = self.extract_image_urls(item_detail)
        item["gender"] = "Men"
        item["skus"] = []

        skus_requests = []
        skus_requests.extend([Request(url.add_or_replace_parameter(response.url, "selectedColor", color["id"]),
                                      callback=self.parse_skus,
                                      meta={"item": item, "skus_requests": skus_requests, "color": color["name"]})
                              for color in item_detail["colors"]])

        return skus_requests.pop()

    def parse_skus(self, response):
        item = response.meta["item"]
        item_detail = json.loads(response.body)
        skus_requests = response.meta["skus_requests"]
        color_name = response.meta["color"]

        if item_detail.get("sizes"):
            for size in item_detail["sizes"]:
                sku = self._create_sku(color_name, size, item_detail.get("oldPrice"))
                item["skus"].append(sku)
        else:
            item["skus"] = self._create_sku(color_name, None, item_detail.get("oldPrice"))

        if skus_requests:
            return skus_requests.pop()

        return Request(item["url"], callback=self.parse_html_response, meta=response.meta)

    def _create_sku(self, color, size, old_price):
        sku = {"color": color,
               "size": size["name"] if size else "",
               "sku_id": f'{color}_{size["name"] if size else ""}'}

        if size and not size.get("available"):
            sku["out_of_stock"] = True

        if old_price:
            sku["previous_prices"] = [].append(self.extract_price(old_price))
            sku["currency"] = old_price[0]

        return sku

    def parse_html_response(self, response):
        item = response.meta["item"]
        product_description = response.css('script#product-detail-template::text').extract_first()
        item["description"] = re.search(r'<div class="product-detail__copy">[\r\n\t\s]+<p>(.+)</p>[\r\n\t\s]+'
                                        r'</div>[\r\n\t\s]+\|#', product_description, re.DOTALL).group(1)
        item["category"] = response.css('.breadcrumbs__item a::text').extract()[1:-1]
        return item

    def extract_price(self, item_detail):
        raw_price = re.search('([\d,]+)', item_detail.get("price"), re.DOTALL).group(1)
        return float(raw_price.replace(',', '')) * 100

    def extract_image_urls(self, item_detail):
        return [img["large"] for img in item_detail["images"]] if item_detail.get("images") else None

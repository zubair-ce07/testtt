import json
from urllib.parse import urlparse

import scrapy

from gluespider.spiders.mixin import Mixin
from gluespider.items import GluesProduct


class ParseSpider(scrapy.Spider, Mixin):
    product_api = 'http://www.gluestore.com.au/ppistock/ajax/updateSizeSelector/mainProductId/'
    name = 'parse_spider'
    seen_ids = list()

    def parse(self, response):
        retailer_id = self.product_retailer(response)
        if self.is_seen(retailer_id):
            return self.next_action(response)

        self.seen_ids.append(retailer_id)
        product = GluesProduct()
        product["genders"] = set()
        product["category"] = self.product_category(response)
        product["description"] = self.product_descriptions(response)
        product["care"] = self.product_cares(response)
        product["retailer_sku"] = retailer_id
        product["name"] = self.product_name(response).strip()
        product["brand"] = self.product_brand(response)
        product["market"] = "AU"
        product["retailer"] = "glue-au"
        product["url"] = response.url
        product["skus"] = dict()
        response.meta["product"] = product
        self.product_genders(response)
        response.meta["remaining_request"] = list()
        response.meta[
            "remaining_request"] += self.create_sku_requests(response)
        response.meta["remaining_request"].append(self.parse_skus(response))

        return self.next_action(response)

    def parse_sizes(self, response):
        if(response.text):
            sizes = json.loads(response.text)
            product = response.meta.get("product")
            sku = response.meta.get("sku")
            skus = product.get("skus")
            for size in sizes:
                product_sku = dict()
                product_sku["price"] = sku.get("price")
                product_sku["currency"] = sku.get("currency")
                product_sku["colour"] = sku.get("colour")
                product_sku["size"] = size.get("size")
                if 0 == size.get("qty"):
                    product_sku["out_of_stock"] = True
                key = f'{product_sku["colour"]}_{product_sku["size"]}_{sku["product_id"]}'
                skus[key] = product_sku
        return self.next_action(response)

    def parse_skus(self, response):
        self.product_sku_images(response)
        self.product_genders(response)
        product_sku = dict()
        product_sku["price"] = self.product_price(response)
        product_sku["currency"] = self.product_currency(response)
        product_sku["colour"] = self.product_current_colour_name(response)
        product_sku["product_id"] = self.product_retailer(response)
        request = self.create_size_request(response)
        request.meta["sku"] = product_sku
        remaining_request = response.meta.get("remaining_request")
        remaining_request.append(request)
        response.meta["remaining_request"] = remaining_request
        return self.next_action(response)

    def create_sku_requests(self, response):
        multiple_requests = set()
        for next_page in response.css('#colors .product-color > a'):
            multiple_requests.add(response.follow(next_page, self.parse_skus))
        return multiple_requests

    def create_size_request(self, response):
        product_id = self.product_retailer(response)
        content_type = 'application/x-www-form-urlencoded; charset=UTF-8'
        request = scrapy.Request(self.product_api+product_id,
                                 headers={
                                     'Content-Type': content_type},
                                 callback=self.parse_sizes)
        return request

    def product_sku_images(self, response):
        product = response.meta.get("product")
        images = product.get("image_urls", list())
        images = list(set().union(images, self.product_images(response)))
        product["image_urls"] = images

    def product_genders(self, response):
        catogories = self.product_category(response)
        name = self.product_name(response)
        if "Unisex" in name:
            response.meta["product"]["genders"].add("unisex-adults")
        elif "Women" in name:
            response.meta["product"]["genders"].add("women")
        elif "Men" in name:
            response.meta["product"]["genders"].add("men")
        elif [category for category in catogories if "Unisex" in category]:
            response.meta["product"]["genders"].add("unisex-adults")
        elif [category for category in catogories if "Women" in category]:
            response.meta["product"]["genders"].add("women")
        elif [category for category in catogories if "Men" in category]:
            response.meta["product"]["genders"].add("men")

    def product_category(self, response):
        catogories = response.css(
            '#shop_breadcrumbs li span::text').extract()
        return [category.strip() for category in catogories]

    def product_descriptions(self, response):
        descriptions_css = ".std h5::text"
        descriptions = response.css(descriptions_css).extract()
        return [description.strip() for description in descriptions]

    def product_cares(self, response):
        care_css = '.std:not(first)::text'
        cares = response.css(care_css).extract()
        return [care.strip() for care in self.remove_duplicates(cares)]

    def product_retailer(self, response):
        css = '.product-form [name="product"]::attr(value)'
        return response.css(css).extract_first()

    def product_images(self, response):
        images_css = '.more-views img::attr(src)'
        return response.css(images_css).extract()

    def product_name(self, response):
        name_css = ".product-name h1::text"
        return response.css(name_css).extract_first()

    def product_brand(self, response):
        brand_css = ".product-view-brand::attr(alt)"
        return response.css(brand_css).extract_first()

    def product_price(self, response):
        price_xpath = './/meta[@property="og:price:amount"]/@content'
        price = response.xpath(price_xpath).extract_first()
        price = price.replace('.', '')
        return int(price)

    def product_currency(self, response):
        currency_xpath = './/meta[@property="og:price:currency"]/@content'
        return response.xpath(currency_xpath).extract_first()

    def product_current_colour_name(self, response):
        selector = ".product-color.active img::attr(title)"
        current_colour = response.css(selector).extract_first()
        return current_colour

    def is_seen(self, _id):
        [product_id for product_id in self.seen_ids if _id == product_id]

    def remove_duplicates(self, items):
        no_dupes = set(items)
        return list(no_dupes)

    def next_action(self, response):
        sub_requests = response.meta.get("remaining_request")
        if not sub_requests:
            return response.meta.get("product")

        request = sub_requests.pop()
        request.meta["product"] = response.meta.get("product")
        request.meta["information"] = response.meta.get("information")
        request.meta["remaining_request"] = response.meta.get(
            "remaining_request")
        return request

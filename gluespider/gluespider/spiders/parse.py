import json
import scrapy

from gluespider.spiders.mixin import Mixin
from gluespider.items import GluesProduct


class ParseSpider(scrapy.Spider, Mixin):
    product_api = 'http://www.gluestore.com.au/ppistock/ajax/updateSizeSelector/mainProductId/'
    name = 'parse_spider'
    seen_ids = list()

    def parse(self, response):
        retailer_id = self.product_retailer(response)
        if retailer_id in self.seen_ids:
            return

        self.seen_ids.append(retailer_id)
        product = GluesProduct()
        response.meta["product"] = product
        product["category"] = self.product_category(response)
        product["description"] = self.product_descriptions(response)
        product["care"] = self.product_cares(response)
        product["name"] = self.product_name(response).strip()
        product["brand"] = self.product_brand(response)
        product["image_urls"] = self.product_images(response)
        product["gender"] = self.product_gender(product, response)
        product["retailer_sku"] = retailer_id
        product["url"] = response.url
        product["market"] = "AU"
        product["retailer"] = "glue-au"

        if self.product_size_exist(response):
            product["skus"] = dict()
            requests = self.create_sku_requests(
                response) + [self.create_size_request(response)]
            response.meta[
                "remaining_request"] = requests
        else:
            response.meta[
                "remaining_request"] = self.create_sku_requests(response)
            key, sku = self.product_default_size(response)
            product["skus"][key] = sku

        return self.next_action(response)

    def parse_sizes(self, response):
        sizes = json.loads(response.text)
        product = response.meta.get("product")
        skus = product.get("skus")
        for size in sizes:
            key, details = self.product_sku_details(size, response)
            skus[key] = details
        return self.next_action(response)

    def parse_skus(self, response):
        product = response.meta.get("product")
        product["category"] += self.product_category(response)
        product["image_urls"] += self.product_images(response)
        product["gender"] = self.product_gender(product, response)
        remaining_request = response.meta.get("remaining_request")
        remaining_request.append(self.create_size_request(response))
        return self.next_action(response)

    def create_sku_requests(self, response):
        colour_request = [response.follow(
            c, self.parse_skus) for c in response.css('#colors .product-color > a')]
        return colour_request

    def product_default_size(self, response):
        product_sku = dict()
        product_sku["price"] = self.product_price(response)
        product_sku["currency"] = self.product_currency(response)
        if self.product_out_of_stock(response):
            product_sku["out_of_stock"] = True
        key = f'{self.product_retailer(response)}'
        return key, product_sku

    def create_size_request(self, response):
        product_sku = dict()
        product_sku["price"] = self.product_price(response)
        product_sku["currency"] = self.product_currency(response)
        product_sku["colour"] = self.product_current_colour_name(response)
        product_sku["product_id"] = self.product_retailer(response)
        product_id = self.product_retailer(response)
        content_type = 'application/x-www-form-urlencoded; charset=UTF-8'
        request = scrapy.Request(self.product_api + product_id,
                                 headers={
                                     'Content-Type': content_type},
                                 meta={"sku": product_sku},
                                 callback=self.parse_sizes)
        return request

    def product_out_of_stock(self, response):
        out_of_stock_css = '.out-of-stock'
        stock = response.css(out_of_stock_css).extract_first()
        return stock

    def product_sku_details(self, size, response):
        sku = response.meta.get("sku")
        product_sku = dict()
        product_sku["price"] = sku.get("price")
        product_sku["currency"] = sku.get("currency")
        product_sku["colour"] = sku.get("colour")
        product_sku["size"] = size.get("size")
        if not size.get("qty"):
            product_sku["out_of_stock"] = True
        key = f'{product_sku["colour"]}_{product_sku["size"]}_{sku["product_id"]}'
        return key, product_sku

    def product_size_exist(self, response):
        size_css = '.input-box.sizes'
        sizes = response.css(size_css).extract()
        return sizes

    def product_gender(self, product, response):
        gender = product.get("gender")
        catogories = self.product_category(response)
        name = self.product_name(response).strip()
        in_women_category = [cat for cat in catogories if "Women" in cat]
        in_mens_category = [cat for cat in catogories if "Men" in cat]
        if "unisex-adults" == gender:
            return gender
        if "Unisex" in name or "Unisex" in catogories:
            return "unisex-adults"
        if "men" == gender and ("Women" in name or in_women_category):
            return "unisex-adults"
        if "women" == gender and ("Men" in name or in_mens_category):
            return "unisex-adults"
        if "Women" in name or in_women_category:
            return "women"
        if "Men" in name or in_mens_category:
            return "men"

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
        brand = response.css(brand_css).extract_first()
        if brand:
            return brand
        else:
            brand_css = ".static-links a::text"
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

    def remove_duplicates(self, items):
        no_dupes = set(items)
        return list(no_dupes)

    def next_action(self, response):
        sub_requests = response.meta.get("remaining_request")
        if not sub_requests:
            return response.meta.get("product")

        request = sub_requests.pop()
        request.meta["product"] = response.meta.get("product")
        request.meta["remaining_request"] = response.meta.get(
            "remaining_request")
        return request

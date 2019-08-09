import copy
import json
import re

import scrapy


class Parser:

    def next_page(self, response):
        pdb.set_trace()
        page_data = json.loads(response.text)
        url = response.meta["url"]
        hits = int(page_data["zones"][0]["data"]["metadata"]["hits"])
        hitsperpage = int(page_data["zones"][0]["data"]["metadata"]["hitsperpage"])
        first = int(page_data["zones"][0]["data"]["metadata"]["first"])
        if (first + hitsperpage) < hits:
            url, page = url.split('?')
            if first == 0:
                next_page = 1
            else:
                next_page = (first / hitsperpage) + 1
            url = f"{url}?page={next_page}"
            yield scrapy.Request(url, callback=self.parse)

    def prepare_params(self, response):
        params = {
            "siteid": response.css(".page-collection::attr(data-attraqt-site-id)").extract_first(),
            "pageurl": response.url,
            "zone0": re.findall(r'data-attraqt-page-type="(\w+)"', response.text)[0],
            "sid": "db4jx5c7ut",
            "uid": "ATT_1564987309510_06771628066488389",
            "config_category": re.findall(r'data-attraqt-category="(\w+[-?\w*]*)"', response.text)[0],
            "config_categorytree": re.findall(r'data-attraqt-category="(\w+[-?\w*]*)"', response.text)[0]
        }
        if params["zone0"] == "category":
            params["fields_category"] = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"
            params["category_hitsperpage"] = 60
            params["category_page"] = int(re.findall(r"page=(\d+)$", response.url)[0]) + 1
        else:
            params["fields_prodpage_bottom"] = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"
            params["prodpage_bottom_hitsperpage"] = 15
            params["sku"] = re.findall(r'"resourceId":(\d+)}', response.text)[0]
        return params

    def retailer_sku(self, response):
        return response.css(".product-sku > *::text").extract_first()

    def category(self, response):
        categories_str = re.findall("Categories: (.+),", response.text)[0]
        return re.findall(r'"\s*([^"]*?)\s*"', categories_str)

    def brand(self, response):
        return re.findall(r'Brand: "(.+)",', response.text)[0]

    def url(self, response):
        return response.url

    def product_name(self, response):
        return re.findall(r'Name: "(.+)",', response.text)[0]

    def description(self, response):
        return response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()

    def care(self, response):
        description = response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()
        care_raw = ["%", "machine", "wash", "wipe", "clean", "faux", "leather", "hand"]
        return [d for d in description if any(cr in d.lower() for cr in care_raw)]

    def image_urls(self, response):
        return response.css(".slide-item img::attr(src)").getall()

    def price(self, response):
        price_text = response.css("*[data-handle=sale-price]::text").extract_first()
        return int(price_text.replace(u'\u00A3', '').replace(".", ''))

    def old_price(self, response):
        prices = response.css(".old-price::text").extract()
        prices = list(map(lambda s: s.replace(u'\u00A3', '').replace(".", ''), prices))
        return list(map(int, prices))

    def currency(self, response):
        return response.css('*[property=og\:price\:currency]::attr(content)').extract_first()

    def gender(self, response):
        return "female"

    def color(self, response, variants):
        for product in variants["products"]:
            if product['handle'] in response.url:
                return product["colour_name"]

    def sizes(self, response):
        quantities = [int(q) for q in response.css(".product-size * option::attr(data-quantity)").extract()]
        sizes = [s.strip() for s in response.css(".size-list .value::text").extract() if s.strip()]
        size_quantity = []
        for size, quantity in zip(sizes, quantities):
            size_quantity.append((size, quantity))
        return size_quantity

    def skus(self, response):
        product = response.meta["product"]
        colours = json.loads(response.text)
        for colour in colours["products"]:
            request = scrapy.Request("https://www.isawitfirst.com/products/" + colour["handle"], callback=self.variants)
            request.meta["product"] = product
            request.meta["variants_info"] = colours
            yield request

    def variants(self, response):
        product = response.meta["product"]
        variants = response.meta["variants_info"]
        color = self.color(response, variants)
        price = self.price(response)
        old_price = self.old_price(response)
        currency = self.currency(response)
        sizes = self.sizes(response)
        sku = {}
        for size, quantity in sizes:
            sku["colour"] = color
            sku["price"] = price
            sku['old_price'] = old_price
            sku["currency"] = currency
            sku["size"] = size
            if quantity == 0:
                sku["out_of_stock"] = True
            else:
                sku["out_of_stock"] = False
            product["skus"][f"{color}_{size}"] = copy.deepcopy(sku)
        if len(product["skus"]) == len(variants["products"]) * len(sizes):
            yield product

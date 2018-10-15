import json
import re

import scrapy
from damart.items import DamartItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DamartSpider(CrawlSpider):
    name = "damart"
    allowed_domains = ["www.damart.co.uk"]
    start_urls = ["http://www.damart.co.uk/"]
    rules = (
            Rule(LinkExtractor(
                allow=["/C-", "/I-Page"], deny=("/NW-")),
                callback="parse"),
            Rule(LinkExtractor(
                restrict_css=[".photo-data"]),
                callback="parse_product")
            )

    def parse_product(self, response):
        """Getting all the product details and storind it in the item"""
        product_details = {
            "_id": self.find_id(response),
            "brand": "Damart",
            "care": self.find_care_text(response),
            "category": self.find_category(response),
            "description": self.find_description(response),
            "image_urls": self.extract_image_urls(response),
            "name": self.find_name(response),
            "retailer_sku": "P-" + self.find_id(response),
            "skus": {},
            "url": {response.url}
        }
        item = DamartItem(product_details)

        color_names = self.find_color_names(response)
        color_urls = self.extract_color_urls(response)
        if color_urls:
            yield scrapy.Request(
                url=color_urls.pop(0),
                callback=self.find_color_variations,
                headers={
                    "X-Requested-With": "XMLHttpRequest"},
                meta={
                    "item": item,
                    "color_names": color_names,
                    "color_urls": color_urls,
                }
            )
        else:
            yield item

    def develop_skus(self, response):
        """Develops skus sturcture and returns it"""
        color_name = (response.meta["color_names"]).pop(0)
        details = self.find_sizes_and_stock_availability(response)
        price = self.find_price(response)
        skus = {}

        for i, size in enumerate(details["sizes"]):
            if "length" in details.keys():
                for length in details["length"]:
                    skus["{}_{}_{}".format(
                        color_name, size, length["text"]
                        )] = {
                        "color": color_name,
                        "currency": "Dollar",
                        "price": price,
                        "size": size
                    }
            else:
                skus["{}_{}".format(color_name, size)] = {
                    "color": color_name,
                    "currency": "Dollar",
                    "price": price,
                    "size": size
                }
            if details["in_stock"]:
                skus[
                    "{}_{}".format(color_name, size)
                    ]["in_stock"] = details["in_stock"][i]
        return skus

    def find_sizes_and_stock_availability(self, response):
        """Parse the json object and returns the specified
        size and stock description"""
        json_data = json.loads(response.body.decode("utf-8"))
        component = json_data["inits"][2]["initDDdSlickComponent"]
        ddData = component[0]["ddData"]
        info = {
            "sizes": [],
            "in_stock": []
        }
        if len(component) > 1:
            length = component[1]["ddData"]
            info["length"] = length
        for details in ddData:
            info["sizes"].append(details["text"])
            if "description" in details.keys():
                if "Available" in details["description"]:
                    info["in_stock"].append(True)
                else:
                    info["in_stock"].append(False)
        return info

    def find_price(self, response):
        """Get's the price attribute from the jason data for
        each color"""
        json_data = json.loads(response.body.decode('utf-8'))
        zone = json_data["zones"]

        zone["priceZone"]
        new_response = response.replace(
            body=zone["priceZone"]
            )
        price = new_response.css(
            ".sale::text, .sale span::text"
        ).extract()
        return "".join(price).split()

    def find_color_variations(self, response):
        """Updates the skus according to the provided colors in meta"""
        if "item" in response.meta:
            color_names = response.meta["color_names"]
            color_urls = response.meta["color_urls"]
            item = response.meta["item"]
            skus = self.develop_skus(response)
            item["skus"].update(skus)

            if color_urls:
                yield scrapy.Request(
                    url=color_urls.pop(0),
                    callback=self.find_color_variations,
                    headers={
                        "X-Requested-With": "XMLHttpRequest"},
                    meta={
                        "item": item,
                        "color_names": color_names,
                        "color_urls": color_urls,
                    }
                )
            else:
                yield item

    def find_next_page(self, response):
        return response.urljoin(
            response.css(".next::attr(href)").extract_first()
        )

    def extract_product_urls(self, response):
        urls = response.css(".photo-data a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def find_name(self, response):
        return response.css(".name::text").extract_first()

    def find_id(self, response):
        return re.findall(r"P-(\d*)", response.url)[0]

    def find_description(self, response):
        description = list(set(response.css(
            ".product-info li::text, .para_hide::text"
        ).extract()))
        return [d.strip() for d in description]

    def find_care_text(self, response):
        product_care = response.css("#careAdvicesZoneNew div::text").extract()
        return [c.strip() for c in product_care if not c == " "]

    def find_category(self, response):
        return response.css(
            ".breadcrum span:nth-child(4) a span::text").extract_first()

    def extract_image_urls(self, response):
        images = response.css(".thumblist a::attr(href)").extract()
        return [response.urljoin(image) for image in images]

    def find_color_names(self, response):
        return response.css(".picto_color img::attr(alt)").extract()

    def extract_color_urls(self, response):
        color_urls = response.css(".picto_color a::attr(href)").extract()
        return [response.urljoin(url) for url in color_urls]

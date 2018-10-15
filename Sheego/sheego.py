import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sheego.items import SheegoItem, SheegoItemLoader


class SheegoSpider(CrawlSpider):
    name = "sheego"
    allowed_domains = ["www.sheego.de"]
    start_urls = ["https://www.sheego.de/"]

    rules = (
        Rule(LinkExtractor(
            allow=("/damenmode/$"),
            deny=("/damenmode-sale/")),
            callback="parse_product_list", follow=True),

        Rule(LinkExtractor(
            allow=("/?pageNr=")),
            callback="parse_product_list", follow=True),

            )

    def parse_product_list(self, response):
        product_urls = self.extract_product_urls(response)
        for url in product_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
                dont_filter=True
            )

    def extract_product_urls(self, response):
        urls = response.css(".js-product__link::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def find_details(self, response):
        details = response.css(
            "input.js-webtrends-data[type=hidden]::attr(data-webtrends)"
            ).extract_first()
        return json.loads(details)

    def find_sizes(self, response):
        sizes = response.css(".sizespots__item::text").extract()
        sizes = [re.sub("\s+", " ", s).strip() for s in sizes if s]
        return [s for s in sizes if s]

    def extract_image_urls(self, response):
        urls = response.css(
            ".p-details__image__thumb__container a::attr(href)"
            ).extract()
        return [response.urljoin(url) for url in urls]

    def has_more_colors(self, response):
        """Checks if the meta has been initailized with more colors"""
        if 'colors' in response.meta:
            return True
        else:
            return False

    def develop_skus(self, response):
        details = self.find_details(response)
        sizes = self.find_sizes(response)
        image_urls = self.extract_image_urls(response)
        color_name = self.find_color_name(response)
        skus = {}

        for size in sizes:
            skus["{}_{}".format(color_name, size)] = {
                "color": color_name,
                "currency": "EUR",
                "price": details["productPrice"],
                "rating": details["productRating"],
                "Availability": details["productAvailability"],
                "size": size
            }
        if self.has_more_colors(response):
            return self.find_color_variations(response, skus, image_urls)

    def find_color_variations(self, response, skus, image_urls):
        item_loader = response.meta["item_loader"]
        item_loader.add_value("skus", skus)
        item_loader.add_value("image_urls", image_urls)
        item_loader.add_value("url", response.url)

        if len(response.meta["colors"]) == 0:
            yield item_loader.load_item()
        else:
            colors = response.meta["colors"]
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.develop_skus,
                    meta={"colors": colors,
                          "item_loader":  item_loader})

    def find_colors_variant_id(self, response):
        colors = response.css(
            ".colorspots__item img::attr(data-src)").extract()
        variant_url = []
        for color in colors:
            _id = re.findall(r"//(\d+)-", color)[0]
            _id = f"{_id[:6]}000{_id[6:]}"
            _id = f"000000{_id}018000"
            variant_url.append(_id)
        return [f"{response.url}/variantid={url}" for url in variant_url]

    def find_color_name(self, response):
        return response.css("span.at-dv-color::text").extract_first()

    def parse_product(self, response):
        details = self.find_details(response)

        loader = SheegoItemLoader(item=SheegoItem(), response=response)
        loader.add_value("_id", details["productId"])
        loader.add_value("name", details["productName"])
        loader.add_css("categories", "span[itemprop=name]::text")
        loader.add_value("brand", "Sheego Style")
        loader.add_value("retailer_sku", details["productId"])
        loader.add_value("gender", "Female")
        loader.add_css("description", ".details__box__desc p::text")
        loader.add_css("care", ".p-details__material td::text")

        colors = self.find_colors_variant_id(response)
        if len(colors):
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.develop_skus,
                    meta={"colors": colors,
                          "item_loader":  loader})
        else:
            yield loader.load_item()

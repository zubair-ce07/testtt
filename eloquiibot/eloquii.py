# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com']
    start_urls = ['https://www.eloquii.com']
    listings_css = ['#nav_menu', '.row.justify-content-center.mt-5']
    products_css = ".product-images a"
    rules = (Rule(LinkExtractor(restrict_css=listings_css)),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_product(self, response):
        product = EloquiiProduct()
        product["product_id"] = self.product_id(response)
        product["brand"] = 'Eloquii'
        product["name"] = self.product_name(response)
        product["category"] = self.product_category(response)
        product["description"] = self.product_description(response)
        product["url"] = response.url
        product["image_urls"] = self.image_urls(response)
        product["skus"] = {}
        product["merch_info"] = self.merch_info(response, product["name"] + product["description"])
        if "COMING SOON" not in product["merch_info"]:
            product["skus"] = self.skus(response)
        yield product

    def product_id(self, response):
        id_css = "#yotpo-bottomline-top-div::attr(data-product-id)"
        return response.css(id_css).extract_first()

    def product_name(self, response):
        name_css = "#yotpo-bottomline-top-div::attr(data-name)"
        return response.css(name_css).extract_first()

    def product_category(self, response):
        category_css = "#yotpo-bottomline-top-div::attr(data-bread-crumbs)"
        return response.css(category_css).extract_first()

    def product_description(self, response):
        description_css = "[name=description]::attr(content)"
        return response.css(description_css).extract_first()

    def image_urls(self, response):
        image_urls_css = ".productthumbnails img::attr(src),.productimagearea img::attr(src)"
        image_urls = list(set(response.css(image_urls_css).extract()))
        image_urls = [response.urljoin(i.replace('small', 'large', 1)) for i in image_urls]
        return image_urls

    def merch_info(self, response, soup):
        merch_info = []
        merch_names = ["limited", "special edition", "discounted"]
        merch_info = [i for i in merch_names if i in soup]
        if bool(re.search(r'\'COMINGSOON\': (true)', response.text)):
            merch_info.append("COMING SOON")
        return merch_info

    def skus(self, response):
        skus = {}
        colours = response.css(".swatchesdisplay a::attr(title)").extract()
        sizes_css = "#product_detail_size_drop_down_expanded a::attr(title)"
        sizes = response.css(sizes_css).extract()
        sizes = sizes[1:]
        prices = self.product_pricing(response)
        for colour in colours:
            for size in sizes:
                skus[colour + '_' + size] = {
                    "colour": colour,
                    "size": size,
                }
                skus[colour + '_' + size].update(prices)
        return skus

    def product_pricing(self, response):
        prices = {}
        previous_price = response.css(".priceGroup strike::text").re_first(r'(\d+\.\d+)')
        prices["price"] = response.css(".priceGroup span::text").extract_first()
        prices["currency"] = re.search(r'([^0-9.])', prices["price"]).group(1)
        prices["price"] = float(re.search(r'(\d+\.\d+)', prices["price"]).group(1))
        if previous_price:
            prices["previous_price"] = previous_price
        return prices

# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com']
    start_urls = ['https://www.eloquii.com']
    rules = (Rule(LinkExtractor(
        restrict_css=["#nav_menu a",
                      ".row.justify-content-center.mt-5"])),
             Rule(LinkExtractor(restrict_css=".product-images a"),
                  callback='parse_product'))

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
        product["merch_info"] = self.merch_info(response)
        if "COMING SOON" not in product["merch_info"]:
            product["skus"] = self.skus(response)
        yield product

    def product_id(self, response):
        return response.css("#yotpo-bottomline-top-div::attr(data-product-id)"
                            ).extract_first()

    def product_name(self, response):
        return response.css("#yotpo-bottomline-top-div::attr(data-name)"
                            ).extract_first()

    def product_category(self, response):
        return response.css(
            "#yotpo-bottomline-top-div::attr(data-bread-crumbs)"
        ).extract_first()

    def product_description(self, response):
        return response.css("[name=description]::attr(content)"
                            ).extract_first()

    def image_urls(self, response):
        image_url = response.css(".productthumbnails img::attr(src)"
                                 ).extract()
        image_url = [response.urljoin(i.replace('small', 'large', 1)) for i in
                     image_url]
        if not image_url:
            image_url = response.css(".productimagearea img::attr(src)"
                                     ).extract_first()
            image_url = response.urljoin(image_url)
        return image_url

    def merch_info(self, response):
        product_merch_info = []
        product_merch_info.append(response.css(
            "h3.text-24.font-demi.mb-3::text").extract_first(default=''))
        product_merch_info.append(response.css(".finalsale::text"
                                               ).extract_first(default=''))
        if bool(re.search(r'\'COMINGSOON\': (true)',
                          response.text)):
            product_merch_info.append("COMING SOON")
        return product_merch_info

    def skus(self, response):
        skus = {}
        colours = response.css(".swatchesdisplay a::attr(title)").extract()
        sizes = response.css(
            "#product_detail_size_drop_down_expanded a::attr(title)").extract()
        sizes = sizes[1:]
        previous_price = response.css(".priceGroup strike::text"
                                      ).re_first(r'(\d+\.\d+)')
        price = response.css(".priceGroup span::text").extract_first()
        currency = ''
        if price:
            currency = re.search(r'([^0-9.])', price).group(1)
            price = float(re.search(r'(\d+\.\d+)', price).group(1))
        for colour in colours:
            for size in sizes:
                skus[colour + '_' + size] = {
                    "colour": colour,
                    "currency": currency,
                    "previous_price": previous_price,
                    "price": price,
                    "size": size,
                }
        return skus

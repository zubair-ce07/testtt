import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kidsbrandstore.items import KidsbrandstoreItem


class BrandStoreSpider(CrawlSpider):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']
    categories_css = [".paginationControl", "div[id=bottom-types]", "div[id=bottom-brands]"]
    products_css = ".bottom-product-grid"

    rules = (
        Rule(LinkExtractor(deny_extensions=['html'], restrict_css=categories_css)),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        )

    def parse_item(self, response):
        product = KidsbrandstoreItem()
        product['retailer_sku'] = self.retailer_sku(response)
        product['gender'] = self.gender(response)
        product['category'] = self.category(response)
        product['brand'] = self.brand(response)
        product['url'] = self.url(response)
        product['name'] = self.product_name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        product['skus'] = self.skus(response)
        product['price'] = self.price(response)
        product['currency'] = self.currency(response)
        return product

    def retailer_sku(self, response):
        return response.css('.product_id::text').extract_first()

    def category(self, response):
        return list(filter(None, response.css('.category::text').extract_first().split("/")))

    def brand(self, response):
        return response.css('.brand::text').extract_first()

    def url(self, response):
        return response.url

    def product_name(self, response):
        return response.css('.name::text').extract_first()

    def description(self, response):
        return response.css('.description::text').extract()

    def care(self, response):
        return response.xpath('//*[*[@class="product-material"]]/text()').extract()

    def image_urls(self, response):
        return response.css('figure a img::attr(src)').extract()

    def price(self, response):
        price_text = response.css('.price::text').extract_first(default="")
        return float(price_text.replace(",", '.'))

    def currency(self, response):
        return response.css('.price_currency_code::text').extract_first()

    def gender(self, response):
        raw_gender = "".join(response.css('div[id=product-list-also-check] p a::text').extract())
        gender_pairs = {"jungen": "boys", "mädchen": "girls"}
        for key, value in gender_pairs.items():
            if key in raw_gender:
                return value
        return "unisex-kids"

    def color(self, response):
        title = response.css('.desktop-header::text').extract_first(default="")
        if title:
            return re.findall("(\w*\.$)", title)[0].replace(".", '')

    def sizes(self, response):
        return response.css('.attribute-title::text').extract()

    def skus(self, response):
        skus = []
        color = self.color(response)
        sizes = self.sizes(response)
        price = self.price(response)
        currency = self.currency(response)

        for size in sizes:
            sku = {}
            if color:
                sku['colour'] = color
            sku['price'] = price
            sku["currency"] = currency
            sku['size'] = size
            sku['sku_id'] = f"{color}_{size}"
            skus.append(sku)
        return skus

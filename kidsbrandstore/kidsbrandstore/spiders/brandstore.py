import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kidsbrandstore.items import KidsbrandstoreItem


class BrandStoreSpider(CrawlSpider):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']
    brands_categories_css = (".paginationControl", "div[id=bottom-types]", "div[id=bottom-brands]")
    products_css = ".bottom-product-grid"

    rules = (
        Rule(LinkExtractor(deny_extensions=['html'], restrict_css=brands_categories_css)),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        )

    def parse_item(self, response):
        product = KidsbrandstoreItem()
        product['retailer_sku'] = self.parse_retailer_sku(response)
        product['gender'] = self.parse_gender(response)
        product['category'] = list(filter(None, self.parse_category(response)))
        product['brand'] = self.parse_brand(response)
        product['url'] = self.parse_url(response)
        product['name'] = self.parse_name(response)
        product['description'] = self.parse_description(response)
        product['care'] = self.parse_care(response)
        product['image_urls'] = self.parse_image_urls(response)
        product['skus'] = self.parse_skus(response)
        product['price'] = self.parse_price(response)
        product['currency'] = self.parse_currency(response)
        yield product

    def parse_retailer_sku(self, response):
        return response.css('.product_id::text').extract_first()

    def parse_category(self, response):
        return response.css('.category::text').extract_first().split("/")

    def parse_brand(self, response):
        return response.css('.brand::text').extract_first()

    def parse_url(self, response):
        return response.url

    def parse_name(self, response):
        return response.css('.name::text').extract_first()

    def parse_description(self, response):
        return response.css('.description::text').extract()

    def parse_care(self, response):
        return (response.xpath('//span[@class="product-material"]/../text()').extract())

    def parse_image_urls(self, response):
        return response.css('figure a img::attr(src)').extract()

    def parse_price(self, response):
        return float(response.css('.price::text').extract_first().replace(",", '.'))

    def parse_currency(self, response):
        return response.css('.price_currency_code::text').extract_first()

    def parse_gender(self, response):
        product_list = "".join(response.css('div[id=product-list-also-check] p a::text').extract())
        if response.css('svg').extract():
            return "unisex-kids"
        elif "jungen" in product_list:
            return "boys"
        elif "mädchen" in product_list:
            return "girls"
        else:
            return "unisex-kids"

    def parse_color(self, response):
        if response.css('.desktop-header::text').extract():
            return (re.search("(\w*\.$)",
                    response.css('.desktop-header::text').extract_first()).group(1).replace(".", ''))

    def parse_sizes(self, response):
        return response.css('.attribute-title::text').extract()

    def parse_skus(self, response):
        skus = []
        color = self.parse_color(response)
        sizes = self.parse_sizes(response)
        price = self.parse_price(response)
        currency = self.parse_currency(response)

        for size in sizes:
            product_dictionary = {}
            if color:
                product_dictionary['colour'] = color
            product_dictionary['price'] = price
            product_dictionary["currency"] = currency
            product_dictionary['size'] = size
            product_dictionary['sku_id'] = f"{color}_{size}"
            skus.append(product_dictionary)
        return skus

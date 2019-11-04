import scrapy
from scrapy.http.request import Request
import re
from asics.items import AsicsItem
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule


class AsicsSpider(CrawlSpider):
    name = 'asics'
    allowed_domains = ["asics.com"]
    product = AsicsItem()
    product_variant_links = []
    start_urls = ['http://www.asics.com/us/en-us/']
    base_url = 'http://www.asics.com/us/en-us/'
    rules = [
        Rule(LinkExtractor(
            allow=r'us/en-us/\w+/\w+/[\w.]+',
            restrict_css=(['.show-menu-item', '.product-image a', '.page-next'])
        ),
            callback="parse_products", follow=True)
    ]

    def parse_products(self, response):
        result = re.search(r'us/en-us/[\w_-]+/[\w_-]+/[\w._-]+.html[\w]*', response.url)
        print(f"IN Parse Singe: {response.url}  {result}")
        if result:
            self.product['description'] = AsicsSpider.description(response)
            self.product['product_name'] = AsicsSpider.product_name(response)
            self.product['category'] = AsicsSpider.product_category(response)
            self.product['image_urls'] = []
            self.product['skus'] = {}
            self.product['date'] = datetime.now().timestamp()
            self.product['price'] = AsicsSpider.price(response)
            self.product['url'] = response.url
            self.product['original_url'] = response.url

            script = response.xpath('//script[@type="text/javascript"]')
            self.product['brand'] = AsicsSpider.brand(script)
            self.product['currency'] = AsicsSpider.currency(script)
            self.product['lang'] = AsicsSpider.lang(script)
            self.product['gender'] = AsicsSpider.gender(script)

            self.product_variants_links = response.css(".js-color::attr(href)").getall()[1:]
            for product in self.parse_product(response):
                if not isinstance(product, Request):
                    yield product

    def parse_product(self, response):
        print(self.product)
        self.product['image_urls'] += AsicsSpider.image_urls(response)
        self.product['skus'].update(AsicsSpider.parse_sku(response))

        if len(self.product_variant_links) > 0:
            page = self.product_variant_links[0]
            del self.product_variant_links[0]
            yield response.follow(page, callback=self.parse_B)
        else:
            yield self.product

    @staticmethod
    def product_name(response):
        product_name = response.css(".pdp-top__product-name::text").get()
        if product_name:
            return product_name.strip()
        return response.css(".pdp-top__product-name::text").get().strip()

    @staticmethod
    def product_category(response):
        # product_category = response.css(".product-classification span::text").get()
        # if product_category:
        #     return product_category.strip()
        return [response.css(".product-classification span::text").get()]

    @staticmethod
    def description(response):
        # description = response.css(".product-info-section-inner::text").get()
        # if description:
        #     return description.strip()
        return response.css(".product-info-section-inner::text").get().strip()

    @staticmethod
    def image_urls(response):
        images = response.css(".thumbnail-link::attr(href)").getall()
        if '#' in images:
            images.remove('#')
        return images

    @staticmethod
    def product_category(response):
        return [response.css(".product-classification span::text").get()]

    @staticmethod
    def price(response):
        return response.css(".price-sales::text").extract()[1].strip()[1:]

    @staticmethod
    def brand(script):
        return script.re(r'"brand": "(\w+)"')

    @staticmethod
    def currency(script):
        return script.re(r'"currency": "(\w+)"')

    @staticmethod
    def lang(script):
        return script.re(r'"language": "(\w+)"')

    @staticmethod
    def gender(script):
        return script.re(r'"product_gender": \[\n +"(\w+)"')

    @staticmethod
    def sku(response):
        return response.css(".product-number span+ span::text").get().strip()

    @staticmethod
    def colour(response):
        return response.css(".variants__header--light::text").get().strip()

    @staticmethod
    def sku_sizes(response):
        return response.css(".variation-group-value .js-ajax::text").getall()

    @staticmethod
    def parse_sku(response):
        skus = {}
        product_sku = AsicsSpider.sku(response)
        product_colour = AsicsSpider.colour(response)
        product_sku_sizes = AsicsSpider.sku_sizes(response)

        for sku_size in product_sku_sizes:
            sku_size = sku_size.strip()
            skus[f"{product_sku.replace('.', '|')}|{product_colour}|{sku_size}"] = {
                "colour": product_colour,
                "size": sku_size,
                "price": AsicsSpider.price(response),
                'currency': 'USD'
            }

        return skus

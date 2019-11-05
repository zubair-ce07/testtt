from datetime import datetime

from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from asics.items import AsicsItem


class AsicsSpider(CrawlSpider):
    name = 'asics'
    product = AsicsItem()
    product_variant_links = []
    start_urls = ['http://www.asics.com/us/en-us/']
    rules = [
        Rule(LinkExtractor(restrict_css=(['.show-menu-item', '.page-next']))),
        Rule(LinkExtractor(restrict_css=(['.product-image a'])), callback="parse_product")
    ]

    def parse_product(self, response):
        self.product['description'] = self.description(response)
        self.product['product_name'] = self.product_name(response)
        self.product['category'] = self.product_category(response)
        self.product['image_urls'] = []
        self.product['skus'] = {}
        self.product['date'] = datetime.now().timestamp()
        self.product['price'] = self.price(response)
        self.product['url'] = response.url
        self.product['original_url'] = response.url

        script = response.xpath('//script[@type="text/javascript"]')
        self.product['brand'] = self.brand(script)
        self.product['currency'] = self.currency(script)
        self.product['lang'] = self.lang(script)
        self.product['gender'] = self.gender(script)

        self.product_variants_links = response.css(".js-color::attr(href)").getall()[1:]
        for product in self.parse_color(response):
            if not isinstance(product, Request):
                yield product

    def parse_color(self, response):
        self.product['image_urls'] += self.image_urls(response)
        self.product['skus'].update(self.parse_sku(response))

        if len(self.product_variant_links) > 0:
            page = self.product_variant_links[0]
            del self.product_variant_links[0]
            yield response.follow(page, callback=self.parse_color)
        else:
            yield self.product

    def product_name(self, response):
        return response.css(".pdp-top__product-name::text").get().strip()

    def product_category(self, response):
        return [response.css(".product-classification span::text").get()]

    def description(self, response):
        return response.css(".product-info-section-inner::text").get().strip()

    def image_urls(self, response):
        images = response.css(".thumbnail-link::attr(href)").getall()
        if '#' in images:
            images.remove('#')
        return images

    def product_category(self, response):
        return [response.css(".product-classification span::text").get()]

    def price(self, response):
        return response.css(".price-sales::text").extract()[1].strip()[1:]

    def brand(self, script):
        return script.re(r'"brand": "(\w+)"')[0]

    def currency(self, script):
        return script.re(r'"currency": "(\w+)"')[0]

    def lang(self, script):
        return script.re(r'"language": "(\w+-\w+)"')[0]

    def gender(self, script):
        return script.re(r'"product_gender": \[\n +"(\w+)"')[0]

    def sku(self, response):
        return response.css(".product-number span+ span::text").get().strip()

    def colour(self, response):
        return response.css(".variants__header--light::text").get().strip()

    def sku_sizes(self, response):
        return response.css(".variation-group-value .js-ajax::text").getall()

    def parse_sku(self, response):
        skus = {}
        product_sku = self.sku(response)
        product_colour = self.colour(response)
        product_sku_sizes = self.sku_sizes(response)

        for sku_size in product_sku_sizes:
            sku_size = sku_size.strip()
            skus[f"{product_sku.replace('.', '|')}|{product_colour}|{sku_size}"] = {
                "colour": product_colour,
                "size": sku_size,
                "price": self.price(response),
                'currency': 'USD'
            }

        return skus

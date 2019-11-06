from datetime import datetime

from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from asics.items import AsicsItem


class AsicsSpider(CrawlSpider):
    name = 'asics'
    product = AsicsItem()
    product_variant_links = []
    count = 1
    innerCount = 1
    start_urls = ['https://www.asics.com/us/en-us']
    rules = [
        Rule(LinkExtractor(restrict_css=(['.show-menu-item', '.page-next']))),
        Rule(LinkExtractor(restrict_css=(['.product-image a'])), callback="parse_product"),
    ]

    def parse_product(self, response):
        product = AsicsItem()
        product['description'] = self.description(response)
        product['product_name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['image_urls'] = []
        product['skus'] = {}
        product['date'] = datetime.now().timestamp()
        product['price'] = self.price(response)
        product['url'] = response.url
        product['original_url'] = response.url

        script = response.xpath('//script[@type="text/javascript"]')
        product['brand'] = self.brand(script)
        product['currency'] = self.currency(script)
        product['lang'] = self.lang(script)
        product['gender'] = self.gender(script)

        product['image_urls'] += self.image_urls(response)
        product['skus'].update(self.parse_sku(response))

        yield product

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

    def skus(self, response):
        skus = response.css(".js-color::attr(href)").getall()
        for index, sku in enumerate(skus):
            split_by_slash = sku.split("/")
            skus[index] = split_by_slash[len(split_by_slash) - 1].replace('.html', '').replace('-', '.')
        return skus

    def colours(self, response):
        colors = response.css(".js-color::attr(title)").getall()
        for index, color in enumerate(colors):
            colors[index] = color.replace('Select Color: ', '')
        return colors

    def sku_sizes(self, response):
        return response.css(".variation-group-value .js-ajax::text").getall()

    def parse_sku(self, response):
        skus = {}
        product_skus = self.skus(response)
        product_colour = self.colours(response)
        product_sku_sizes = self.sku_sizes(response)
        for sku, color in zip(product_skus, product_colour):
            for sku_size in product_sku_sizes:
                sku_size = sku_size.strip()
                skus[f"{sku}|{color}|{sku_size}"] = {
                    "colour": color,
                    "size": sku_size,
                    "price": self.price(response),
                    'currency': 'USD'
                }

        return skus

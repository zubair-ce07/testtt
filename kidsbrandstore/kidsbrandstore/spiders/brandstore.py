import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kidsbrandstore.items import KidsbrandstoreItem


class BrandStoreSpider(CrawlSpider):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']

    rules = (
        Rule(LinkExtractor(deny_extensions=['html'], restrict_css=(".paginationControl",
                           "div[id=bottom-types]", "div[id=bottom-brands]"))),
        Rule(LinkExtractor(restrict_css=".bottom-product-grid"), callback='parse_item'),
        )

    def parse_item(self, response):
        product = KidsbrandstoreItem()
        product['retailer_sku'] = self.parse_retailer_sku(response)
        product['category'] = self.parse_category(response)
        product['brand'] = self.parse_brand(response)
        product['url'] = self.parse_url(response)
        product['name'] = self.parse_name(response)
        product['description'] = self.parse_description(response)
        product['care'] = self.parse_care(response)
        product['image_urls'] = self.parse_image_urls(response)
        product['skus'] = self.parse_skus(response)
        product['price'] = self.parse_price(response)
        product['currency'] = self.parse_currency(response)
        product['gender'] = self.parse_gender(response)
        yield product

    def parse_retailer_sku(self, response):
        return response.css('.product_id::text').extract_first()

    def parse_category(self, response):
        return response.css('.category::text').extract_first()

    def parse_brand(self, response):
        return response.css('.brand::text').extract_first()

    def parse_url(self, response):
        return response.url

    def parse_name(self, response):
        return response.css('.name::text').extract_first()

    def parse_description(self, response):
        return response.css('.description::text').extract_first()

    def parse_care(self, response):
        return (response.css('div[class=product-information-wrapper] p::text').extract()[-3]
                if response.css('div[class=product-information-wrapper] p::text').extract()
                else None)

    def parse_image_urls(self, response):
        return response.css('figure a img::attr(src)').extract()

    def parse_price(self, response):
        return response.css('.price::text').extract_first()

    def parse_currency(self, response):
        return response.css('.price_currency_code::text').extract_first()

    def parse_gender(self, response):
        product_list = "".join(response.css('div[id=product-list-also-check] p a::text').extract())
        if response.css('svg').extract():
            return "boys/girls"
        elif "jungen" in product_list:
            return "boys"
        elif "mädchen" in product_list:
            return "girls"
        else:
            return "unisex-kids"

    def parse_color(self, response):
        if response.css('.desktop-header::text').extract():
            title = response.css('.desktop-header::text').extract_first()
            return title.split('-')[-1].replace('.', '').replace(' ', '')
        else:
            return None

    def parse_sizes(self, response):
        return response.css('.attribute-title::text').extract()

    def parse_skus(self, response):
        skus = []
        color = self.parse_color(response)
        sizes = self.parse_sizes(response)
        price = self.parse_price(response)
        currency = self.parse_currency(response)

        for size in sizes:
            skus.append({
                "colour": color,
                "price": price,
                "currency": currency,
                "size": size,
                "sku_id": f'{color}_{size}'
            })
        return skus

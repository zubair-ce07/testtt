import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Item:
    def __init__(self, response):
        self.response = response

    def _get_sku(self):
        return self.response.css('span.product_id::text').extract_first()

    def _get_gender(self):
        if self.response.xpath('//svg').extract():
            return "Boys/Girls"
        elif "jungen" in "".join(self.response.xpath('//div[@id="product-list-also-check"]/p/a/text()').extract()):
            return "Boys"
        elif "mädchen" in "".join(self.response.xpath('//div[@id="product-list-also-check"]/p/a/text()').extract()):
            return "Girls"
        else:
            return "Boys/Girls"

    def _get_category(self):
        return self.response.css('span.category::text').extract_first()

    def _get_brand(self):
        return self.response.css('span.brand::text').extract_first()

    def _get_url(self):
        return self.response.css('span.url::text').extract_first()

    def _get_name(self):
        return self.response.css('span.name::text').extract_first()

    def _get_desc(self):
        return self.response.css('span.description::text').extract_first()

    def _get_material(self):
        return (self.response.xpath('//div[@class="product-information-wrapper"]/p/text()').extract()[-1]
                if self.response.xpath('//div[@class="product-information-wrapper"]/p/text()').extract() else None)

    def _get_image_urls(self):
        return self.response.xpath('//figure//a//img/@src').extract()

    def _get_color(self):
        return (self.response.css('span.desktop-header::text').extract_first().split('-')[-1].replace('.', '').replace(' ', '')
                if self.response.css('span.desktop-header::text').extract() else None)

    def _get_sizes(self):
        return self.response.xpath('//label[@class="attribute-title"]/text()').extract()

    def _get_skus(self):
        color = self._get_color()
        currency = self._get_currency()
        price = self._get_price()
        sizes = self._get_sizes()
        skus = []
        for size in sizes:
            skus.append({
                "colour": color,
                "price": price,
                "currency": currency,
                "size": size,
                "sku_id": f'{color}_{size}'
                })
        return skus

    def _get_price(self):
        return self.response.css('span.price::text').extract_first()

    def _get_currency(self):
        return self.response.css('span.price_currency_code::text').extract_first()

    def create_item(self):
        return {
            "retailer_sku": self._get_sku(),
            "gender": self._get_gender(),
            "category": self._get_category(),
            "brand": self._get_brand(),
            "url": self._get_url(),
            "name": self._get_name(),
            "description": self._get_desc(),
            "care": self._get_material(),
            "image_urls": self._get_image_urls(),
            "skus": self._get_skus(),
            "price": self._get_price(),
            "currency": self._get_currency()
        }


class BrandStoreSpider(CrawlSpider):
    name = 'brandstore'
    allowed_domains = ['kidsbrandstore.de']
    start_urls = ['http://kidsbrandstore.de/']

    rules = (
        Rule(LinkExtractor(allow="https://kidsbrandstore\.de:443", deny='\.html'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield scrapy.Request('http://kidsbrandstore.de/', self.parse, dont_filter=False)


    def parse_item(self, response):
        if response.xpath("//meta[@name='og:title']"):
            yield Item(response).create_item()

import json

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from parse_item_structure import ParseItem


class ProductParser(scrapy.Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = ParseItem()
        product = self.extract_product(response)

        if not self.is_new_item(product):
            return

        item['name'] = self.extract_name(response)
        item['retailer_sku'] = product['id']
        item['spider_name'] = 'wefashion'
        item['brand'] = product['brand']
        item['category'] = product['category']
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['url'] = response.url
        item['description'] = self.extract_description(response)
        item['skus'] = self.extract_skus(product, response)
        item['image_urls'] = self.extract_image_urls(response)
        item['trail'] = response.meta.get('trail', [])

        return item

    def is_new_item(self, product):
        if product and product['id'] not in self.seen_ids:
            self.seen_ids.add(product['id'])
            return True

        return False

    def extract_product(self, response):
        product = response.css('[id=productEcommerceObject]::attr(value)').extract_first()
        if not product:
            return product

        product = product.split('"id"')
        product = '{"id"' + product[1]
        return json.loads(product)

    def extract_name(self, response):
        product_name = response.css('.product-name::text').extract_first()
        return product_name.strip() if product_name else None

    def extract_description(self, response):
        content = response.css('.product-details .tab-content::text').extract_first()
        return [x.strip() for x in content.split('.') if x.strip()]

    def extract_image_urls(self, response):
        return response.css('.productcarouselslides img::attr(data-image-replacement)').extract()

    def extract_skus(self, product, response):
        skus = {}
        colours_data = response.css('.swatches.color a::text').extract()
        sizes = response.css('.swatches.size .emptyswatch a::text').extract()
        skus['price'] = product['price']
        skus['currency'] = product['currencyCode']
        skus['colours'] = [x.strip() for x in colours_data]
        skus['sizes'] = [x.strip() for x in sizes]

        return skus

    def extract_market(self):
        return 'EU'

    def extract_retailer(self):
        return 'wefashion.de'

    def extract_brand(self):
        return 'We Fashion'


class WeFashionSpider(CrawlSpider):
    name = 'wefashion-crawl-spider'
    allowed_domains = ['www.wefashion.de']
    start_urls = ['https://www.wefashion.de/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    product_css = ['.level-top-1', '.category-refinement']
    listing_css = ['.container']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] if title else title

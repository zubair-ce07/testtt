import json
import re
from urllib.parse import urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider, Request

from ..items import Product

CLEANER_REGEX = r'[\n\r\t]'
PRICE_CLEANER_REGEX = r'\W'


class ProductParser(Spider):
    seen_ids = set()
    name = 'fragrance_shop_spider'

    def parse(self, response):
        product_raw_information = self.product_raw_information(response)
        retailer_sku_id = product_raw_information.get('id')

        if retailer_sku_id in self.seen_ids:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta['trail']

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = self.product_gender(product_raw_information.get('attributes'))
        item['category'] = self.product_category(product_raw_information.get('classification'))
        item['brand'] = product_raw_information.get('brand')
        item['url'] = response.url
        item['market'] = 'UK'
        item['retailer'] = 'The Fragrance Shop-UK'
        item['name'] = product_raw_information.get('name')
        item['description'] = product_raw_information.get('description')
        item['image_urls'] = self.product_image_urls(product_raw_information.get('images'))
        item['skus'] = self.product_skus(product_raw_information)
        item['price'] = self.product_price(product_raw_information.get('price'))
        item['currency'] = self.product_currency(response)

        return item

    def product_raw_information(self, response):
        selector = 'script[defer]:not([src])'
        raw_data = response.css(selector).re_first(r'({.*})')
        return json.loads(raw_data)

    def product_gender(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('display') == 'Gender':
                return raw_attr.get('value', 'unisex')

    def product_category(self, raw_data):
        return raw_data.get('mainCategoryName', [])

    def product_image_urls(self, raw_data):
        return [img.get('url') for img in raw_data]

    def product_skus(self, raw_data):
        product_variants = raw_data.get('variantProducts')
        if not product_variants:
            return [{
                'previous_prices': self.product_price(raw_data.get('listPrice')),
                'size': raw_data.get('uomValue'),
                'sku_id': raw_data.get('sku')
            }]

        return [self.product_sku(product_variant) for product_variant in product_variants]

    def product_sku(self, raw_data):
        return {
            'previous_prices': self.product_price(raw_data.get('listPrice')),
            'size': self.sku_size(raw_data.get('variantAttributes')),
            'sku_id': raw_data.get('productId'),
        }

    def sku_size(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('fieldCode') == 'global.size.volume':
                return raw_attr.get('fieldValue', 'one')

    def product_price(self, raw_price):
        formatted_price = raw_price.get('formatted').get('withTax')
        clean_price = re.sub(PRICE_CLEANER_REGEX, '', str(formatted_price))
        return clean_price

    def product_currency(self, response):
        raw_data = response.css('script[type="application/ld+json"]::text').get()
        raw_data = re.sub(CLEANER_REGEX, '', raw_data)
        raw_data = json.loads(raw_data)
        return raw_data['offers']['priceCurrency']


class FragranceShopCrawler(CrawlSpider):
    name = 'fragrance_shop_crawler'
    allowed_domains = ['thefragranceshop.co.uk']
    start_urls = ['http://thefragranceshop.co.uk/']
    product_parser = ProductParser()

    allow = r'/l'
    listing_css = ('.megaNav__list__item',)
    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listing_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        products_relative_urls = response.css('.imagePanel a::attr(href)').getall()

        yield from [Request(url=urljoin(response.url, relative_url), callback=self.product_parser.parse,
                            meta={'trail': [response.url]}) for relative_url in products_relative_urls]

        next_page_url = response.css('.pagination li:last-child a::attr(href)').get()
        if not next_page_url:
            return
        yield Request(url=next_page_url, callback=self.parse_listing)

import scrapy
import json

from scrapy.spiders import CrawlSpider, Request
from scrapy.loader import ItemLoader

from HKTV.items import Product


class HktvmallSpider(CrawlSpider):
    name = 'hktvmall'

    allowed_domains = ['www.hktvmall.com']
    start_urls = ['https://www.hktvmall.com/hktv/en/']
    api_url = 'https://www.hktvmall.com/hktv/en/ajax/search_products?query="":'\
              'relevance:zone:{}:street:main:&currentPage={}&pageSize=60'
    zones = ['supermarket', 'beautynhealth', 'housewares', 'homenfamily', 'fashion']

    def parse(self, response):
        for zone in self.zones:
            yield Request(self.api_url.format(zone, 0), callback=self.parse_json, meta={'zone': zone})

    def parse_json(self, response):
        zone = response.meta.get('zone')
        raw_data = json.loads(response.text)
        products = raw_data['products']
        number_of_pages = int(raw_data['pagination']['numberOfPages'])

        yield from self.parse_product(products)
        
        for page in range(number_of_pages):
            yield Request(self.api_url.format(zone, page), callback=self.parse_json)

    def parse_product(self, products):
        for product in products:    
            product_loader = ItemLoader(item=Product())
            
            product_loader.add_value('name', self.get_product_name(product))
            product_loader.add_value('url', self.get_product_url(product))
            product_loader.add_value('brand', self.get_product_brand(product))
            product_loader.add_value('code', self.get_product_code(product))
            product_loader.add_value('categories', self.get_product_categories(product))
            product_loader.add_value('price', self.get_product_price(product))
            product_loader.add_value('currency', self.get_product_currency(product))
            product_loader.add_value('previous_price', self.get_product_previous_price(product))
            product_loader.add_value('description', self.get_product_description(product))          
            product_loader.add_value('availability', self.get_product_stock(product))
            product_loader.add_value('packaging', self.get_product_packaging(product))
            product_loader.add_value('image_urls', self.get_product_images(product))
            product_loader.add_value('reviews_count', self.get_product_reviews_count(product))
            product_loader.add_value('reviews_score', self.get_product_reviews_score(product))
            product_loader.add_value('barcode', self.get_product_barcode(product))
            product_loader.add_value('store_name', self.get_product_store_name(product))

            yield product_loader.load_item()

    def get_product_name(self, product):
        return product['name']

    def get_product_url(self, product):
        return product['url']

    def get_product_brand(self, product):
        return product['brandName']

    def get_product_code(self, product):
        if 'categories' in product:
            return product['categories'][0]['code']

    def get_product_categories(self, product):
        if 'categories' in product:
            return product['categories'][0]['name']

    def get_product_price(self, product):
        if 'promotionPrice' in product:
            return product['promotionPrice']['value']
        return product['price']['value']

    def get_product_currency(self, product):
        if 'price' in product:
            return product['price']['currencyIso']

    def get_product_previous_price(self, product):
        if 'promotionPrice' in product:
            return product['price']['value']

    def get_product_description(self, product):
        return product['summary']

    def get_product_stock(self, product):
        return product['stock']['stockLevelStatus']['code']

    def get_product_packaging(self, product):
        return product['packingSpec']

    def get_product_images(self, product):
        return self.parse_images(product['images'])

    def get_product_reviews_count(self, product):
        return product['numberOfReviews']

    def get_product_reviews_score(self, product):
        return product['score']

    def get_product_barcode(self, product):
        return product['code']

    def get_product_store_name(self, product):
        return product['store']['name']

    def parse_images(self, images):
        return [image['url'] for image in images]

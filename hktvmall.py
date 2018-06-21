import scrapy
import json

from scrapy.spiders import CrawlSpider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from HKTV.items import Product

class HktvmallSpider(CrawlSpider):
    name = 'hktvmall'

    allowed_domains = ['www.hktvmall.com']
    start_urls = ['https://www.hktvmall.com/hktv/en/']
    api_url = 'https://www.hktvmall.com/hktv/en/ajax/search_products?query="":relevance:zone:{}:street:main:&currentPage={}&pageSize=60'
    zones = ['supermarket', 'beautynhealth', 'housewares', 'homenfamily', 'fashion']

    def parse(self, response):
        for zone in self.zones:
            yield Request(self.api_url.format('fashion', 0), callback=self.parse_json, meta={'zone': 'fashion'})

    def parse_json(self, response):
        products = response.meta.get('product') or []
        zone = response.meta.get('zone')
        data = json.loads(response.text)
        products = products.copy() + data['products']
        number_of_pages = int(data['pagination']['numberOfPages'])
        current_page = int(data['pagination']['currentPage'])

        if current_page < number_of_pages:
            for page in range(number_of_pages):
                yield Request(self.api_url.format(zone, page), meta={'product': products}, callback=self.parse_json)
        else:
            yield from self.parse_product(products)

    def parse_product(self, products):
        for product in products:    
            product_loader = ItemLoader(item=Product())
            product_loader.add_value('name', product['name'])
            product_loader.add_value('url', product['url'])
            product_loader.add_value('brand', product['brandName'])

            if 'categories' in product:
                product_loader.add_value('code', product['categories'][0]['code'])
                product_loader.add_value('categories', product['categories'][0]['name'])

            if 'price' in product:
                product_loader.add_value('price', product['price']['value'])
                product_loader.add_value('currency', product['price']['currencyIso'])
                product_loader.add_value('previous_price', product['price']['value'])

            if 'promotionPrice' in product:
                product_loader.add_value('price', product['promotionPrice']['value'])

            if 'description' in product:
                product_loader.add_value('description', product['description'])     
            
            product_loader.add_value('availability', product['stock']['stockLevelStatus']['code'])
            product_loader.add_value('packaging', product['packingSpec'])
            product_loader.add_value('image_urls', self.get_images(product['images']))
            product_loader.add_value('reviews_count', product['numberOfReviews'])
            product_loader.add_value('reviews_score', product['score'])
            product_loader.add_value('barcode', product['code'])
            product_loader.add_value('store_name', product['store']['name'])

            yield product_loader


    def get_images(self, images):
        return [image['url'] for image in images]
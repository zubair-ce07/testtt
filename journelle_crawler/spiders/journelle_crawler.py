from datetime import datetime
import json

from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.http import HtmlResponse

from journelle_crawler.items import ProductItem


class JournelleCrawler(CrawlSpider):
    name = 'journelle'

    allowed_domains = ['algolianet.com', 'journelle.com']

    currency = 'EUR'
    market = 'EU'
    retailer = 'journelle-eu'

    categories_index_and_filter = {
        'lounge': ['shopify_products_primary-rank', 'lounge%20AND%20named_tags.price%3Afull-price'],
        'lingerie': ['shopify_products_primary-rank', 'lingerie%20AND%20named_tags.price%3Afull-price'],
        'accessories': ['shopify_products_custom-rank2', 'accessories']
    }

    def start_requests(self):
        for index, filters in self.categories_index_and_filter.values():
            yield self.create_products_grid_request(category_index=index, hits_per_page=1, category_filters=filters)

    def parse(self, response):
        results = json.loads(response.text).get('results')[0]
        total_products = results['nbHits']
        total_products_retrieved = results['hitsPerPage']

        # all products are not retrieved in grid
        if total_products != total_products_retrieved:
            category_index, category_filters = self.get_category_index_and_filters(results['params'])
            yield self.create_products_grid_request(category_index=category_index, hits_per_page=total_products,
                                                    category_filters=category_filters)
        # all products are retrieved in grid
        else:
            products_data = results['hits']
            for product_data in products_data:
                product_canonical = product_data["named_tags"]["canonical"]
                yield Request(f'https://www.journelle.com/products/{product_canonical}', callback=self.parse_product)

    def create_products_grid_request(self, category_index, hits_per_page, category_filters):
        url = ('https://8n5kjnqkjm-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20'
               'JavaScript%20(lite)%203.24.5%3Binstantsearch.js%202.3.3%3BJS%20Helper%202.23.0&x-algolia-application-id'
               '=8N5KJNQKJM&x-algolia-api-key=d7f276337a47369d25c206dd1406d4e1')
        body = (f'{{"requests":[{{"indexName":"{category_index}","params":"query=&numericFilters=inventory_quantity'
                f'%3E%3D1&hitsPerPage={hits_per_page}&maxValuesPerFacet=1000&page=0&filters=named_tags.merch-department'
                f'%3A{category_filters}&facets=%5B%22named_tags.type-filter%22%2C%22options.size%22%2C%22'
                f'named_tags.base-color%22%2C%22named_tags.color-tone%22%2C%22named_tags.decorative%22%2C%22'
                f'named_tags.material-type%22%2C%22named_tags.features%22%2C%22named_tags.cup-lining%22%2C%22vendor'
                f'%22%5D&tagFilters="}}]}}')
        return Request(url, method='POST', body=body)

    def get_category_index_and_filters(self, super_key):
        for category, (index, filters) in self.categories_index_and_filter.items():
            if category in super_key:
                return index, filters

    def parse_product(self, response):
        product = ProductItem()

        product_information = response.css('div.main-content > script').get()[106:-11]
        product_information = json.loads(product_information)

        product['retailer_sku'] = self.extract_retailer_sku(product_information=product_information)
        if product['retailer_sku'] != '':
            product['gender'] = 'Female'
            product['category'] = self.extract_category(product_information=product_information)
            product['brand'] = self.extract_brand(product_information=product_information)
            product['url'] = response.url
            product['date'] = self.extract_date(response=response)
            product['currency'] = self.currency
            product['market'] = self.market
            product['retailer'] = self.retailer
            product['url_original'] = response.url
            product['name'] = self.extract_name(product_information=product_information)
            product['description'] = self.extract_description(product_information=product_information)
            product['care'] = self.extract_care(product_information=product_information)
            product['image_urls'] = self.extract_image_urls(product_information=product_information)
            product['price'] = self.extract_price(product_information=product_information)
            product['skus'] = self.extract_skus(product_information=product_information)
            product['spider_name'] = self.name
            product['crawl_start_time'] = self.extract_crawl_start_time()

            yield product

    def extract_retailer_sku(self, product_information):
        return product_information[0]['sku']

    def extract_category(self, product_information):
        return product_information[0]['type']

    def extract_brand(self, product_information):
        return product_information[0]['vendor']

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_name(self, product_information):
        return product_information[0]['title']

    def extract_description(self, product_information):
        description = HtmlResponse(url='example.com', body=product_information[0]['description'], encoding='utf-8')
        return description.css('*::text').getall()

    def extract_care(self, product_information):
        care = HtmlResponse(url='example.com', body=product_information[0]['details'], encoding='utf-8')
        return care.css('*::text').getall()

    def extract_image_urls(self, product_information):
        image_urls = []
        for product_color_information in product_information:
            for image in product_color_information['images']:
                image_urls.append(image['regular'])
        return image_urls

    def extract_price(self, product_information):
        return product_information[0]['price']

    def extract_skus(self, product_information):
        skus = {}
        for product_color_information in product_information:
            for variant in product_color_information['variants']:
                sku = {}
                sku['price'] = variant['price']
                sku['currency'] = self.currency
                sku['size'] = variant['size']
                sku['out_of_stock'] = variant['quantity'] == 0
                skus[variant['variantId']] = sku
        return skus

    def extract_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')

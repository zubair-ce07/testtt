from datetime import datetime
import json
from urllib.parse import urlencode

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse

from journelle_crawler.items import ProductItem
from journelle_crawler.linkextractors.products_link_extractor import ProductLinkExtractor


class JournelleCrawler(CrawlSpider):
    name = 'journelle'
    currency = 'EUR'
    market = 'EU'
    retailer = 'journelle-eu'
    gender = 'Female'

    products_api_url = ('https://8n5kjnqkjm-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20'
                        'vanilla%20JavaScript%20(lite)%203.24.5%3Binstantsearch.js%202.3.3%3BJS%20Helper%202.23.0&'
                        'x-algolia-application-id=8N5KJNQKJM&x-algolia-api-key=d7f276337a47369d25c206dd1406d4e1')

    categories_index_and_filter = {
        'lounge': ['shopify_products_primary-rank', 'lounge AND named_tags.price:full-price'],
        'lingerie': ['shopify_products_primary-rank', 'lingerie AND named_tags.price:full-price'],
        'accessories': ['shopify_products_custom-rank2', 'accessories']
    }

    allowed_domains = ['algolianet.com', 'journelle.com']

    rules = (
        Rule(ProductLinkExtractor(), callback='parse_product'),
    )

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
            for request in super().parse(HtmlResponse(url=response.url, body=response.text, encoding='utf-8')):
                yield request

    def create_products_grid_request(self, category_index, hits_per_page, category_filters):
        body = json.dumps({
            f'requests': [
                {
                    'indexName': category_index,
                    'params': urlencode({
                        'query': '',
                        'numericFilters': 'inventory_quantity>=1',
                        'hitsPerPage': hits_per_page,
                        'maxValuesPerFacet': '1000',
                        'page': '0',
                        'filters': f'named_tags.merch-department:{category_filters}',
                        'facets': [],
                        'tagFilters': ''
                    })
                }
            ]
        })
        return Request(self.products_api_url, method='POST', body=body)

    def get_category_index_and_filters(self, super_key):
        for category, (index, filters) in self.categories_index_and_filter.items():
            if category in super_key:
                return index, filters

    def parse_product(self, response):
        product = ProductItem()

        product_information = response.css('div.main-content > script').get()[106:-11]
        product_information = json.loads(product_information)

        first_color_information = product_information[0]

        product['retailer_sku'] = self.extract_retailer_sku(product_information=first_color_information)
        if product['retailer_sku'] != '':
            product['gender'] = self.gender
            product['category'] = self.extract_category(product_information=first_color_information)
            product['brand'] = self.extract_brand(product_information=first_color_information)
            product['url'] = response.url
            product['date'] = self.extract_date(response=response)
            product['currency'] = self.currency
            product['market'] = self.market
            product['retailer'] = self.retailer
            product['url_original'] = response.url
            product['name'] = self.extract_name(product_information=first_color_information)
            product['description'] = self.extract_description(product_information=first_color_information)
            product['care'] = self.extract_care(product_information=first_color_information)
            product['image_urls'] = self.extract_image_urls(product_information=product_information)
            product['price'] = self.extract_price(product_information=first_color_information)
            product['skus'] = self.extract_skus(product_information=product_information)
            product['spider_name'] = self.name
            product['crawl_start_time'] = self.extract_crawl_start_time()

            yield product

    def extract_retailer_sku(self, product_information):
        return product_information['sku']

    def extract_category(self, product_information):
        return product_information['type']

    def extract_brand(self, product_information):
        return product_information['vendor']

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_name(self, product_information):
        return product_information['title']

    def extract_description(self, product_information):
        description = HtmlResponse(url='example.com', body=product_information['description'], encoding='utf-8')
        return description.css('*::text').getall()

    def extract_care(self, product_information):
        care = HtmlResponse(url='example.com', body=product_information['details'], encoding='utf-8')
        return care.css('*::text').getall()

    def extract_image_urls(self, product_information):
        image_urls = []
        for product_color_information in product_information:
            for image in product_color_information['images']:
                image_urls.append(image['regular'])
        return image_urls

    def extract_price(self, product_information):
        return product_information['price']

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

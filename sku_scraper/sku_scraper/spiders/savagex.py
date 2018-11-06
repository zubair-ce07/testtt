# -*- coding: utf-8 -*-
import json
import re

from scrapy import Spider
from scrapy.http import Request
from w3lib.url import url_query_parameter, add_or_replace_parameter

from ..items import Item
from ..utilities import pricing


class Mixin:
    product_url_t = 'https://www.savagex.co.uk/shop/{}-{}'

    listings_url_t = 'https://www.savagex.co.uk/api/products?aggs=false&includeOutOfStock=true'\
        '&page=1&size=1000&defaultProductCategoryIds={}&sort=newarrivals&excludeFpls=13511'

    allowed_domains = ['savagex.co.uk']
    start_urls = ['https://www.savagex.co.uk/']

    headers = {
        'x-tfg-storedomain': 'www.savagex.co.uk',
    }


class SavagexParseSpider(Spider, Mixin):
    name = 'savagex-parse'

    seen_ids = set()

    def parse(self, response):
        raw_product = self.extract_raw_product(response)

        retailer_sku = self.extract_retailer_sku(raw_product)
        if self.is_seen_id(retailer_sku):
            return

        item = Item()
        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(raw_product)
        item['image_urls'] = self.extract_image_urls(raw_product)
        item['care'] = self.extract_care(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['category'] = self.extract_category(response)
        item['url'] = self.extract_product_url(response)
        item['skus'] = self.make_skus(raw_product, response)

        return item

    def is_seen_id(self, retailer_sku):
        if retailer_sku in self.seen_ids:
            return True
        self.seen_ids.add(retailer_sku)

    def extract_raw_product(self, response):
        raw_product_css = 'body > script:nth-of-type(3)::text'
        raw_product = response.css(raw_product_css).extract_first()
        raw_product = json.loads(re.search('__NEXT_DATA__ = (.*)', raw_product).group(1))

        return raw_product['props']['initialProps']['product']

    def extract_currency(self, response):
        currency_css = 'meta[property="og:price:currency"]::attr(content)'
        return response.css(currency_css).extract_first()

    def extract_retailer_sku(self, raw_product):
        return raw_product['item_number'].split('-')[0]

    def extract_name(self, raw_product):
        return raw_product['label']

    def extract_image_urls(self, raw_product):
        return raw_product['image_view_list']

    def extract_care(self, raw_product):
        return raw_product['medium_description'].strip()

    def extract_description(self, raw_product):
        return raw_product['long_description']

    def extract_money_strings(self, raw_product):
        return [raw_product['retail_unit_price'], raw_product.get('sale_unit_price')]
    
    def extract_product_url(self, response):
        return response.url

    def extract_category(self, response):
        return [link_text for link_text, _ in response.meta.get('trail') or [] if link_text]

    def make_skus(self, raw_product, response):
        money_string = self.extract_money_strings(raw_product)

        common_sku = pricing(money_string)
        common_sku['currency'] = self.extract_currency(response)

        skus = {}

        for raw_colour in raw_product['related_product_id_object_list']:
            colour = raw_colour['color']
            raw_sizes = (raw_colour.get('product_id_object_list') or
                         raw_product['product_detail_id_object_list'])

            for raw_size in raw_sizes:
                sku = common_sku.copy()
                sku['colour'] = colour
                sku['size'] = raw_size['size']
                
                if raw_size['availability'] != 'in stock':
                    sku['out_of_stock'] = True

                skus[f'{colour}_{sku["size"]}'] = sku

        return skus


class SavagexCrawlSpider(Spider, Mixin):
    name = 'savagex-crawl'

    product_parser = SavagexParseSpider()

    def parse(self, response):
        yield from self.create_listings_requests(response)

    def parse_listing(self, response):
        raw_listings = json.loads(response.text)

        if not raw_listings:
            return

        yield from self.create_product_requests(raw_listings, response)

        next_page = int(url_query_parameter(response.url, 'page')) + 1
        listings_url = add_or_replace_parameter(response.url, 'page', next_page)

        headers = response.request.headers.copy()
        meta = {
            'trail': self.make_trail(response),
        }
        yield Request(listings_url, headers=headers, meta=meta, callback=self.parse_listing)

    def parse_product(self, response):
        return self.product_parser.parse(response)

    def create_listings_requests(self, response):
        requests = []

        raw_listings = self.extract_raw_listings(response)
        raw_categories = raw_listings['productBrowser']['sections']
        api_key = raw_listings['api']['key']

        trail = self.make_trail(response)

        for category_name, raw_category in raw_categories.items():
            headers = self.headers.copy()
            headers['x-api-key'] = api_key
            meta = {
                'trail': trail,
                'link_text': category_name,
            }
            listings_url = self.listings_url_t.format(raw_category['defaultProductCategoryIds'])
            request = Request(listings_url, headers=headers, meta=meta, callback=self.parse_listing)
            requests.append(request)

        return requests

    def create_product_requests(self, products, response):
        requests = []

        meta = {
            'trail': self.make_trail(response)
        }

        for product in products:
            url = self.product_url_t.format(product["permalink"], product["master_product_id"])
            requests.append(Request(url, headers=self.headers.copy(), meta=meta.copy(),
                                    callback=self.parse_product))

        return requests

    def extract_raw_listings(self, response):
        raw_listings = response.xpath('//body/script/text()').extract_first()
        return json.loads(re.search('__CONFIG__ = (.*)', raw_listings).group(1))

    def make_trail(self, response):
        link_text = response.meta.get('link_text') or ''
        return (response.meta.get('trail') or []) + [(link_text, response.url)]

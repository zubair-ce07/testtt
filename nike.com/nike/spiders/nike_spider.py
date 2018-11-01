import json
import re

from scrapy.spiders import CrawlSpider
from w3lib.url import add_or_replace_parameter

from nike.items import NikeItem


class NikeParser:
    gender_map = {'kids girls boys': 'unisex-kids', 'women men': 'unisex-adults',
                  'girls boys': 'unisex-adults', 'women': 'women', 'men': 'men',
                  'girls': 'girls', 'boys': 'boys'}

    def parse(self, response):
        item = NikeItem()

        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['trail'] = self.extract_trail(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['url'] = response.url

        item['skus'] = self.extract_skus(response)

        return item

    def extract_skus(self, response):
        skus = []
        common_sku = {}

        for raw_colour in self.raw_product_details(response):
            common_sku['colour'] = raw_colour['colorDescription']
            common_sku.update(self.extract_pricing(raw_colour))

            in_stock_skus = self.extract_in_stock_skus(raw_colour)

            for raw_sku in raw_colour['skus']:
                sku = common_sku.copy()
                sku['sku_id'] = raw_sku['id']

                sku['size'] = 'One Size' if raw_sku['localizedSize'] == 'ONE SIZE' \
                    else f"{raw_sku['localizedSize']}"

                if raw_sku['skuId'] not in in_stock_skus:
                    sku['out_of_stock'] = True

                skus += [sku]

        return skus

    def extract_pricing(self, raw_prices):
        pricing = {'currency': raw_prices['currency']}

        prices = [raw_prices['currentPrice'], raw_prices['fullPrice']]
        prices = sorted([price * 100 for price in prices])

        pricing['price'] = prices[0]

        if prices[0] < prices[1]:
            pricing['previous_prices'] = prices[1:]

        return pricing

    def extract_image_urls(self, response):
        urls = []

        for raw_colour in self.raw_product_details(response):

            for raw_url in raw_colour['nodes'][0]['nodes']:
                raw_url = raw_url['properties']

                urls.append(raw_url.get('squarishURL') or raw_url.get('startImageURL'))

        return urls

    def extract_in_stock_skus(self, raw_skus):
        in_stock_skus = []

        for raw_sku in raw_skus['availableSkus']:
            in_stock_skus.append(raw_sku['skuId'])

        return in_stock_skus

    def extract_brand(self, response):
        raw_brand = self.raw_brand_details(response)
        return raw_brand['@carts']['cart']['brand']

    def extract_name(self, response):
        raw_name = self.raw_product_details(response)
        return list(raw_name)[0]['title']

    def extract_gender(self, response):
        raw_gender = list(self.raw_product_details(response))

        soup = ' '.join(raw_gender[0]['genders']).lower()

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

    def extract_description(self, response):
        raw_description = list(self.raw_product_details(response))
        return raw_description[0]['descriptionPreview'].split('.')

    def retailer_sku(self, response):
        raw_retailer_sku = self.raw_product_details(response)
        return list(raw_retailer_sku)[0]['styleCode']

    def extract_trail(self, response):
        return response.meta['trail']

    def extract_category(self, response):
        return [t for t, _ in response.meta['trail']]

    def extract_care(self, response):
        css = '.pi-pdpmainbody li ::text'
        return response.css(css).extract()

    def raw_product_details(self, response):
        raw_product_details = self.raw_brand_details(response)
        return raw_product_details['Threads']['products'].values()

    def raw_brand_details(self, response):
        css = '#app-root ~ script::text'
        raw_brand_details = response.css(css).extract_first()
        return json.loads(re.findall('{.+}', raw_brand_details)[0])


class NikeCrawler(CrawlSpider):
    name = 'nike_spider'
    allowed_domains = ['nike.com']
    start_urls = ['https://store.nike.com/gb/en_gb/']

    nike_parser = NikeParser()

    products_request_url_t = 'https://store.nike.com/html-services/' \
                             'gridwallData?country=GB&lang_locale=en_GB&gridwallPath=n/1j5'

    def parse(self, response):
        requests = self.create_product_list_requests(response)
        return self.generate_requests(requests)

    def parse_prodducts(self, response):
        requests = self.create_product_requests(response)
        return self.generate_requests(requests)

    def generate_requests(self, requests):
        for request in requests:
            yield request

    def create_product_list_requests(self, response):
        total_products_number = self.extract_total_products_number(response)
        page_number = 0
        visited_products_number = 0

        requests = []

        while visited_products_number < total_products_number:
            url = add_or_replace_parameter(self.products_request_url_t, 'pn', page_number)
            meta = {'trail': [(self.extract_title(response), response.url)]}

            requests.append(response.follow(url, callback=self.parse_prodducts, meta=meta))

            visited_products_number += 60
            page_number += 1

        url = add_or_replace_parameter(self.products_request_url_t, 'pn', page_number)
        requests.append(response.follow(url, callback=self.parse_prodducts))

        return requests

    def create_product_requests(self, response):
        raw_urls = json.loads(response.text)['sections'][0]['items']

        requests = []

        for raw_url in raw_urls:
            url = raw_url['pdpUrl']
            meta = {'trail': response.meta['trail']}

            requests.append(response.follow(url, callback=self.nike_parser.parse, meta=meta))

        return requests

    def extract_title(self, response):
        css = 'head title::text'
        return response.css(css).extract_first()

    def extract_total_products_number(self, response):
        css = '#pageTrackingDataElement::text'
        raw_number = json.loads(response.css(css).extract_first())

        return raw_number['response']['totalResults']

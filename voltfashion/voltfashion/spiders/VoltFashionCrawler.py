# -*- coding: utf-8 -*-
import json
from urllib.parse import urljoin

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.url import add_or_replace_parameters

EXTRACT_JSON_REGEX = r'({.*})'
CLEANER_ITEMS = ['\xa0']


class ProductParser(Spider):
    ids_seen = set()
    name = 'VoltFashionSpider'
    CONTENT_SELECTORS = "div[id*='react_']:not([class]) + script"

    def parse_product(self, response):
        trail = response.meta.get('trail', [])
        raw_product_details = fetch_clean_and_load_json(response, self.CONTENT_SELECTORS)
        product_details = raw_product_details.get('product')
        retailer_sku_id = product_details.get('Code')

        if retailer_sku_id in self.ids_seen:
            return

        self.ids_seen.add(retailer_sku_id)
        trail.append(response.url)
        item = {}
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = product_details.get('SeoGender', 'both')
        item['category'] = self.product_category(product_details.get('CategoryStructure'))
        item['brand'] = product_details.get('ProductBrand')
        item['url'] = response.url
        item['market'] = 'SV'
        item['retailer'] = 'VoltFashion-SV'
        item['name'] = product_details.get('Name')
        item['description'] = product_details.get('ShortDescription')
        item['care'] = self.product_care(product_details.get('ProductCare'))
        item['image_urls'] = self.product_images(product_details.get('ProductImages'))
        item['skus'] = self.product_skus(product_details)
        item['price'] = self.clean_price(product_details.get('FormattedListPrice'))
        item['currency'] = self.product_currency(product_details.get('ListPrice'))
        item['meta'] = {'requests': self.product_skus_requests(response, product_details.get('Siblings'), item)}

        return self.next_item_or_request(item)

    def product_category(self, category_json_obj):
        category = []
        for _, cat_name in enumerate(category_json_obj):
            category.append(cat_name)
        return category

    def product_care(self, care_json_obj):
        care = []
        if care_json_obj:
            for care_obj in care_json_obj:
                care.append(care_obj.get('Name'))
        return care

    def product_images(self, image_json_obj):
        images = []
        for image_obj in image_json_obj:
            images.append(image_obj.get('Url'))
        return images

    def product_currency(self, currency_json_obj):
        if currency_json_obj:
            return currency_json_obj.get('Currency')
        return None

    def product_skus(self, product_details):
        product_skus = []
        raw_skus = product_details.get('Skus')
        sku_color = product_details.get('ColorFilter')
        previous_price = self.clean_price(product_details.get('FormattedOfferedPrice'))
        for sku_obj in raw_skus:
            sku = {"colour": sku_color,
                   "previous_prices": [previous_price],
                   "size": sku_obj.get('Size'),
                   "sku_id": sku_obj.get('Id')
                   }
            product_skus.append(sku)

        return product_skus

    def product_skus_requests(self, response, product_variant, item):
        requests = []
        for variant in product_variant:
            url = urljoin(response.url, variant.get('Url'))
            requests.append(Request(url=url, callback=self.update_product_skus, dont_filter=True,
                                    meta={'item': item}))

        if response.url in requests:
            requests.remove(response.url)
        return requests

    def update_product_skus(self, response):
        item = response.meta['item']
        raw_product_details = fetch_clean_and_load_json(response, self.CONTENT_SELECTORS)
        product_details = raw_product_details.get('product')

        item['skus'] += (self.product_skus(product_details))
        item['image_urls'] += self.product_images(product_details.get('ProductImages'))
        return self.next_item_or_request(item)

    def next_item_or_request(self, item):
        sku_requests = item['meta']['requests']
        if sku_requests:
            request = item['meta']['requests'].pop()
            yield request
        else:
            item.pop('meta')
            yield item

    def clean_price(self, raw_price):
        return raw_price.replace(':-', '')


class VoltFashionCrawler(CrawlSpider):
    name = 'VoltFashionCrawler'
    product_parser = ProductParser()
    allowed_domains = ['voltfashion.com']
    start_urls = ['https://voltfashion.com/sv/']

    deny_paths = (r'/Butiker/', r'/corporate/', r'/functional/')

    CONTENT_SELECTORS = '#productlistpage__container + script'

    rules = (
        Rule(LinkExtractor(allow=r'/sv/', deny=deny_paths, restrict_css=('ul .-level-2', )),
             callback='alter_url_and_make_request', follow=False),
    )

    def alter_url_and_make_request(self, response):
        url = ''
        raw_json_data = fetch_clean_and_load_json(response, self.CONTENT_SELECTORS)
        total_items_count = raw_json_data.get('totalCount')

        if total_items_count:
            query_params = {'itemsPerPage': total_items_count, 'page': '0', 'view': 'small-img'}
            url = add_or_replace_parameters(response.url, query_params)
            url = url.replace('/?', '/#')

        return Request(url=url if url != '' else response.url, callback=self.fetch_product_urls_and_make_request,
                       dont_filter=True)

    def fetch_product_urls_and_make_request(self, response):

        raw_json_data = fetch_clean_and_load_json(response, self.CONTENT_SELECTORS)
        products_content = raw_json_data.get('products', [])

        for product in products_content:
            url = urljoin(response.url, product.get('Url'))
            yield Request(url=url, callback=self.product_parser.parse_product, meta={'trail': [response.url]})


def fetch_clean_and_load_json(response, content_selector):
    raw_json_data = response.css(content_selector).re_first(EXTRACT_JSON_REGEX)
    raw_json_data = clean_data(raw_json_data)
    return json.loads(raw_json_data) if raw_json_data else {}


def clean_data(data):
    if not data:
        return

    if type(data) is list:
        clean_data = []
        for d in data:
            for to_place in CLEANER_ITEMS:
                d = d.replace(to_place, '')
            clean_data.append(d)
        return clean_data

    clean_data = data
    for to_replace in CLEANER_ITEMS:
        clean_data = clean_data.replace(to_replace, '')

    return clean_data
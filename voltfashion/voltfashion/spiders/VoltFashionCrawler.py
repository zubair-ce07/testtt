import json
from urllib.parse import urljoin

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.url import add_or_replace_parameters

from ..items import Product

REGEX_EXTRACT = r'({.*})'
UNDESIRED_TEXTS = ['\xa0']


class ProductParser(Spider):
    seen_ids = set()
    name = 'VoltFashionSpider'
    CONTENT_SELECTOR = "div[id*='react_']:not([class]) + script"

    def parse_product(self, response):
        raw_product_details = fetch_clean_and_load(response, self.CONTENT_SELECTOR)
        product_details = raw_product_details.get('product')
        retailer_sku_id = product_details.get('Code')

        if retailer_sku_id in self.seen_ids:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = product_details.get('SeoGender', 'unisex')
        item['category'] = product_details.get('CategoryStructure')
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

    def product_care(self, raw_care):
        return [care.get('Name') for care in raw_care] if raw_care else []

    def product_images(self, raw_images):
        return [img.get('Url') for img in raw_images] if raw_images else []

    def product_currency(self, raw_currency):
        return raw_currency.get('Currency') if raw_currency else None

    def product_skus(self, product_details):
        product_skus = []
        raw_skus = product_details.get('Skus')
        sku_color = product_details.get('ColorFilter')
        raw_previous_price = product_details.get('FormattedOfferedPrice')
        previous_price = self.clean_price(raw_previous_price)

        for sku_obj in raw_skus:
            sku = {}
            sku['colour'] = sku_color
            sku['previous_prices'] = [previous_price]
            sku['size'] = sku_obj.get('Size')
            sku['sku_id'] = sku_obj.get('Id')
            product_skus.append(sku)

        return product_skus

    def product_skus_requests(self, response, product_sku_variant, item):
        requests = []
        for variant in product_sku_variant:
            url = urljoin(response.url, variant.get('Url'))
            requests.append(
                Request(url=url, callback=self.update_product_skus, dont_filter=True, meta={'item': item})
            )

        if response.url in requests:
            requests.remove(response.url)
        return requests

    def update_product_skus(self, response):
        item = response.meta['item']
        raw_product_details = fetch_clean_and_load(response, self.CONTENT_SELECTOR)
        product_details = raw_product_details.get('product')
        item['skus'] += self.product_skus(product_details)
        item['image_urls'] += self.product_images(product_details.get('ProductImages'))
        return self.next_item_or_request(item)

    def next_item_or_request(self, item):
        if item['meta']['requests']:
            request = item['meta']['requests'].pop()
            yield request
        else:
            item.pop('meta')
            yield item

    def clean_price(self, raw_price):
        return raw_price.replace(':-', '') if raw_price else None


class VoltFashionCrawler(CrawlSpider):
    name = 'VoltFashionCrawler'
    product_parser = ProductParser()

    allowed_domains = ['voltfashion.com']
    start_urls = ['https://voltfashion.com/sv/']

    ALLOW = r'/sv/'
    DENY = (r'/Butiker/', r'/corporate/', r'/functional/')
    RESTRICT_CSS = ('ul .-level-2',)
    CONTENT_SELECTORS = '#productlistpage__container + script'

    rules = (
        Rule(LinkExtractor(allow=ALLOW, deny=DENY, restrict_css=RESTRICT_CSS), callback='parse_products_urls'),
    )

    def parse_products_urls(self, response):
        raw_data = fetch_clean_and_load(response, self.CONTENT_SELECTORS)
        total_items_count = raw_data.get('totalCount')

        if not total_items_count:
            return self.make_products_requests(response)

        query_params = {'itemsPerPage': total_items_count, 'page': '0', 'view': 'small-img'}
        url = add_or_replace_parameters(response.url, query_params)
        url = url.replace('/?', '/#')
        return Request(url=url, callback=self.make_products_requests, dont_filter=True)

    def make_products_requests(self, response):
        raw_data = fetch_clean_and_load(response, self.CONTENT_SELECTORS)
        products_content = raw_data.get('products', [])

        for product in products_content:
            url = urljoin(response.url, product.get('Url'))
            yield Request(url=url, callback=self.product_parser.parse_product, meta={'trail': [response.url]})


def fetch_clean_and_load(response, content_selector):
    raw_data = response.css(content_selector).re_first(REGEX_EXTRACT)
    raw_data = clean_data(raw_data)
    loaded_content = json.loads(raw_data)
    return loaded_content if loaded_content else {}


def clean_data(data):
    if not data:
        return

    if isinstance(data, list):
        clean_data = []
        for d in data:
            for undesired_text in UNDESIRED_TEXTS:
                d = d.replace(undesired_text, '')
            clean_data.append(d)
        return clean_data

    clean_data = data
    for undesired_text in UNDESIRED_TEXTS:
        clean_data = clean_data.replace(undesired_text, '')

    return clean_data

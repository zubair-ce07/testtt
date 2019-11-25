import json
from urllib.parse import urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider, Request
from w3lib.url import add_or_replace_parameters

from ..items import Product


class ProductParser(Spider):
    seen_ids = set()
    name = 'volt_fashion_spider'
    CONTENT_SELECTOR = "div[id*='react_']:not([class]) + script"

    def parse_product(self, response):
        raw_product_details = fetch_clean_and_load(response, self.CONTENT_SELECTOR)
        raw_product = raw_product_details.get('product')
        retailer_sku_id = raw_product.get('Code')
        product_price = self.clean_price(raw_product.get('FormattedListPrice'))

        if retailer_sku_id in self.seen_ids or not product_price:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = raw_product.get('SeoGender', 'unisex')
        item['category'] = raw_product.get('CategoryStructure')
        item['brand'] = raw_product.get('ProductBrand')
        item['url'] = response.url
        item['market'] = 'SV'
        item['retailer'] = 'VoltFashion-SV'
        item['name'] = raw_product.get('Name')
        item['description'] = raw_product.get('ShortDescription')
        item['care'] = self.product_care(raw_product.get('ProductCare'))
        item['image_urls'] = self.product_images(raw_product.get('ProductImages'))
        item['skus'] = self.product_skus(raw_product)
        item['price'] = product_price
        item['currency'] = self.product_currency(raw_product.get('ListPrice'))
        item['meta'] = {'requests': self.product_skus_requests(response, raw_product.get('Siblings'), item)}

        return self.next_item_or_request(item)

    def product_care(self, raw_care):
        return [care.get('Name') for care in raw_care]

    def product_images(self, raw_images):
        return [img.get('Url') for img in raw_images]

    def product_currency(self, raw_currency):
        return raw_currency.get('Currency')

    def product_skus(self, raw_product):
        product_skus = []
        raw_skus = raw_product.get('Skus')
        sku_color = raw_product.get('ColorFilter')
        raw_previous_price = raw_product.get('FormattedOfferedPrice')
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
            if url == response.url:
                continue
            requests.append(
                Request(url=url, callback=self.parse_skus, meta={'item': item})
            )

        return requests

    def parse_skus(self, response):
        item = response.meta['item']
        raw_product_details = fetch_clean_and_load(response, self.CONTENT_SELECTOR)
        raw_product = raw_product_details.get('product')
        item['skus'] += self.product_skus(raw_product)
        item['image_urls'] += self.product_images(raw_product.get('ProductImages'))
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
    name = 'volt_fashion_crawler'
    product_parser = ProductParser()

    allowed_domains = ['voltfashion.com']
    start_urls = ['https://voltfashion.com/sv/']

    allow = r'/sv/'
    deny = (r'/Butiker/', r'/corporate/', r'/functional/')
    listing_css = ('ul .-level-2',)
    CONTENT_SELECTORS = '#productlistpage__container + script'

    rules = (
        Rule(LinkExtractor(allow=allow, deny=deny, restrict_css=listing_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        raw_data = fetch_clean_and_load(response, self.CONTENT_SELECTORS)
        total_items_count = raw_data.get('totalCount')

        if not total_items_count:
            return self.parse_products_requests(response)

        query_params = {'itemsPerPage': total_items_count, 'page': '0', 'view': 'small-img'}
        raw_url = add_or_replace_parameters(response.url, query_params)
        absolute_url = raw_url.replace('/?', '/#')
        return Request(url=absolute_url, callback=self.parse_products_requests, dont_filter=True)

    def parse_products_requests(self, response):
        raw_data = fetch_clean_and_load(response, self.CONTENT_SELECTORS)
        products = raw_data.get('products', [])

        for product in products:
            url = urljoin(response.url, product.get('Url'))
            yield Request(url=url, callback=self.product_parser.parse_product, meta={'trail': [response.url]})


def fetch_clean_and_load(response, content_selector):
    REGEX_EXTRACT = r'({.*})'
    raw_data = response.css(content_selector).re_first(REGEX_EXTRACT)
    raw_data = clean_data(raw_data)
    return json.loads(raw_data) if raw_data else {}


def clean_data(data):
    UNDESIRED_TEXTS = ['\xa0']
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

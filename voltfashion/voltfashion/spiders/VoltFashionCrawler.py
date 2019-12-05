import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider, Request
from w3lib.url import add_or_replace_parameters

from ..items import Product


class ProductParser(Spider):
    seen_ids = set()
    name = 'volt_fashion_spider'

    def parse_product(self, response):
        raw_product = self.fetch_raw_product(response)
        retailer_sku_id = raw_product['Code']
        product_price = self.clean_price(raw_product['FormattedListPrice'])

        if retailer_sku_id in self.seen_ids or not product_price:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = raw_product.get('SeoGender', 'unisex')
        item['category'] = raw_product.get('CategoryStructure', [])
        item['brand'] = raw_product.get('ProductBrand', 'VoltFashion')
        item['url'] = response.url
        item['market'] = 'SV'
        item['retailer'] = 'VoltFashion-SV'
        item['name'] = raw_product['Name']
        item['description'] = raw_product['ShortDescription']
        item['care'] = self.product_care(raw_product['ProductCare'])
        item['image_urls'] = self.product_images(raw_product.get('ProductImages', []))
        item['skus'] = self.product_skus(raw_product)
        item['price'] = product_price
        item['currency'] = self.product_currency(raw_product['ListPrice'])
        item['meta'] = {'requests': self.product_skus_requests(response, raw_product['Siblings'])}

        return self.next_item_or_request(item)

    def fetch_raw_product(self, response):
        css = "div[id*='react_']:not([class]) + script"
        raw_product_details = fetch_clean_and_load(response, css)
        return raw_product_details['product']

    def next_item_or_request(self, item):
        if item['meta']['requests']:
            request = item['meta']['requests'].pop()
            request['meta']['item'] = item
            yield request
        else:
            item.pop('meta')
            yield item

    def product_care(self, raw_care):
        return [care.get('Name') for care in raw_care]

    def product_images(self, raw_images):
        return [img.get('Url') for img in raw_images]

    def product_currency(self, raw_currency):
        return raw_currency.get('Currency')

    def product_skus(self, raw_product):
        raw_skus = raw_product.get('Skus')
        raw_previous_price = raw_product.get('FormattedOfferedPrice')

        common_sku = {'colour': raw_product.get('ColorFilter'),
                      'previous_prices': [self.clean_price(raw_previous_price)]}

        product_skus = []
        for sku_obj in raw_skus:
            sku = common_sku.copy()
            sku['size'] = sku_obj.get('Size')
            sku['sku_id'] = sku_obj.get('Id')
            product_skus.append(sku)

        return product_skus

    def product_skus_requests(self, response, product_sku_variant):
        return [response.Follow(url=variant.get('Url'), callback=self.parse_skus) for variant in product_sku_variant]

    def parse_skus(self, response):
        item = response.meta['item']
        raw_product = self.fetch_raw_product(response)
        item['skus'] += self.product_skus(raw_product)
        item['image_urls'] += self.product_images(raw_product['ProductImages'])
        return self.next_item_or_request(item)

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
        pagination_url = raw_url.replace('/?', '/#')
        return Request(url=pagination_url, callback=self.parse_products_requests, dont_filter=True)

    def parse_products_requests(self, response):
        raw_data = fetch_clean_and_load(response, self.CONTENT_SELECTORS)
        products = raw_data.get('products', [])

        for product in products:
            url = product.get('Url')
            yield response.follow(url=url, callback=self.product_parser.parse_product, meta={'trail': [response.url]})


def fetch_clean_and_load(response, content_selector):
    REGEX_EXTRACT = r'({.*})'
    raw_data = response.css(content_selector).re_first(REGEX_EXTRACT)
    raw_data = clean(raw_data)
    return json.loads(raw_data) if raw_data else {}


def clean(raw_data):
    UNDESIRED_TEXTS = ['\xa0']
    if not raw_data:
        return

    if isinstance(raw_data, list):
        clean_data = []
        for d in raw_data:
            for undesired_text in UNDESIRED_TEXTS:
                d = d.replace(undesired_text, '')
            clean_data.append(d)
        return clean_data

    for undesired_text in UNDESIRED_TEXTS:
        raw_data = raw_data.replace(undesired_text, '')

    return raw_data

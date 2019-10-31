import json

from scrapy import Request
from scrapy.spiders import CrawlSpider
from urllib.parse import urljoin

from ..items import NnnowItem


class NnnowParser:

    def parse_details(self, response):
        item = NnnowItem()
        raw_product = self.get_raw_product(response)

        item['retailer_sku'] = self.extract_retailor_sku(raw_product)
        item['gender'] = self.extract_gender(raw_product)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand(raw_product)
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['care'] = self.extract_care(raw_product)
        item['image_urls'] = self.extract_img_urls(raw_product)
        item['skus'] = self.extract_skus(raw_product, response)

        item['request_queue'] = self.extract_color_requests(response)
        yield self.get_item_or_req_to_yield(item)

    def parse_color(self, response):
        item = response.meta['item']
        product_detail = self.get_raw_product(response)

        item['image_urls'] += self.extract_img_urls(product_detail)
        item['skus'] += self.extract_skus(product_detail, response)

        yield self.get_item_or_req_to_yield(item)

    def get_raw_product(self, response):
        page_json_data = response.css('script::text').re_first('(?<=window.DATA= )(.*)')
        return json.loads(page_json_data)['ProductStore']['PdpData']['mainStyle']

    def get_item_or_req_to_yield(self, item):
        if item['request_queue']:
            request_next = item['request_queue'].pop()
            request_next.meta['item'] = item
            return request_next

        del item['request_queue']
        return item

    def extract_color_requests(self, response):
        url_domain = 'https://www.nnnow.com'
        color_urls = response.css('.nw-color-item.nwc-anchortag::attr(href)').getall()
        return [Request(urljoin(url_domain, url), callback=self.parse_color) for url in color_urls]

    def extract_retailor_sku(self, raw_product):
        return raw_product['styleId']

    def extract_gender(self, raw_product):
        return raw_product['gender']

    def extract_category(self, response):
        return response.css('.nw-breadcrumb-link ::text').getall()

    def extract_brand(self, raw_product):
        return raw_product['brandName']

    def extract_url(self, response):
        return response.url

    def extract_name(self, raw_product):
        return raw_product['name']

    def extract_description(self, raw_product):
        finer_details = raw_product['finerDetails']
        if finer_details['specs']:
            return finer_details['specs']['list']
        return finer_details['whatItIs']['list'] + finer_details['whatItDoes']['list']

    def extract_care(self, raw_product):
        if raw_product['finerDetails']['compositionAndCare']:
            return raw_product['finerDetails']['compositionAndCare']['list']
        return []

    def extract_img_urls(self, raw_product):
        return [imgs['medium'] for imgs in raw_product['images']]

    def extract_common_skus(self, raw_product, response):
        color = raw_product['colorDetails']['primaryColor']
        currency = response.css('[itemProp="priceCurrency"]::attr(content)').get()
        return {'currency': currency, 'colour': color}

    def extract_skus(self, raw_product, response):
        common_sku = self.extract_common_skus(raw_product, response)

        skus = []
        for product_sku in raw_product['skus']:
            sku = common_sku.copy()
            sku['price'] = product_sku['price']
            sku['previous_price'] = [product_sku['mrp']]
            sku['size'] = product_sku['size']
            sku['out_of_stock'] = not product_sku['inStock']
            sku['sku_id'] = product_sku['skuId']
            skus.append(sku)
        return skus


class NnnowSpider(CrawlSpider):
    name = 'nnnowSpider'
    allowed_domains = ['nnnow.com']
    start_urls = [
        'https://www.nnnow.com/',
    ]

    nnnow_details = NnnowParser()
    request_headers = {'accept': 'application/json',
                       'Content-Type': 'application/json',
                       'module': 'odin'}
    request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
    payload_template = '/{}?p={}&cid=tn_{}'

    def parse(self, response):
        raw_page = self.get_raw_page(response)
        nav_menu_items = raw_page['NavListStore']['navListData']['data']['menu']['level1']

        for menu_item in nav_menu_items:
            yield response.follow(menu_item['url'], callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_page = self.get_raw_page(response)
        total_pages = raw_page['ProductStore']['ProductData']['totalPages']
        category = response.url.split('/')[-1]

        for pg_no in range(1, total_pages):
            payload = {'deeplinkurl': self.payload_template.format(category, str(pg_no), category.replace("-", "_"))}
            yield response.follow(self.request_url, callback=self.parse_category, method='POST',
                                  body=json.dumps(payload), headers=self.request_headers)

    def parse_category(self, response):
        products_urls = json.loads(response.body)['data']['styles']['styleList']

        for product_url in products_urls:
            url_product = product_url["url"]
            yield response.follow(urljoin(self.start_urls[0], url_product), callback=self.nnnow_details.parse_details)

    def get_raw_page(self, response):
        return json.loads(response.css('script::text').re_first('(?<=window.DATA= )(.*)'))


class NnnowItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()


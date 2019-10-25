import json

from scrapy import Request
from scrapy.spiders import CrawlSpider
from urllib.parse import urljoin

from ..items import NnnowItem


class NnnowParser:

    def parse_details(self, response):
        item = NnnowItem()
        product_detail = self.get_raw_product(response)

        item['retailer_sku'] = self.extract_retailor_sku(product_detail)
        item['gender'] = self.extract_gender(product_detail)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand(product_detail)
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(product_detail)
        item['description'] = self.extract_description(product_detail)
        item['care'] = self.extract_care(product_detail)
        item['image_urls'] = self.extract_img_urls(product_detail)
        item['skus'] = self.extract_skus(product_detail, response)

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

    def extract_retailor_sku(self, product_detail):
        return product_detail['styleId']

    def extract_gender(self, product_detail):
        return product_detail['gender']

    def extract_category(self, response):
        return response.css('.nw-breadcrumb-link ::text').getall()

    def extract_brand(self, product_detail):
        return product_detail['brandName']

    def extract_url(self, response):
        return response.url

    def extract_name(self, product_detail):
        return product_detail['name']

    def extract_description(self, product_detail):
        finer_details = product_detail['finerDetails']
        if finer_details['specs']:
            return finer_details['specs']['list']
        return finer_details['whatItIs']['list'] + finer_details['whatItDoes']['list']

    def extract_care(self, product_detail):
        if product_detail['finerDetails']['compositionAndCare']:
            return product_detail['finerDetails']['compositionAndCare']['list']
        return []

    def extract_img_urls(self, product_detail):
        return [imgs['medium'] for imgs in product_detail['images']]

    def extract_common_skus(self, product_detail, response):
        color = product_detail['colorDetails']['primaryColor']
        currency = response.css('[itemProp="priceCurrency"]::attr(content)').get()
        return {'currency': currency, 'colour': color}

    def extract_skus(self, product_detail, response):
        common_sku = self.extract_common_skus(product_detail, response)

        skus = []
        for product_sku in product_detail['skus']:
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
    url_domain = 'https://www.nnnow.com'

    def parse(self, response):
        page_data_json = self.load_json_data(response)
        nav_menu_items = page_data_json['NavListStore']['navListData']['data']['menu']['level1']

        for menu_item in nav_menu_items:
            yield response.follow(menu_item['url'], callback=self.parse_category)

    def parse_pagination(self, response):
        page_data_json = self.load_json_data(response)
        total_pages = page_data_json['ProductStore']['ProductData']['totalPages']

        request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
        category = response.url.split('/')[-1]
        request_headers = {'accept': 'application/json',
                           'Content-Type': 'application/json',
                           'module': 'odin'}

        for pg_no in range(1, total_pages):
            payload = {'deeplinkurl': f'/{category}?p={str(pg_no)}&cid=tn_{category.replace("-", "_")}'}
            yield response.follow(request_url, callback=self.parse_category, method='POST',
                                  body=json.dumps(payload), headers=request_headers)

    def parse_category(self, response):
        products_urls = json.loads(response.body)['data']['styles']['styleList']

        for product_url in products_urls:
            url_product = product_url["url"]
            yield response.follow(urljoin(self.url_domain, url_product), callback=self.nnnow_details.parse_details)

    def load_json_data(self, response):
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
    img_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()


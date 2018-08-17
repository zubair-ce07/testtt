from json import loads
from w3lib.url import url_query_parameter
from urllib.parse import urljoin
from re import match

from scrapy.spiders import CrawlSpider
from scrapy import FormRequest
from scrapy import Request

from jackjones.items import Product


class JackJonesSpider(CrawlSpider):
    name = 'jackjones'

    currency = ' YUAN'
    gender = 'Boys'

    api_key_url = 'https://www.jackjones.com.cn/api/service/init?channel=6'

    category_url = "https://www.jackjones.com.cn/assets/pc/JACKJONES/nav.json"

    listing_url = 'https://www.jackjones.com.cn/api/goods/goodsList'

    product_url = 'https://www.jackjones.com.cn/detail/JACKJONES/{}.json'

    headers = {'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                             'like Gecko) Ubuntu Chromium/68.0.3440.84 Chrome/68.0.3440.84 Safari/537.36'
               }

    params = {'currentpage': '1',
              'goodsHighPrice': '',
              'goodsLowPrice': '',
              'goodsSelect': '',
              'sortDirection': 'desc',
              'sortType': '1'
              }

    product_schema = {
        'retailer_sku': '',
        'image_urls': '',
        'name': '',
        'brand': '',
        'description': '',
        'category': [],
        'care': [],
        'skus': []
    }

    allowed_domains = ['jackjones.com.cn']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,
    }

    def start_requests(self):
        yield Request(JackJonesSpider.api_key_url, callback=self.parse_api_key)

    def parse_api_key(self, response):
        api_token = loads(response.text).get('data', {}).get('token', "")
        JackJonesSpider.headers['token'] = api_token

        yield Request(JackJonesSpider.category_url, callback=self.parse_category)

    def parse_category(self, response):
        raw_navs = loads(response.text)
        raw_navs = raw_navs.get('data')
        category_ids = {url_query_parameter(url, 'classifyIds')
                        for url in self.extract_category_links(raw_navs)
                        if match('.*\/goodsList\.html\?.*', url)}

        for category_id in category_ids:
            params = JackJonesSpider.params.copy()
            params['classifyIds'] = category_id

            yield FormRequest(JackJonesSpider.listing_url, headers=JackJonesSpider.headers,
                              formdata=params, callback=self.parse_listing, method='GET')

    def parse_listing(self, response):
        raw_product = self.get_raw_product(response)
        product_ids = [i.get('goodsCode') for i in raw_product.get('data')]

        for product_id in product_ids:
            yield Request(JackJonesSpider.product_url.format(product_id), callback=self.parse_product)

        current_page = int(raw_product.get('currentpage', '-1')) + 1
        total_pages = int(raw_product.get('totalPage', '-1')) + 1

        for next_page in range(current_page, total_pages):
            params = JackJonesSpider.params.copy()
            params['classifyIds'] = url_query_parameter(response.url, 'classifyIds')
            params['currentpage'] = str(next_page)

            yield FormRequest(JackJonesSpider.listing_url, headers=JackJonesSpider.headers,
                              formdata=params, callback=self.parse_pagination, method='GET')

    def parse_pagination(self, response):
        raw_product = self.get_raw_product(response)
        product_ids = [i.get('goodsCode') for i in raw_product.get('data')]

        for product_id in product_ids:
            yield Request(JackJonesSpider.product_url.format(product_id), callback=self.parse_product)

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)
        if not raw_product:
            return JackJonesSpider.product_schema

        product_item = Product()

        product_item['category'] = self.get_categories(raw_product)
        product_item['name'] = self.get_product_name(raw_product)
        product_item['retailer_sku'] = self.get_retailer_sku(raw_product)

        product_item['brand'] = self.get_brand(raw_product)
        product_item['gender'] = self.get_gender(raw_product)
        product_item['description'] = self.get_description(raw_product)

        product_item['image_urls'] = self.get_image_urls(raw_product)
        product_item['care'] = self.get_care(raw_product)
        product_item['skus'] = self.get_skus(raw_product)
        product_item['url'] = self.get_product_url(raw_product)

        return self.product_stock_request(product_item)

    def product_stock_request(self, product_item):
        stock_url = "https://www.jackjones.com.cn/api/goods/getStock?goodsCode={}"

        yield Request(stock_url.format(product_item.get('retailer_sku')),
                      callback=self.parse_product_stock, meta={'item': product_item})

    def parse_product_stock(self, response):
        raw_stock = self.get_raw_product(response).get('data')
        product_item = response.meta.get('item')
        raw_skus = product_item.get('skus').copy()

        for raw_sku in raw_skus:

            if raw_stock.get(raw_sku.get('sku_id', '')) == 0:
                raw_sku['out_of_stock'] = True

            raw_sku['sku_id'] = "{}_{}".format(raw_sku.get('color'), raw_sku.get('size'))

        product_item['skus'] = raw_skus

        return product_item

    def get_raw_product(self, response):
        return loads(response.text)

    def get_product_name(self, raw_product):
        return raw_product.get('data', {}).get("goodsName")

    def get_care(self, raw_product):
        return [raw_product.get('data', {}).get("goodsInfo")]

    def get_description(self, raw_product):
        return [raw_product.get('data', {}).get("describe")]

    def get_retailer_sku(self, raw_product):
        return raw_product.get('data', {}).get("projectCode")

    def get_image_urls(self, raw_product):
        base_url = 'https://www.jackjones.com.cn/'
        product_colors = raw_product.get('data', {}).get("color", [])
        image_urls = sum((color.get("picurls") for color in product_colors), [])
        return [urljoin(base_url, url) for url in image_urls]

    def get_gender(self, raw_product):
        return JackJonesSpider.gender

    def get_brand(self, raw_product):
        return raw_product.get('data', {}).get("brand")

    def get_product_url(self, raw_product):
        product_url = "https://www.jackjones.com.cn/goodsDetails.html?design={}"
        product_id = raw_product.get('data', {}).get("projectCode")
        return product_url.format(product_id)

    def get_categories(self, raw_product):
        product_colors = raw_product.get('data', {}).get("color", [])

        if product_colors:
            return list({color.get("categoryName") for color in product_colors})

    def get_skus(self, raw_product):
        raw_colors = raw_product.get('data', {}).get("color", [])

        if not raw_colors:
            return []

        product_skus = []
        for raw_color in raw_colors:
            for size_sku in raw_color.get('sizes'):
                sku = {'price': raw_color.get('price'),
                       'previous_price': [raw_color.get('originalPrice')],
                       'currency': JackJonesSpider.currency,
                       'size': size_sku.get('size'),
                       'sku_id': size_sku.get('sku'),
                       'color': raw_color.get('color')}

                if raw_color.get("status") == "OutShelf":
                    sku['out_of_stock'] = True

                product_skus.append(sku)

        return product_skus

    @staticmethod
    def extract_category_links(raw_navs):
        category_links = []
        for raw_nav in raw_navs:
            category_links.append(raw_nav.get('navigationUrl'))

            for raw_sub_nav in raw_nav.get('list'):
                category_links.append(raw_sub_nav.get('navigationUrl'))

                raw_third_nav = [raw_nav.get('navigationUrl') for raw_nav in raw_sub_nav.get('list')]
                category_links.extend(raw_third_nav)

        return category_links

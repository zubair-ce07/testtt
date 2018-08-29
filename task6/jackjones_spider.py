from json import loads
from re import match
from six.moves.urllib.parse import urljoin
from w3lib.url import url_query_parameter, add_or_replace_parameter

from scrapy.spiders import CrawlSpider
from scrapy import Request

from jackjones.items import Product


class JackJonesSpider(CrawlSpider):
    name = 'jackjones'

    currency = ' YUAN'
    gender = 'Boys'

    api_key_url = 'https://www.jackjones.com.cn/api/service/init?channel=6'

    category_url = "https://www.jackjones.com.cn/assets/pc/JACKJONES/nav.json"

    listing_url = 'https://www.jackjones.com.cn/api/goods/goodsList?currentpage=1&' \
                  'goodsHighPrice=&goodsLowPrice=&goodsSelect=&sortDirection=desc&sortType=1'

    product_url = 'https://www.jackjones.com.cn/detail/JACKJONES/{}.json'

    stock_url = "https://www.jackjones.com.cn/api/goods/getStock?goodsCode={}"

    headers = {}

    allowed_domains = ['jackjones.com.cn']
    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    def start_requests(self):
        yield Request(self.api_key_url, callback=self.parse_api_key)

    def parse_api_key(self, response):
        api_token = loads(response.text).get('data', {}).get('token', "")
        self.headers['token'] = api_token

        yield Request(self.category_url, callback=self.parse_category)

    def parse_category(self, response):
        raw_navs = loads(response.text)['data']
        category_links = self.extract_category_links(raw_navs, [])
        category_ids = {url_query_parameter(url, 'classifyIds') for url in category_links
                        if match('.*\/goodsList\.html\?.*', url)}

        for category_id in category_ids:
            listing_url = add_or_replace_parameter(self.listing_url, 'classifyIds', category_id)
            yield Request(listing_url, headers=self.headers, callback=self.parse_listing)

    def parse_listing(self, response):
        raw_listings = self.extract_raw_product(response)
        product_ids = [i['goodsCode'] for i in raw_listings['data']]

        for product_id in product_ids:
            yield Request(self.product_url.format(product_id), callback=self.parse_product)

        current_page = int(raw_listings.get('currentpage', '-1')) + 1
        total_pages = int(raw_listings.get('totalPage', '-1')) + 1

        page_id = url_query_parameter(response.url, 'classifyIds')
        listing_url = add_or_replace_parameter(self.listing_url, 'classifyIds', page_id)

        for next_page in range(current_page, total_pages):
            listing_url = add_or_replace_parameter(listing_url, 'currentpage', next_page)
            yield Request(listing_url, headers=self.headers, callback=self.parse_pagination)

    def parse_pagination(self, response):
        raw_pagination = self.extract_raw_product(response)
        product_ids = [i['goodsCode'] for i in raw_pagination['data']]

        for product_id in product_ids:
            yield Request(self.product_url.format(product_id), callback=self.parse_product)

    def parse_product(self, response):
        raw_product = self.extract_raw_product(response)

        product_item = Product()

        product_item['category'] = self.extract_categories(raw_product)
        product_item['name'] = self.extract_product_name(raw_product)
        product_item['retailer_sku'] = self.extract_retailer_sku(raw_product)
        product_item['brand'] = self.extract_brand(raw_product)
        product_item['gender'] = self.extract_gender(raw_product)
        product_item['description'] = self.extract_description(raw_product)
        product_item['image_urls'] = self.extract_image_urls(raw_product)
        product_item['care'] = self.extract_care(raw_product)
        product_item['skus'] = self.extract_skus(raw_product)
        product_item['url'] = self.extract_product_url(raw_product)

        return self.product_stock_request(product_item)

    def product_stock_request(self, product_item):
        yield Request(self.stock_url.format(product_item.get('retailer_sku')),
                      callback=self.parse_product_stock, meta={'item': product_item})

    def parse_product_stock(self, response):
        raw_stock = self.extract_raw_product(response).get('data')
        product_item = response.meta.get('item')
        raw_skus = product_item.get('skus').copy()
        for raw_sku in raw_skus:

            if raw_stock.get(raw_sku.get('sku_id', '')) == 0:
                raw_sku['out_of_stock'] = True

            raw_sku['sku_id'] = "{}_{}".format(raw_sku.get('color'), raw_sku.get('size'))
        product_item['skus'] = raw_skus

        return product_item

    def extract_raw_product(self, response):
        return loads(response.text)

    def extract_product_name(self, raw_product):
        return raw_product['data']["goodsName"]

    def extract_care(self, raw_product):
        return [raw_product['data']["goodsInfo"]]

    def extract_description(self, raw_product):
        return [raw_product['data']["describe"]]

    def extract_retailer_sku(self, raw_product):
        return raw_product['data']["projectCode"]

    def extract_image_urls(self, raw_product):
        base_url = 'https://www.jackjones.com.cn/'
        product_colors = raw_product['data']["color"]
        image_urls = sum((color.get("picurls") for color in product_colors), [])
        return [urljoin(base_url, url) for url in image_urls]

    def extract_gender(self, raw_product):
        return self.gender

    def extract_brand(self, raw_product):
        return raw_product['data']["brand"]

    def extract_product_url(self, raw_product):
        product_url = "https://www.jackjones.com.cn/goodsDetails.html?design={}"
        product_id = raw_product['data']["projectCode"]
        return product_url.format(product_id)

    def extract_categories(self, raw_product):
        product_colors = raw_product['data']["color"]
        return list({color["categoryName"] for color in product_colors})

    def extract_skus(self, raw_product):
        raw_colors = raw_product['data']["color"]

        product_skus = []
        for raw_color in raw_colors:
            sku = {'price': raw_color['price'], 'currency': self.currency,
                   'previous_price': [raw_color['originalPrice']], 'color': raw_color['color']}

            for size_sku in raw_color.get('sizes'):
                sku = sku.copy()
                raw_size = size_sku['size']

                if not raw_size:
                    raw_size = 'One Size'

                sku['size'] = raw_size
                sku['sku_id'] = size_sku['sku']

                if raw_color.get("status") == "OutShelf":
                    sku['out_of_stock'] = True

                product_skus.append(sku)

        return product_skus

    def extract_category_links(self, raw_nav, category_links):
        if raw_nav:
            category_links.append(raw_nav.pop()['navigationUrl'])
            sub_nav = raw_nav.get('list')
            if sub_nav:
                self.extract_category_links(sub_nav, category_links)
            self.extract_category_links(raw_nav, category_links)

        return category_links

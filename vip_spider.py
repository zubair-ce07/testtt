import json

from scrapy import Request, Selector
from w3lib.url import add_or_replace_parameter, url_query_parameter

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'vip-cn'
    market = 'CN'
    lang = 'zh'
    allowed_domains = ['vip.com']
    start_urls = ['https://category.vip.com']


class VipParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    care_css = ".dc-table-tit:contains('材质') ~ td ::text"
    raw_description_css = '.dc-table.fst ::text'
    price_css = '.pi-price-box ::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['care'] = self.product_care(response)
        garment['category'] = self.product_category(raw_product)
        garment['description'] = self.product_description(response)
        garment['gender'] = self.product_gender(garment)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, raw_product):
        return raw_product['product']['id']

    def product_name(self, raw_product):
        return raw_product['product']['name']

    def product_brand(self, raw_product):
        return raw_product['brand']['name']

    def product_category(self, raw_product):
        return [raw_product['brand']['name']]

    def raw_product(self, response):
        css = 'script:contains(O_share)'
        raw_product = response.css(css).re('var PG = ({.*}?)')[0]
        return json.loads(raw_product)

    def image_urls(self, response):
        css = '.dc-img-detail ::attr(data-original)'
        raw_urls = clean(response.css(css))
        return [f'https:{url}' for url in raw_urls]

    def product_gender(self, garment):
        soup = ' '.join(garment['category'] + [garment['name']])
        return self.gender_lookup(soup) or Gender.KIDS.value

    def skus(self, response):
        raw_skus = self.raw_product(response)['product']
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = raw_skus['curSelectColorProps']
        skus = {}

        for sku_id, raw_sku in raw_skus['sizeStock'].items():
            sku = common_sku.copy()
            size = raw_sku['name']
            sku['size'] = self.one_size if size == '均码/F' else size
            skus[sku_id] = sku

        return skus

    def colour_requests(self, response):
        css = '.J-colorItem:not(.color-selected)::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colour) for url in urls]


class VipCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = VipParseSpider()

    category_request_url = 'https://category.vip.com/ajax/getTreeList.php?tree_id=107'
    category_listing_request_url = 'https://category.vip.com/'
    product_listing_request_url_t = 'https://category.vip.com/ajax/mapi.php?service=product_info&productIds={}'
    product_request_url_t = 'https://detail.vip.com/detail-{}-{}.html'
    page_size = 50

    deny_category_ids = [
        '288532',
        '288533',
        '96552',
        '26600',
        '26599',
        '105274',
        '26601',
        '31553',
        '269646'
    ]

    def parse(self, response):
        requests = []
        meta = {'trail': self.add_trail(response)}
        css = 'script:contains(cateIdList)::text'

        for c_id in response.css(css).re('cate_id":(.*?),'):
            if c_id in self.deny_category_ids:
                continue

            url = add_or_replace_parameter(self.category_request_url, 'cid', c_id)
            requests.append(response.follow(url, callback=self.parse_category_listing, meta=meta.copy()))

        return requests

    def parse_category_listing(self, response):
        category_id = url_query_parameter(response.url, 'cid')
        raw_urls = json.loads(response.text)['data'][category_id][0]
        meta = {'trail': self.add_trail(response)}

        return [Request(f"{self.category_listing_request_url}{raw_url['url']}",
                        callback=self.parse_product_listing, meta=meta.copy())
                for raw_url in raw_urls['children']]

    def parse_product_listing(self, response):
        css = 'script:contains(merchandise)'
        product_ids = json.loads(response.css(css).re(r':(\[.*\])')[0])
        meta = {'trail': self.add_trail(response)}
        requests = []

        for i in range(0, len(product_ids), self.page_size):
            next_product_ids = "%2C".join(product_ids[i:i + self.page_size])
            requests.append(Request(
                self.product_listing_request_url_t.format(next_product_ids),
                callback=self.parse_product, meta=meta.copy())
            )

        css = '#J_searchCatListLast_tpl::text'
        url_s = Selector(text=clean(response.css(css))[0])
        next_page_url = clean(url_s.css('a::attr(href)'))[0]

        return requests + [response.follow(next_page_url, callback=self.parse_product_listing)]

    def parse_product(self, response):
        requests = []
        meta = {'trail': self.add_trail(response)}

        for raw_url in json.loads(response.text)['data']['products']:
            requests.append(Request(
                self.product_request_url_t.format(raw_url['brandId'], raw_url['productId']),
                callback=self.parse_item, meta=meta.copy())
            )

        return requests

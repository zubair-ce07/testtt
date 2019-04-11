import re
import json

from w3lib.url import add_or_replace_parameter
from scrapy.spiders import CrawlSpider, Request

from garnethill_spider.items import GarnethillSpiderItem


class GarnethillCrawler(CrawlSpider):

    name = 'garnethill-us-crawl'
    allowed_domains = ['garnethill.com']
    start_urls = ['https://www.garnethill.com/']

    headers = {
        'authority': 'www.garnethill.com',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    }

    homeware_industries = ['rugs', 'decor', 'home', 'furniture', 'bed', 'bath']
    image_url_t = 'https://akamai-scene7.garnethill.com/is/image/{}?$ghpdp_hero2$'
    category_url_t = 'https://www.garnethill.com/UnbxdAPI?returnRespAsJSON=true&categoryId={}&rows=100'
    image_req_t = 'https://akamai-scene7.garnethill.com/is/image/garnethill/{}_is?req=imageset,json&id={}'

    def parse_start_url(self, response):
        return Request(url=response.url, callback=self.parse_categories)

    def parse_categories(self, response):
        raw_categories = response.css('.menuItem li a ::attr(href)').extract()
        return [Request(url=response.urljoin(category), callback=self.parse_pagination, headers=self.headers,
                        cookies={'INTL_SHIPPING_CTX': 'US|USD'}) for category in raw_categories]

    def parse_pagination(self, response):
        raw_pages = self.raw_pages(response)
        return Request(url=self.category_url_t.format(raw_pages.get('categoryId')), headers=self.headers,
                       callback=self.parse_listings, cookies={'INTL_SHIPPING_CTX': 'US|USD'})

    def parse_listings(self, response):
        raw_listings = self.raw_listings(response)
        return [Request(url=add_or_replace_parameter(response.urljoin(product['productDetailTargetURL']),
                'listIndex', product['listIndex']), callback=self.parse_product, headers=self.headers,
                cookies={'INTL_SHIPPING_CTX': 'US|USD'}) for product in raw_listings['products']]

    def parse_product(self, response):
        item = GarnethillSpiderItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'en'
        item['market'] = 'USA'
        item['gender'] = 'women'
        item['image_urls'] = []
        item['url'] = response.url
        item['brand'] = 'Garnet Hill'
        item['skus'] = self.skus(raw_product)
        item['care'] = self.product_care(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(response)
        item['retailer_sku'] = self.product_id(raw_product)
        item['description'] = self.product_description(raw_product)
        item['meta'] = {'requests_queue': self.image_url_requests(raw_product, item)}
        item['industry'] = self.is_home_ware(item)

        return self.next_request_or_item(item)

    def raw_listings(self, response):
        return json.loads(response.text)

    def is_home_ware(self, item):

        for category in item['category']:

            if any(homeware in category.lower() for homeware in self.homeware_industries):
                item['gender'] = None
                return 'homeware'

        return ''

    def next_request_or_item(self, item):
        requests = item['meta']['requests_queue']

        if requests:
            request = requests.pop()
            request.meta['item'] = item

            return request

        item.pop('meta')

        return item

    def product_category(self, response):
        return response.css('#breadcrumbs_ul li ::text').extract()[1:]

    def raw_product(self, response):
        css = 'script:contains("pageProduct") ::text'
        raw_product_r = re.compile('/\*(.*)\*/', re.DOTALL)
        raw_product = json.loads(response.css(css).re_first(raw_product_r))

        if raw_product.get('pageProduct'):
            return [raw_product['pageProduct']]

        return raw_product.get('bundle', [])

    def product_care(self, raw_product):
        raw_care = raw_product[0].get('productAdditionalInfoTabs') or \
                   raw_product[0].get('pageProduct')['productAdditionalInfoTabs']

        if raw_care[0].get('tabHtmlValue'):
            return raw_care[0]['tabHtmlValue'].split(';')[4::4]

        return []

    def raw_pages(self, response):
        css = 'script:contains("numberOfProducts") ::text'
        return json.loads(response.css(css).re_first(re.compile('/\*(.*)\*/', re.DOTALL)))

    def product_id(self, raw_product):
        return raw_product[0].get('prodId') or raw_product[0].get('pageProduct', {}).get('prodId', [])

    def product_name(self, raw_product):
        return raw_product[0].get('prodName') or raw_product[0].get('pageProduct', {}).get('prodName', [])

    def parse_image_urls(self, response):
        item = response.meta['item']
        raw_urls = re.search(':"(.*)"}', response.text).group(1).split(',')
        item['image_urls'] = [self.image_url_t.format(i) for url in raw_urls for i in url.split(';')]

        return self.next_request_or_item(item)

    def skus(self, raw_product):
        skus = {}

        for raw_skus in raw_product:

            for raw_sku in raw_skus.get('entitledItems') or \
                           raw_skus.get('pageProduct', {}).get('entitledItems', []):

                sku = self.product_pricing(raw_product, raw_sku)
                colour_id, size_id = self.colour_and_size_ids(raw_skus)

                if not raw_sku['buyable']:
                    sku['out_of_stock'] = True

                for sku_id in raw_sku['definingAttributes']:

                    if sku_id['optionItemKey'] == colour_id:
                        sku['colour'] = sku_id['displayName']
                    if sku_id['optionItemKey'] == size_id:
                        sku['size'] = sku_id['displayName'] or 'One Size'

                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def colour_and_size_ids(self, raw_skus):
        raw_ids = raw_skus.get('definingAttributes') or \
                  raw_skus.get('pageProduct', {}).get('definingAttributes', [])

        return raw_ids[0]['optionItemKey'], raw_ids[1]['optionItemKey']

    def product_description(self, raw_product):
        description = raw_product[0].get('longDesc') or raw_product[0].get('pageProduct', [])

        if description and type(description) != str:
            return [description.get('longDesc')] or []
        elif description and type(description) == str:
            return [description]

        return []

    def image_url_requests(self, raw_product, item):
        product_id = raw_product[0].get('mfPartNumber') or \
                     raw_product[0].get('pageProduct', {}).get('mfPartNumber', [])

        return [Request(url=self.image_req_t.format(product_id, product_id),
                        meta={'item': item}, callback=self.parse_image_urls)]

    def product_pricing(self, raw_product, raw_sku):
        pricing = {'price': raw_sku.get('minimumPrice') or raw_sku['contractPrice']}
        prev_price = raw_sku.get('minListPrice') or raw_sku.get('listPrice', '')
        pricing['currency'] = raw_product[0].get('currencyCode') or \
                              raw_product[0].get('pageProduct')['currencyCode']

        if prev_price and prev_price != pricing['price']:
            pricing['previous_price'] = prev_price

        return pricing

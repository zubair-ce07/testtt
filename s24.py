import json
import re
import unicodedata
import urllib
import urllib.parse as urlparse

from scrapy import Item, Field, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class _24sItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    price = Field()
    skus = Field()
    requests = Field()


class _24sSpider(CrawlSpider):
    name = '24s'
    allowed_domains = ['24s.com', 'dkpvob44gb-dsn.algolia.net']
    start_urls = [
        'https://www.24s.com/en-us/'
    ]

    pagination_url_t = 'https://dkpvob44gb-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=' \
                       'Algolia+for+vanilla+JavaScript+3.32.1%3BJS+Helper+2.26.1&x-algolia-' \
                       'application-id=DKPVOB44GB&x-algolia-api-key=9b23af4f250bb432947c20b7c82890a2'
    product_url_t = '{}-{}_{}?defaultSku={}&color={}'
    facets = urllib.parse.quote('["brand","brand","color_en_pack","clothing_size_FR",'
                                '"clothing_size_US","clothing_size_UK","clothing_size_IT",'
                                '"clothing_size_DE","clothing_size_JP","shoes_size_EU",'
                                '"shoes_size_FR","shoes_size_US","shoes_size_UK",'
                                '"shoes_size_JP","shoes_size_KOR","promotion_event_type"]')
    headers = {
        'accept': 'application/json',
        'Origin': 'https://www.24s.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
    }

    listings_css = ['.nav-link', '[class="device-drop-btn"]']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_categories'),
    )

    def parse_categories(self, response):
        tag_filter = self.get_tag_filters(response)
        rule_contexts = self.get_rule_contexts(response)

        body = '{"requests":[{"indexName":"prod_products","params":"query=&tagFilters=' + tag_filter \
               + '&page=0&getRankingInfo=true&ruleContexts=' + rule_contexts \
               + '&facets=' + self.facets + '"}]}'

        return Request(self.pagination_url_t, method='POST',
                       body=body, headers=self.headers, callback=self.parse_pagination)

    def get_tag_filters(self, response):
        raw_tag_filter = ["US"]
        raw_tag_filter.extend(response.css('::attr(data-filter)').get().split(','))
        tag_filter = re.sub(' ', '', re.sub('\'', '"', str(raw_tag_filter)))
        return urllib.parse.quote(tag_filter)

    def get_rule_contexts(self, response):
        raw_rule_context = response.css('::attr(data-filter)').get()

        if ',' in raw_rule_context:
            raw_rule_context = [re.sub(',', '_MERCH_US', raw_rule_context)]
        else:
            raw_rule_context = [f"{raw_rule_context}{'_MERCH_US'}"]

        rule_context = re.sub(' ', '', (re.sub('\'', '"', str(raw_rule_context))))
        return urllib.parse.quote(rule_context)

    def parse_pagination(self, response):
        self.extract_products_url(response)
        total_pages = json.loads(response.text)['results'][0]['nbPages'] + 1
        body = json.loads(response.request.body)

        for page_number in range(1, total_pages):
            body = self.next_req_body(body, page_number)
            yield Request(self.pagination_url_t, method='POST',
                          body=json.dumps(body), headers=self.headers,
                          callback=self.extract_products_url, dont_filter=True)

    def next_req_body(self, body, page_number):
        body['requests'][0]['params'] = re.sub('page=(.+?)&',
                                               f'page={page_number}&',
                                               body['requests'][0]['params'])
        return body

    def extract_products_url(self, response):
        raw_products = json.loads(response.text)['results'][0]

        for product in raw_products['hits']:
            title = self.clean_accent_and_grb(product['title_en'])
            brand = self.clean_accent_and_grb(product['brand'])
            group_id = product['item_group_id']
            sku_id = product['sku']
            color = self.clean_accent_and_grb(product['color_brand'])
            product_url = self.product_url_t.format(title, brand, group_id, sku_id, color)
            yield response.follow(product_url, callback=self.parse_item)

    def clean_accent_and_grb(self, raw_str):
        raw_str = ''.join((c for c in unicodedata.normalize('NFD', raw_str) if
                           unicodedata.category(c) != 'Mn')).lower()
        return re.sub(' |\/', '-', re.sub('"', '', raw_str))

    def parse_item(self, response):
        item = _24sItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['skus'] = self.product_skus(response)
        item['image_urls'] = self.product_images(response)

        item['requests'] = self.color_requests(response)
        return self.next_request_or_item(item)

    def color_requests(self, response):
        requests = []
        product_json = json.loads(response.css('::attr(data-variants-tree)').get())

        for color in product_json['_children']:
            if not color['selected']:
                url = response.url[:response.url.index('?')]
                requests.append(Request(f'{url}?color={color["value"]}', callback=self.parse_color))

        return requests

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.product_images(response))
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_images(self, response):
        images_urls_1 = response.css('[id*="product-img-"] img ::attr(src)').getall()
        images_urls_2 = response.css('[id*="img-"] img ::attr(src)').getall()

        return [url for url in images_urls_1 + images_urls_2
                if 'base64' not in url]

    def product_skus(self, response):
        skus = {}
        price_sel = response.css('[itemprop="price"]')
        color = urlparse.parse_qs(urlparse.urlparse(response.url).query)['color'][0]
        sizes = clean(response.css('select option:nth-child(n+3)::text').getall())

        common_sku = {
            'color': color,
            'price': price_sel.css('::attr(content)').get(),
            'previous_price': price_sel.css('::attr(data-price)').get(),
            'currency': price_sel.css('::attr(data-currency)').get()
        }

        if not sizes:
            common_sku['out_of_stock'] = False
            common_sku['size'] = 'OneSize'
            return {f'{common_sku["size"]}_{color}': common_sku.copy()}

        for size in sizes:

            common_sku['out_of_stock'] = False
            if 'Out of stock' in size:
                common_sku['out_of_stock'] = True
                size = size[:size.index(' - O')]
            common_sku['size'] = size

            skus[f'{color}_ {size}'] = common_sku.copy()

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, response):
        return urlparse.parse_qs(urlparse.urlparse(response.url).query)['defaultSku'][0]

    def product_gender(self, response):
        return response.css('script:contains("universe")'). \
            re_first('universe\":\"(.+?)\"')

    def product_name(self, response):
        return response.css('#product-toolbar h2::text').get()

    def product_category(self, response):
        return response.css('script:contains("category")').re_first('category\"\:\"(.+?)\"').split('\\/')

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('[class="function-bold"] ::text').get()

    def product_description(self, response):
        descp = response.css('.grey ::text').getall()[:-1]
        return [''.join(descp)][0].split('.')

    def product_care(self, response):
        return clean(response.css('.grey ::text').getall()[-1].split('/'))



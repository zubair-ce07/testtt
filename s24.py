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

    pagination_url = 'https://dkpvob44gb-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia+for+vanilla' \
                     '+JavaScript+3.32.1%3BJS+Helper+2.26.1&x-algolia-application-id=DKPVOB44GB&x-algolia-api-' \
                     'key=9b23af4f250bb432947c20b7c82890a2'

    headers = {
        'accept': 'application/json',
        'Origin': 'https://www.24s.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 '
                      'Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
    }

    body_json = json.loads('{"requests":[{"indexName":"prod_products","params":"query=&tagFilters={}&page=0&'
                           'getRankingInfo=true&ruleContexts={}"}]}')

    listings_css = ['.nav-link', '[class="device-drop-btn"]']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_categories'),
    )

    def parse_categories(self, response):
        body = self.request_payload(response)
        return Request(self.pagination_url, method='POST', body=body, headers=self.headers,
                       callback=self.parse_pagination)

    def request_payload(self, response):
        tag_filter = self.get_tag_filters(response)
        rule_contexts = self.get_rule_contexts(response)
        params = self.body_json['requests'][0]['params'].format(tag_filter, rule_contexts)
        self.body_json['requests'][0]['params'] = params

        return json.dumps(self.body_json)

    def get_tag_filters(self, response):
        raw_tag_filter = ["US"] + response.css('::attr(data-filter)').get().split(',')
        tag_filter = str(raw_tag_filter).replace('\'', '"').replace(' ', '')
        return urllib.parse.quote(tag_filter)

    def get_rule_contexts(self, response):
        raw_rule_context = response.css('::attr(data-filter)').get()

        if ',' not in raw_rule_context:
            raw_rule_context = f'{raw_rule_context},'

        rule_context = raw_rule_context.replace('\'', '"').replace(' ', '').replace(',', '_MERCH_US')
        return urllib.parse.quote(rule_context)

    def parse_pagination(self, response):
        self.parse_products(response)
        total_pages = json.loads(response.text)['results'][0]['nbPages'] + 1

        for page_number in range(1, total_pages):
            body = self.request_body(response, page_number)
            yield Request(self.pagination_url, method='POST', body=body, headers=self.headers,
                          callback=self.parse_products, dont_filter=True)

    def request_body(self, response, page_number):
        body = json.loads(response.request.body)
        body['requests'][0]['params'] = re.sub('page=(.+?)&', f'page={page_number}&',
                                               body['requests'][0]['params'])
        return json.dump(body)

    def parse_products(self, response):
        raw_products = json.loads(response.text)['results'][0]

        for product in raw_products['hits']:
            product_url = self.clean_url(f'{product["title_en"]}-{product["brand"]}_{product["item_group_id"]}?'
                                         f'defaultSku={product["sku"]}&color={product["color_brand"]}')
            yield response.follow(product_url, callback=self.parse_item)

    def clean_url(self, raw_str):
        raw_str = (c for c in unicodedata.normalize('NFD', raw_str) if unicodedata.category(c) != 'Mn')
        raw_str = ''.join(raw_str).lower()
        return re.sub(' |\/', '-', raw_str.replace('"', ''))

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
        product_json = json.loads(response.css('::attr(data-variants-tree)').get())
        return [Request(self.new_color_url(color, response), callback=self.parse_color)
                for color in product_json['_children'] if not color['selected']]

    def new_color_url(self, color, response):
        params = {'color': color}
        url_parts = list(urllib.parse.urlparse(response.url))
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.parse.urlencode(query)

        return urllib.parse.urlunparse(url_parts)

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'] += self.product_images(response)
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_images(self, response):
        images_urls = response.css('[id*="product-img-"] img ::attr(src) , [id*="img-"] img ::attr(src)').getall()
        return [url for url in images_urls
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

        for size in sizes or ['One_Size']:
            if 'Out of stock' in size:
                common_sku['out_of_stock'] = True
                size = clean(size.split('-')[0])
            common_sku['size'] = size
            skus[f'{color}_{size}'] = common_sku.copy()

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, response):
        return response.css('script:contains("productSKU")').re_first('productSKU\"\:\"(.+?)\"')

    def product_gender(self, response):
        return response.css('script:contains("universe")').re_first('universe\":\"(.+?)\"')

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


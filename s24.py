import json
import re
import unicodedata
import urllib

from scrapy import Item, Field, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
import urllib.parse as urlparse


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
    sku_key_t = '{}_{}'
    prod_req_t = '{}?color={}'
    pagination_url_t = 'https://dkpvob44gb-dsn.algolia.net/1/indexes/*/queries?{}'
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
    params = (
        ('x-algolia-agent', 'Algolia for vanilla JavaScript 3.32.1;JS Helper 2.26.1'),
        ('x-algolia-application-id', 'DKPVOB44GB'),
        ('x-algolia-api-key', '9b23af4f250bb432947c20b7c82890a2'),
    )

    listing_css = ['.nav-link', '[class="device-drop-btn"]']
    all_brands_css = '#lbm-brands-page-html'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_css=all_brands_css), callback='foo'),
    )

    def parse_pagination(self, response):
        page_number = self.get_page_number(response)
        tag_filter = self.get_tag_filters(response)
        rule_contexts = self.get_rule_contexts(response)

        body = '{"requests":[{"indexName":"prod_products","params":"query=&tagFilters=' + tag_filter \
               + '&page=' + page_number + '&getRankingInfo=true&ruleContexts=' + rule_contexts \
               + '&facets=' + self.facets + '"}]}'

        yield Request(self.pagination_url_t.format(urllib.parse.urlencode(self.params)), method='POST',
                      body=body, headers=self.headers, callback=self.parse_products, meta={'listing_url': response.url})

    def get_page_number(self, response):
        if 'pg_num' in response.meta.keys():
            return response.meta['pg_num']
        return '0'

    def get_tag_filters(self, response):
        raw_tag_filter = ["US"]
        raw_tag_filter.extend(response.css('::attr(data-filter)').get().split(','))
        tag_filter = re.sub(' ', '', re.sub('\'', '"', str(raw_tag_filter)))
        return urllib.parse.quote(tag_filter)

    def get_rule_contexts(self, response):
        raw_rule_context = response.css('::attr(data-filter)').get()

        if ',' in raw_rule_context:
            raw_rule_context = [re.sub(',', '_MERCH_US', )]
        else:
            context_format = '{}{}'
            raw_rule_context = [context_format.format(raw_rule_context, '_MERCH_US')]

        rule_context = re.sub(' ', '', (re.sub('\'', '"', str(raw_rule_context))))
        return urllib.parse.quote(rule_context)

    def parse_products(self, response):
        products_json = json.loads(response.text)['results'][0]

        for product in products_json['hits']:
            title = self.clean_accent_and_grb(product['title_en'])
            brand = self.clean_accent_and_grb(product['brand'])
            group_id = product['item_group_id']
            sku_id = product['sku']
            color = self.clean_accent_and_grb(product['color_brand'])

            product_url = self.product_url_t.format(title, brand, group_id, sku_id, color)
            yield response.follow(product_url, callback=self.parse_item)

        if products_json['page'] <= products_json['nbPages']:
            next_page_num = str((products_json['page']) + 1)
            return response.follow(response.meta['listing_url'], callback=self.parse,
                                   meta={'pg_num': next_page_num}, dont_filter=True)

    def clean_accent_and_grb(self, raw_str):
        str = ''.join((c for c in unicodedata.normalize('NFD', raw_str) if
                       unicodedata.category(c) != 'Mn')).lower()
        return re.sub(' |\/', '-', re.sub('"', '', str))

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
        raw_product_json = json.loads(response.css('::attr(data-variants-tree)').get())

        for color in raw_product_json['_children']:
            if not color['selected']:
                url = response.url[:response.url.index('?')]
                requests.append(Request(self.prod_req_t.format(url, color["value"]), callback=self.parse_color))

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
            return {self.sku_key_t.format(common_sku["size"], color): common_sku.copy()}

        for size in sizes:

            common_sku['out_of_stock'] = False
            if 'Out of stock' in size:
                common_sku['out_of_stock'] = True
                size = size[:size.index(' - O')]
            common_sku['size'] = size

            skus[self.sku_key_t.format(color, size)] = common_sku.copy()

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
        gender = response.css('title::text').get()
        return gender[:gender.index("'")]

    def product_name(self, response):
        name = response.css('title::text').get()
        return clean(name[name.index("'s") + 2:name.index("|")])

    def product_category(self, response):
        return response.css('script:contains("category")').re_first('pageSubCategory\"\:\"(.+?)\"').split('_')

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('[class="function-bold"] ::text').get()

    def product_description(self, response):
        descp = response.css('.grey ::text').getall()[:-1]
        return [''.join(descp)][0].split('.')

    def product_care(self, response):
        return clean(response.css('.grey ::text').getall()[-1].split('/'))


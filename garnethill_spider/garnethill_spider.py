import re
import json

from scrapy.link import Link
from w3lib.html import remove_tags
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

from garnethill_spider.items import GarnethillSpiderItem


class GarnethillParseSpider(CrawlSpider):

    name = 'garnethill-us-parse'
    homeware_industries = ['rugs', 'decor', 'home', 'furniture', 'bed', 'bath']
    image_url_t = 'https://akamai-scene7.garnethill.com/is/image/{}?$ghpdp_hero2$'
    image_req_t = 'https://akamai-scene7.garnethill.com/is/image/garnethill/{}_is?req=imageset,json&id={}'

    def parse(self, response):
        item = GarnethillSpiderItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'en'
        item['industry'] = ''
        item['market'] = 'USA'
        item['image_urls'] = []
        item['gender'] = 'women'
        item['url'] = response.url
        item['brand'] = 'Garnet Hill'
        item['skus'] = self.skus(raw_product)
        item['care'] = self.product_care(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(response)
        item['retailer_sku'] = self.product_id(raw_product)
        item['description'] = self.product_description(raw_product)
        item['meta'] = {'requests_queue': self.image_url_requests(raw_product, item)}

        if self.is_homeware(item):
            item['gender'] = None
            item['industry'] = 'homeware'

        return self.next_request_or_item(item)

    def parse_image_urls(self, response):
        item = response.meta['item']
        raw_urls = re.search(':"(.*)"}', response.text).group(1).split(',')
        item['image_urls'] = [self.image_url_t.format(i) for url in raw_urls for i in url.split(';')]

        return self.next_request_or_item(item)

    def is_homeware(self, item):
        return any(homeware in category.lower() for category in item['category']
                   for homeware in self.homeware_industries)

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
                   raw_product[0].get('pageProduct', {}).get('productAdditionalInfoTabs', [])

        if raw_care and raw_care[0].get('tabHtmlValue'):
            return [remove_tags(i) for i in raw_care[0]['tabHtmlValue'].split(';')[4::4]]

        return []

    def product_id(self, raw_product):
        return raw_product[0].get('prodId') or raw_product[0]['pageProduct']['prodId']

    def product_name(self, raw_product):
        return raw_product[0].get('prodName') or raw_product[0]['pageProduct']['prodName']

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
                        sku['size'] = sku_id.get('displayName') or 'One Size'

                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def product_description(self, raw_product):
        description = raw_product[0].get('longDesc')

        if description:
            return [remove_tags(description)]
        elif raw_product[0].get('pageProduct'):
            return [remove_tags(raw_product[0]['pageProduct'].get('longDesc'))] or []

        return []

    def image_url_requests(self, raw_product, item):
        product_id = raw_product[0].get('mfPartNumber') or raw_product[0]['pageProduct']['mfPartNumber']

        return [Request(url=self.image_req_t.format(product_id, product_id), meta={'item': item},
                        callback=self.parse_image_urls)]

    def product_pricing(self, raw_product, raw_sku):
        prev_price = raw_sku.get('minListPrice') or raw_sku.get('listPrice')
        pricing = {'price': raw_sku.get('minimumPrice') or raw_sku['contractPrice']}
        pricing['currency'] = raw_product[0].get('currencyCode') or \
                              raw_product[0]['pageProduct']['currencyCode']

        if prev_price and prev_price != pricing['price']:
            pricing['previous_price'] = prev_price

        return pricing

    def colour_and_size_ids(self, raw_skus):
        raw_ids = raw_skus.get('definingAttributes') or raw_skus['pageProduct']['definingAttributes']
        return raw_ids[0]['optionItemKey'], raw_ids[1]['optionItemKey']


class CategoryLE(LinkExtractor):

    def extract_links(self, response):
        raw_categories = response.css('.menuItem li a ::attr(href)').extract()
        return [Link(response.urljoin(category)) for category in raw_categories]


class GarnethillCrawlSpider(CrawlSpider):

    name = 'garnethill-us-crawl'
    allowed_domains = ['garnethill.com']
    cookies = {'INTL_SHIPPING_CTX': 'US|USD'}
    start_urls = ['https://www.garnethill.com/']
    category_url_t = 'https://www.garnethill.com/UnbxdAPI?returnRespAsJSON=true&categoryId={}&rows=100'

    rules = (
        Rule(CategoryLE(), callback='parse_pagination'),
    )

    parse_spider = GarnethillParseSpider()

    def parse_pagination(self, response):
        raw_pages = self.raw_pages(response)
        return Request(url=self.category_url_t.format(raw_pages.get('categoryId')),
                       callback=self.parse_listings, cookies=self.cookies)

    def parse_listings(self, response):
        return [Request(url=response.urljoin(product['productDetailTargetURL']), callback=self.parse_spider.parse,
                        cookies=self.cookies) for product in json.loads(response.text)['products']]

    def raw_pages(self, response):
        css = 'script:contains("numberOfProducts") ::text'
        return json.loads(response.css(css).re_first(re.compile('/\*(.*)\*/', re.DOTALL)))

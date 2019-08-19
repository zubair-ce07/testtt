import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule, Spider

from speedo.items import SpeedoItem


class SpeedoParser(Spider):
    name = 'speedoparser'
    brand = 'Speedo'
    market = 'AU'
    retailer = 'speedo-au'

    allowed_domains = [
        'speedo.com.au'
    ]

    def parse(self, response):
        item = SpeedoItem()
        item['brand'] = self.brand
        item['skus'] = []
        item['image_urls'] = []
        item['url'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.get_categories(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        item['requests'] = self.get_colour_requests(response)

        return self.next_request_or_item(item)

    def parse_skus_and_images(self, response):
        item = response.meta['item']
        item['skus'].extend(self.get_sku(response))
        item['image_urls'].extend(self.get_image_urls(response))

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if not item.get('requests'):
            del item['requests']
            return item

        request = item['requests'].pop(0)
        request.meta.setdefault('item', item)

        return request

    def get_colour_requests(self, response):
        urls = response.css('a.color-attribute::attr(href)').getall()
        return [Request(url=url, callback=self.parse_skus_and_images) for url in urls]

    def get_image_urls(self, response):
        raw_urls = json.loads(response.text)['product']['images']['large']
        return [url['url'] for url in raw_urls]

    def get_name(self, response):
        return response.css('.product-name::text').get()

    def get_product_id(self, response):
        return response.css('.product-id::text').get()

    def get_description(self, response):
        css = '.render-product-details::attr(data-json)'
        description_map = json.loads(response.css(css).get())
        features = re.findall(r'<li>(.*?)</li>', description_map[1]['content'])

        return self.sanitize_list([description_map[0]['content']] + features)

    def get_sku(self, response):
        product_map = json.loads(response.text)['product']
        out_of_stock = self.get_out_of_stock(product_map['availability']['messages'])
        skus = []

        for raw_size in product_map['variationAttributes'][1]['values']:
            sku = {**self.get_pricing_details(response)}
            sku['colour'] = product_map['variationAttributes'][0]['displayValue']
            sku['size'] = raw_size['displayValue']
            sku['sku_id'] = f'{sku["colour"]}-{sku["size"]}'
            sku['out_of_stock'] = out_of_stock
            skus.append(sku)

        return skus

    def get_pricing_details(self, response):
        price_map = json.loads(response.text)['product']['price']
        pricing = {'price': self.sanitize_price(price_map['sales']['decimalPrice'])}
        pricing['currency'] = price_map['sales']['currency']

        if price_map.get('list'):
            pricing['previous_prices'] = [self.sanitize_price(price_map['list']['decimalPrice'])]

        return pricing

    def get_categories(self, response):
        return self.sanitize_list(response.css('.breadcrumb a::text').getall()[1:-1])

    def get_gender(self, response):
        return response.css('.product-spec-list dd::text').get()

    def get_care(self, response):
        care = response.css('.product-spec-list dd:nth-last-child(1)::text').get()
        return self.sanitize_list(care.split(','))

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs if i and i.strip()]

    def sanitize_price(self, price):
        return float(''.join(re.findall(r'\d+', price)))

    def get_out_of_stock(self, messages):
        return re.findall(r'>(.*?)</div>', messages[0])[0] != 'In Stock'


class SpeedoCrawler(CrawlSpider):
    name = 'speedocrawler-crawl'
    speedo_parser = SpeedoParser()

    start_urls = [
        'https://speedo.com.au/'
    ]

    allowed_domains = [
        'speedo.com.au'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    cookie = {'KP_UID': '28cff93f-9c85-e95e-ddb5-449687693fc5'}

    listing_css = ['.nav-item.dropdown', '.product-list-cards', '.show-more']
    product_css = '.product-grid'
    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css, tags=['a', 'button::attr(data-url)']),
             callback='parse'),
    ]

    def start_requests(self):
        return [Request(url, cookies=self.cookie.copy()) for url in self.start_urls]

    def parse(self, response):
        requests = super(SpeedoCrawler, self).parse(response)
        trail = self.add_trail(response)

        return [r.replace(meta={**r.meta, 'trail': trail.copy()}) for r in requests]

    def parse_product(self, response):
        yield self.speedo_parser.parse(response)

    def add_trail(self, response):
        new_trail = [(response.css('head title::text').get(), response.url)]
        return response.meta.get('trail', []) + new_trail

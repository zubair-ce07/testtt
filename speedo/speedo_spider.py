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

    genders = [
        ('women', 'women'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girls', 'girls'),
        ('men', 'men'),
        ('adults', 'unisex-adults'),
        ('unisex', 'unisex-adults'),
        ('kids', 'unisex-kids'),
        ('babies', 'unisex-kids'),
        ('toddlers', 'unisex-kids'),
    ]

    def parse(self, response):
        item = SpeedoItem()
        item['skus'] = []
        item['image_urls'] = []
        item['url'] = response.url
        item['brand'] = self.brand
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['trail'] = response.meta.get('trail', [])
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['category'] = self.get_categories(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        item['requests'] = self.get_colour_requests(response)

        return self.next_request_or_item(item)

    def parse_colour_requests(self, response):
        raw_product = json.loads(response.text)
        item = response.meta['item']
        item['image_urls'].extend(self.get_image_urls(raw_product))
        item['requests'].extend(self.get_size_requests(raw_product))

        return self.next_request_or_item(item)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'].append(self.get_sku(response))

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
        return [Request(url=url, callback=self.parse_colour_requests) for url in urls]

    def get_size_requests(self, raw_product):
        attrs = raw_product['product']['variationAttributes']
        raw_sizes = next((a['values'] for a in attrs if a['attributeId'].lower() == 'size'), [])
        return [Request(s['url'], callback=self.parse_skus) for s in raw_sizes]

    def get_name(self, response):
        return response.css('.product-name::text').get()

    def get_care(self, response):
        care = response.css('.product-spec-list dt:contains("material") + dd::text').get(default='')
        return self.sanitize_list(care.split(','))

    def get_gender(self, response):
        gender_candidate = response.css('.product-spec-list dd::text').get().lower()

        for tag, gender in self.genders:
            if tag in gender_candidate:
                return gender

        return 'unisex-adults'

    def get_categories(self, response):
        return self.sanitize_list(response.css('.breadcrumb a::text').getall()[1:-1])

    def get_product_id(self, response):
        return response.css('.product-id::text').get()

    def get_description(self, response):
        css = '.product-detail-card'
        css = f'{css}.features li::text, {css}.details .card-text::text'
        return self.sanitize_list(response.css(css).getall())

    def get_image_urls(self, raw_product):
        return [url['url'] for url in raw_product['product']['images']['large']]

    def get_sku(self, response):
        raw_product = json.loads(response.text)
        raw_colour, raw_size = self.get_raw_colour_and_size(raw_product)

        sku = self.get_pricing_details(raw_product)
        if raw_colour:
            sku['colour'] = raw_colour
        sku['size'] = raw_size or 'One Size'
        sku['sku_id'] = f'{sku.get("colour", "")}-{sku["size"]}'
        sku['out_of_stock'] = self.get_out_of_stock(raw_product)

        return sku

    def get_raw_attribute(self, raw_product, attribute):
        attrs = raw_product['product']['variationAttributes']
        return next((a['values'] for a in attrs if a['attributeId'].lower() == attribute), [])

    def get_raw_colour_and_size(self, raw_product):
        raw_colour = raw_size = ''

        for attrs in raw_product['product']['variationAttributes']:
            if attrs['attributeId'].lower() in ('color', 'colour'):
                raw_colour = attrs['displayValue']
            if attrs['attributeId'].lower() == 'size':
                raw_size = attrs['displayValue']

        return raw_colour, raw_size

    def get_pricing_details(self, raw_product):
        price_map = raw_product['product']['price']
        pricing = {'price': self.sanitize_price(price_map['sales']['decimalPrice'])}
        pricing['currency'] = price_map['sales']['currency']

        if price_map.get('list'):
            pricing['previous_prices'] = [self.sanitize_price(price_map['list']['decimalPrice'])]

        return pricing

    def get_out_of_stock(self, raw_product):
        messages = raw_product['product']['availability']['messages']
        return not bool(re.findall(r'>(.*?)</div>', messages[0]))

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs if i and i.strip()]

    def sanitize_price(self, price):
        return float(''.join(re.findall(r'\d+', price)))


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

    cookie = {
        'KP_UID': 'ac4118db-cae9-6512-6cba-df08719614e9'
    }

    product_css = '.product-grid'
    listing_css = [
        '.nav-item.dropdown',
        '.product-list-cards',
        '.show-more'
    ]

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback=speedo_parser.parse),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css, tags=['a', 'button'],
                                          attrs=['href', 'data-url']), callback='parse'),
    ]

    def start_requests(self):
        return [Request(url, cookies=self.cookie.copy()) for url in self.start_urls]

    def parse(self, response):
        requests = super(SpeedoCrawler, self).parse(response)
        trail = self.add_trail(response)

        return [r.replace(meta={**r.meta, 'trail': trail.copy()}) for r in requests]

    def add_trail(self, response):
        new_trail = [(response.css('head title::text').get(), response.url)]
        return response.meta.get('trail', []) + new_trail

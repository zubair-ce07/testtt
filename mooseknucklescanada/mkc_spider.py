import itertools as it
import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider

from mooseknucklescanada.items import MKCItem


class MKCParser(Spider):
    market = 'CA'
    currency = 'CAD'
    name = 'mkcparser'
    brand = 'Moose Knuckles'
    retailer = 'mooseknuckles-ca'

    allowed_domains = [
        'mooseknucklescanada.com'
    ]

    genders = [
        ('women', 'women'),
        ('woman', 'women'),
        ('ladies', 'women'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('man', 'men'),
        ('men', 'men'),
        ('mens', 'men'),
        ('adults', 'unisex-adults'),
        ('kids', 'unisex-kids'),
    ]

    def parse(self, response):
        item = MKCItem()
        item['url'] = response.url
        item['brand'] = self.brand
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['trail'] = response.meta.get('trail', [])
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['category'] = self.get_categories(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['skus'] = self.get_skus(response)

        if not item['skus']:
            item['out_of_stock'] = True

        return item

    def get_name(self, response):
        return response.css('.product-name h1::text').get()

    def get_care(self, response):
        css = 'dt:contains("Additional Information") + dd li::text'
        return self.sanitize_list(response.css(css).getall())

    def get_gender(self, response):
        gender_candidate = response.css('.std::text').get().lower()

        for tag, gender in self.genders:
            if tag in gender_candidate:
                return gender

        return 'unisex-adults'

    def get_categories(self, response):
        css = '.short-description .std::text, button.btn-cart::attr(data-category)'
        return self.sanitize_list(response.css(css).getall())

    def get_image_urls(self, response):
        return response.css('.product-image-gallery img::attr(data-src)').getall()

    def get_description(self, response):
        return self.sanitize_list(response.css('.tab-content .std::text').getall())

    def get_product_id(self, response):
        return response.css('meta[property="product:retailer_item_id"]::attr(content)').get()

    def get_skus(self, response):
        skus = []
        if self.get_out_of_stock(response):
            return skus

        raw_skus = self.get_raw_skus(response)
        pricing_details = self.get_pricing_details(response)

        for colour, size in raw_skus:
            if not colour and size:
                continue

            sku = pricing_details.copy()
            if colour.get('label'):
                sku['colour'] = colour['label']
                sku['sku_id'] = f'{colour["id"]}'
            if size.get('label'):
                sku['size'] = size['label']
                sku['sku_id'] = f'{sku.get("sku_id", "")}{size["id"]}'
            if sku.get('colour') and sku.get('size'):
                oos = it.product(colour['products'], size['products'])
                sku['out_of_stock'] = not any([c == s for c, s in oos])
            elif colour or size:
                sku['out_of_stock'] = False

            skus.append(sku)

        return skus

    def get_raw_skus(self, response):
        attributes = response.css('#product-options-wrapper script').re_first(r'{.*}')
        attributes_map = json.loads(attributes)['attributes']
        raw_colours, raw_sizes = [''], ['']

        for key in attributes_map.keys():
            if attributes_map[key]['label'].lower() in ('color', 'colour'):
                raw_colours = attributes_map[key]['options']
            if attributes_map[key]['label'].lower() == 'size':
                raw_sizes = attributes_map[key]['options']

        return it.product(raw_colours, raw_sizes)

    def get_out_of_stock(self, response):
        css = 'meta[property="product:availability"]::attr(content)'
        return response.css(css).get() != 'in stock'

    def get_pricing_details(self, response):
        pricing_map = json.loads(response.css('div.main script').re_first(r'{.*}'))
        return {
            'currency': self.currency,
            'price': self.sanitize_price(pricing_map['productPrice']),
            'previous_prices': [self.sanitize_price(pricing_map['productOldPrice'])]
        }

    def sanitize_price(self, price, to_cents=True):
        if isinstance(price, str):
            price = float(''.join(re.findall(r'\d+', price)))
        if to_cents:
            price *= 100

        return price

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs if i and i.strip()]


class MKCCrawler(CrawlSpider):
    name = 'mkccrawler'
    mkc_parser = MKCParser()

    allowed_domains = [
        'mooseknucklescanada.com'
    ]

    start_urls = [
        'https://www.mooseknucklescanada.com/en/'
    ]

    product_css = '.ls-products-grid__images'
    listing_css = ['.nav-primary', '.toolbar-bottom .next.i-next']

    rules = [
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css), callback='parse')
    ]

    def parse(self, response):
        requests = super(MKCCrawler, self).parse(response)
        trail = self.add_trail(response)
        return [r.replace(meta={**r.meta, 'trail': trail.copy()}) for r in requests]

    def parse_product(self, response):
        yield self.mkc_parser.parse(response)

    def add_trail(self, response):
        new_trail = [(response.css('head title::text').get(), response.url)]
        return response.meta.get('trail', []) + new_trail

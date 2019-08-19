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
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['category'] = self.get_categories(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['trail'] = response.meta.get('trail', [])

        oos = self.get_out_of_stock(response)
        key, value = ('out_of_stock', oos) if oos else ('skus', self.get_out_of_stock(response))
        item[key] = value

        return item

    def get_name(self, response):
        return response.css('.product-name h1::text').get()

    def get_care(self, response):
        care_css = '#collateral-tabs .tab-container:nth-child(4) .tab-content li::text'
        return self.sanitize_list(response.css(care_css).getall())

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
        attributes = response.css('#product-options-wrapper script').re_first(r'{.*}')
        attributes_map = json.loads(attributes)['attributes']
        raw_colours, raw_sizes = attributes_map['141']['options'], attributes_map['142']['options']
        pricing_details = self.get_pricing_details(response)
        skus = []

        for raw_colour in raw_colours:
            for product in raw_colour['products']:
                for raw_size in raw_sizes:
                    if not product in raw_size['products']:
                        continue
                    sku = {**pricing_details}
                    sku['size'] = raw_size['label']
                    sku['colour'] = raw_colour['label']
                    sku['sku_id'] = f'{sku["colour"]}_{sku["size"]}'
                    skus.append(sku)
                    break

        return skus

    def get_out_of_stock(self, response):
        out_of_stock = response.css('meta[property="product:availability"]::attr(content)').get()
        return out_of_stock != 'in stock'

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

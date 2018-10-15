import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from loropiana.items import LoropianaItem


class LoropianaParse:
    def parse_product(self, response):
        item_trail = response.meta.get('trail', [])
        item_trail.append((response.css('head title::text').extract_first().strip(), response.url))

        item = LoropianaItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['trail'] = item_trail
        item['category'] = self.category(response)
        item['brand'] = response.css('.top-bar a::attr(title)').extract_first()
        item['product_name'] = response.css('.product-info .t-h2::text').extract_first()
        item['gender'] = self.gender(item.get('category'))
        item['care'] = self.care(response)
        item['description'] = self.description(response)
        item['image_urls'] = []
        item['url'] = response.url
        item['skus'] = []

        color_codes = self.add_skus(response, item, meta={
            'currency': self.currency(response),
            'price': self.price(response)
        })

        yield scrapy.Request(url=self.image_detail_url(item.get('retailer_sku'), color_codes.pop()),
                             callback=self.add_image_urls, meta={
                'product_details': item,
                'color_codes': color_codes
            })

    def add_image_urls(self, response):
        item = response.meta.get('product_details')
        images_detail = json.loads(response.text)
        color_codes = response.meta.get('color_codes')

        for images in images_detail:
            item['image_urls'] += [format.get('url') for format in images.get('formats') if
                                   'LARGE' in format.get('url', '')]

        if color_codes:
            yield scrapy.Request(url=self.image_detail_url(item.get('retailer_sku'), color_codes.pop()),
                                 callback=self.add_image_urls, meta={
                    'product_details': item,
                    'color_codes': color_codes
                })
        else:
            yield item

    def add_skus(self, response, item, meta):
        skus = []
        color_codes = []
        for color in self.skus(response):
            color_codes.append(color.get('code'))
            for size in color['sizes']:
                skus += [{'sku_id': size['variantCode'],
                          'size': size['code'],
                          'currency': meta['currency'],
                          'price': meta['price']
                          }]
        item['skus'] += skus
        return color_codes

    def gender(self, details):
        if 'Men' in details:
            gender = 'men'
        elif 'Women' in details:
            gender = 'Women'
        elif 'girl' in details:
            gender = 'girl'
        elif 'boy' in details:
            gender = 'boy'
        elif 'girl or boy' in details and 'baby' in details or 'Children' in details:
            gender = 'unisex-kids'
        else:
            gender = 'unisex-adults'
        return gender

    def retailer_sku(self, response):
        raw_retailer_sku = response.css('.t-product-copy::text').extract_first()
        return re.findall(r'[A-Z0-9]+', raw_retailer_sku)[0]

    def category(self, response):
        sub_category = response.css('.t-product-breadcrumps a::text').extract_first()
        main_category = response.css(
            '.t-product-breadcrumps::text').extract_first().strip().split('>')
        main_category = [category.strip()
                         for category in main_category if category != '']
        if sub_category:
            main_category.append(sub_category.strip())
        return main_category

    def description(self, response):
        sub_description = response.css('.t-pdp-page-section-title.title ~ p::text').extract_first()
        return f"{response.css('.t-caption::text').extract_first()} {sub_description}"

    def care(self, response):
        raw_care = response.css('button[aria-label="Care & Maintenance"] ~ .content ::text').extract()
        return [d.strip() for d in raw_care if d.strip()]

    def currency(self, response):
        raw_currency = response.css('.t-product-cta-price::text').extract_first()
        return re.findall('[A-Z]+', raw_currency)[0]

    def price(self, response):
        raw_price = response.css('.t-product-cta-price::text').extract_first()
        return int(''.join(re.findall('[0-9]+', raw_price)))

    def color_code(self, response):
        return response.css('.colourvalue .t-caps.t-grey::text').extract_first()[1:-1]

    def skus(self, response):
        return json.loads(response.css('#js-pdp-initial-variants::attr(value)').extract_first())

    def image_detail_url(self, retailer_sku, color_code):
        return f"https://uk.loropiana.com/en/api/pdp/get-images?articleCode={retailer_sku}&colorCode={color_code}"


class LoropianaCrawler(CrawlSpider):
    name = 'loropiana_spider'
    allowed_domains = ['uk.loropiana.com']
    start_urls = ['https://uk.loropiana.com/en']
    loropiana_parse = LoropianaParse()

    rules = [Rule(LinkExtractor(restrict_css='[class=menu-mask]'), callback='parse'),
             Rule(LinkExtractor(restrict_css='.category-results-grid'), callback=loropiana_parse.parse_product)]

    def parse(self, response):
        req = super().parse(response)
        for r in req:
            r.meta['trail'] = [(response.css('head title::text').extract_first().strip(), response.url)]
            yield r

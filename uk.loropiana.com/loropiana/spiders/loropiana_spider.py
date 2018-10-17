import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from loropiana.items import LoropianaItem


class LoropianaParse:
    def parse(self, response):
        item = LoropianaItem()

        item['retailer_sku'] = self.common_data(response)['id']
        item['trail'] = response.meta.get('trail')
        item['category'] = self.category(response)
        item['brand'] = self.common_data(response)['brand']
        item['name'] = self.common_data(response)['name']
        item['care'] = self.care(response)
        item['description'] = self.description(response)
        item['gender'] = self.gender(item['category'] + item['description'])
        item['image_urls'] = []
        item['url'] = response.url
        item['skus'] = []

        requests = [response.follow(url=self.color_request_url(item['retailer_sku'], color), callback=self.parse_skus,
                                    meta={'item': item, 'price': self.common_data(response)['price'],
                                          'currency': self.currency(response)}) for color in
                    self.color_codes(response)] + [
                       response.follow(url=self.image_request_url(item['retailer_sku'], color),
                                       callback=self.parse_image_urls, meta={'item': item}) for color in
                       self.color_codes(response)]

        return self.next_request(item, requests)

    def next_request(self, item, resquests):
        if resquests:
            next_request = resquests.pop()
            next_request.meta['resquests'] = resquests
            return next_request
        else:
            return item

    def parse_skus(self, response):
        raw_sku = json.loads(response.text)
        item = response.meta['item']

        for color in raw_sku:
            for size in color.get('sizes', []):
                sku = dict()
                sku['sku_id'] = size['variantCode']
                sku['color'] = color['description']
                sku['price'] = response.meta['price']
                sku['currency'] = response.meta['currency']
                sku['size'] = 'One_size' if size['code'] == 'NR' else size['code']
                if size['stock']['stockLevelStatus']['code'] == "outOfStock":
                    sku['outOfStock'] = True

                item['skus'] += [sku]

        return self.next_request(item, response.meta['resquests'])

    def parse_image_urls(self, response):
        item = response.meta['item']
        raw_images = json.loads(response.text)

        for images in raw_images:
            item['image_urls'] += [format['url'] for format in images.get('formats') if 'LARGE' in format.get('url')]

        return self.next_request(item, response.meta['resquests'])

    def color_codes(self, response):
        raw_colors = json.loads(response.css('#js-pdp-initial-variants::attr(value)').extract_first())
        return [color.get('code') for color in raw_colors]

    def gender(self, details):
        gender = 'unisex-adults'
        genders = {'Men': 'men', 'girl': 'girl', 'Women': 'women', 'boy': 'boy', 'girl or boy': 'unisex-kids',
                   'Children': 'unisex-kids'}

        for key in genders.keys():
            if key in details:
                gender = genders[key]

        return gender

    def category(self, response):
        raw_categoty = self.common_data(response)['category'].split('/')
        return [category for category in raw_categoty if category != '']

    def description(self, response):
        return response.css('.t-caption::text, .t-pdp-page-section-title.title ~ p::text').extract()

    def care(self, response):
        raw_care = response.css('button[aria-label="Care & Maintenance"] ~ .content ::text').extract()
        return [d.strip() for d in raw_care if d.strip()]

    def currency(self, response):
        raw_currency = response.css('.t-product-cta-price::text').extract_first()
        return re.findall('[A-Z]+', raw_currency)[0]

    def common_data(self, response):
        return json.loads(response.css('#js-gtm-pdp-landing::attr(data-gtm-info)').extract_first())

    def color_request_url(self, retailer_sku, color_code):
        return f"https://uk.loropiana.com/en/api/pdp/product-variants?articleCode={retailer_sku}&colorCode={color_code}"

    def image_request_url(self, retailer_sku, color_code):
        return f"https://uk.loropiana.com/en/api/pdp/get-images?articleCode={retailer_sku}&colorCode={color_code}"


class LoropianaCrawler(CrawlSpider):
    name = 'loropiana_spider'
    allowed_domains = ['uk.loropiana.com']
    start_urls = ['https://uk.loropiana.com/en']
    loropiana_parse = LoropianaParse()

    listing_css = '[class=menu-mask]'
    catagorise_css = '.category-results-grid'

    rules = [Rule(LinkExtractor(restrict_css=[listing_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=[catagorise_css]), callback=loropiana_parse.parse)]

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first().strip(), response.url)]
        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

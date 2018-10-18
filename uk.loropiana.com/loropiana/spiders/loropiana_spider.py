import json
import re
from urllib.parse import urlencode

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from loropiana.items import LoropianaItem


class LoropianaParse:
    ONE_SIZES = ['NR']
    COLOUR_REQUEST_URL = "https://uk.loropiana.com/en/api/pdp/product-variants?{}"
    IMAGES_REQUEST_URL = "https://uk.loropiana.com/en/api/pdp/get-images?{}"

    def parse(self, response):
        item = LoropianaItem()
        raw_product = self.common_data(response)

        item['retailer_sku'] = raw_product['id']
        item['brand'] = raw_product['brand']
        item['name'] = raw_product['name']
        item['trail'] = response.meta['trail']
        item['care'] = self.care(response)
        item['url'] = response.url
        item['category'] = self.category(response)
        item['description'] = self.description(response)
        item['gender'] = self.gender(item)
        item['image_urls'] = []
        item['skus'] = []

        item['meta'] = self.image_requests(item, response) + self.colour_requests(item, response)

        return self.next_requests(item)

    def parse_skus(self, response):
        item = response.meta['item']
        common_sku = {}
        common_sku['price'] = response.meta['price']
        common_sku['currency'] = response.meta['currency']

        for colour in json.loads(response.text):
            common_sku['colour'] = colour['description']

            for size in colour['sizes']:
                sku = common_sku.copy()

                sku['sku_id'] = size['variantCode']
                sku['size'] = 'One size' if size['code'] in self.ONE_SIZES else size['code']
                if size['stock']['stockLevelStatus']['code'] == "outOfStock":
                    sku['outOfStock'] = True

                item['skus'] += [sku]

        return self.next_requests(item)

    def parse_image_urls(self, response):
        item = response.meta['item']

        for raw_image_url in json.loads(response.text):
            item['image_urls'] += [image_format['url'] for image_format in raw_image_url['formats'] if
                                   'LARGE' in image_format['url']]

        return self.next_requests(item)

    def next_requests(self, item):
        if item['meta']:
            next_request = item['meta'].pop()
            return next_request
        else:
            del item['meta']
            return item

    def colour_requests(self, item, response):
        request_meta = {'item': item, 'price': self.common_data(response)['price'],
                        'currency': self.currency(response)}
        colour_requests = []

        for colour in self.colour_codes(response):
            params = {"articleCode": item['retailer_sku'], "colorCode": colour}
            request_url = self.COLOUR_REQUEST_URL.format(urlencode(params))
            colour_requests.append(
                response.follow(url=request_url, callback=self.parse_skus, meta=request_meta))

        return colour_requests

    def image_requests(self, item, response):
        image_requests = []

        for colour in self.colour_codes(response):
            params = {"articleCode": item['retailer_sku'], "colorCode": colour}
            request_url = self.IMAGES_REQUEST_URL.format(urlencode(params))
            image_requests.append(
                response.follow(url=request_url, callback=self.parse_image_urls, meta={'item': item}))

        return image_requests

    def colour_codes(self, response):
        css = '#js-pdp-initial-variants::attr(value)'
        raw_colours = json.loads(response.css(css).extract_first())
        return [colour['code'] for colour in raw_colours]

    def gender(self, item):
        soup = item['category'] + item['description']
        gender = 'unisex-adults'
        genders = {'Men': 'men', 'girl': 'girl', 'Women': 'women', 'boy': 'boy', 'girl or boy': 'unisex-kids',
                   'Children': 'unisex-kids'}

        for key, value in genders.items():
            if key in soup:
                gender = value

        return gender

    def category(self, response):
        raw_categoty = self.common_data(response)['category'].split('/')
        return [category for category in raw_categoty if category]

    def description(self, response):
        return response.css('.t-caption::text, .t-pdp-page-section-title.title ~ p::text').extract()

    def care(self, response):
        css = 'button[aria-label="Care & Maintenance"] ~ .content ::text'
        raw_care = response.css(css).extract()
        return [d.strip() for d in raw_care if d.strip()]

    def currency(self, response):
        css = '.t-product-cta-price::text'
        raw_currency = response.css(css).extract_first()
        return re.findall('[A-Z]+', raw_currency)[0]

    def common_data(self, response):
        return json.loads(response.css('#js-gtm-pdp-landing::attr(data-gtm-info)').extract_first())


class LoropianaCrawler(CrawlSpider):
    name = 'loropiana_spider'
    allowed_domains = ['uk.loropiana.com']
    start_urls = ['https://uk.loropiana.com/en']
    loropiana_parse = LoropianaParse()

    listing_css = '.menu-mask'
    product_css = '.category-results-grid'

    rules = [Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback=loropiana_parse.parse)]

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first().strip(), response.url)]
        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

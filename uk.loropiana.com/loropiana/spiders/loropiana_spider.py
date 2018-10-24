import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameter

from loropiana.items import LoropianaItem


class LoropianaParser:
    one_size = ['NR']
    colour_url_t = "https://uk.loropiana.com/en/api/pdp/product-variants"
    image_request_url_t = "https://uk.loropiana.com/en/api/pdp/get-images"

    gender_map = {'children': 'unisex-kids', 'girl or boy': 'unisex-kids', 'girl': 'girl',
                  'boy': 'boy', 'women': 'women', 'men': 'men'}

    def parse(self, response):
        item = LoropianaItem()

        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['brand'] = self.extract_brand(response)
        item['name'] = self.extract_name(response)
        item['trail'] = self.extract_trail(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_category(response)
        item['description'] = self.extract_description(response)
        item['gender'] = self.extract_gender(item)
        item['url'] = response.url
        item['image_urls'] = []
        item['skus'] = []

        requests = self.generate_image_requests(response) + self.generate_colour_requests(response)
        item['meta'] = {'requests': requests}

        return self.generate_request_or_item(item)

    def parse_skus(self, response):
        item = response.meta['item']
        item['skus'] += self.extract_skus(response)

        return self.generate_request_or_item(item)

    def parse_image_urls(self, response):
        item = response.meta['item']
        item['image_urls'] += self.extract_image_urls(response)

        return self.generate_request_or_item(item)

    def generate_request_or_item(self, item):
        """
        Return request if item['meta'] have request else return item
        :param item:
        :return request_or_item:
        """
        if item.get('meta') is None:
            return item

        if item['meta'].get('requests'):
            next_request = item['meta']['requests'].pop()
            next_request.meta['item'] = item
            return next_request

        del item['meta']
        return item

    def extract_skus(self, response):
        """
        Extract skus from response
        :param response: response must contain json string text and have 'common' sku in meta
        :return: skus as list of dicts
        """
        skus = []
        raw_color = json.loads(response.text)

        common_sku = response.meta['common']
        common_sku['colour'] = raw_color[0]['description']

        for size in raw_color[0]['sizes']:
            sku = common_sku.copy()

            sku['sku_id'] = size['variantCode']
            sku['size'] = 'One size' if size['code'] in self.one_size else size['code']

            if size['stock']['stockLevelStatus']['code'] == "outOfStock":
                sku['out_of_stock'] = True

            skus += [sku]
        return skus

    def extract_image_urls(self, response):
        """
        Extract image urls from response
        :param response: response must contain json string text
        :return: Image urls list
        """
        image_urls = []

        for raw_image_url in json.loads(response.text):
            image_urls += [image_url['url'] for image_url in raw_image_url['formats'] if
                           'LARGE' in image_url['url']]

        return image_urls

    def generate_colour_requests(self, response):
        """
        Create requests for each colour skus
        :param response: response of product page
        :return: list of requests
        """
        raw_product = self.extract_raw_product(response)
        common_sku = {'price': raw_product['price'],
                      'currency': self.extract_currency(response)}
        meta = {'common': common_sku}

        requests = []

        url = add_or_replace_parameter(self.colour_url_t, 'articleCode', raw_product['id'])

        for colour in self.extract_colour_codes(response):
            url = add_or_replace_parameter(url, 'colorCode', colour)

            requests.append(response.follow(url, callback=self.parse_skus, meta=meta))

        return requests

    def generate_image_requests(self, response):
        """
        Create requests for images of each colour
        :param response: response of product page
        :return: list of requests
        """
        image_requests = []

        url = add_or_replace_parameter(
            self.image_request_url_t, 'articleCode', self.extract_raw_product(response)['id'])

        for colour in self.extract_colour_codes(response):
            url = add_or_replace_parameter(url, 'colorCode', colour)

            image_requests.append(response.follow(url, callback=self.parse_image_urls))

        return image_requests

    def extract_colour_codes(self, response):
        css = '#js-pdp-initial-variants::attr(value)'
        raw_colours = json.loads(response.css(css).extract_first())
        return [colour['code'] for colour in raw_colours]

    def extract_retailer_sku(self, response):
        raw_product = self.extract_raw_product(response)
        return raw_product['id']

    def extract_brand(self, response):
        raw_product = self.extract_raw_product(response)
        return raw_product['brand']

    def extract_name(self, response):
        raw_product = self.extract_raw_product(response)
        return raw_product['name']

    def extract_trail(self, response):
        return response.meta['trail']

    def extract_gender(self, item):
        soup = ' '.join(item['category'] + item['description']).lower()

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

        return 'unisex-adults'

    def extract_category(self, response):
        raw_categoty = self.extract_raw_product(response)['category'].split('/')
        return [category.strip() for category in raw_categoty if category.strip()]

    def extract_description(self, response):
        css = '.t-caption::text, .desktop-details ' \
              '.t-pdp-page-section-title.title ~ p::text'
        return response.css(css).extract()

    def extract_care(self, response):
        css = 'button[aria-label="Care & Maintenance"] ~ .content ::text'
        raw_care = response.css(css).extract()
        return [d.strip() for d in raw_care if d.strip()]

    def extract_currency(self, response):
        css = '.t-product-cta-price::text'
        raw_currency = response.css(css).extract_first()
        if 'GBP' in raw_currency:
            return 'GBP'

    def extract_raw_product(self, response):
        css = '#js-gtm-pdp-landing::attr(data-gtm-info)'
        return json.loads(response.css(css).extract_first())


class LoropianaCrawler(CrawlSpider):
    name = 'loropiana_spider'
    allowed_domains = ['uk.loropiana.com']
    start_urls = ['https://uk.loropiana.com/en']

    listing_css = ['.menu-mask']
    product_css = ['.category-results-grid']

    rules = [Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')]

    LoropianaParser = LoropianaParser()

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first().strip(), response.url)]

        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

    def parse_item(self, response):
        return self.LoropianaParser.parse(response)

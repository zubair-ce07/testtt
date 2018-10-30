import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from lanebryant.items import LanebryantItem


class LanebryantParser:
    image_request_url_t = 'https://lanebryant.scene7.com/is/image/'

    def parse(self, response):
        item = LanebryantItem()

        item['trail'] = self.extract_trail(response)
        item['brand'] = self.extract_brand(response)
        item['skus'] = self.extract_skus(response)
        item['name'] = self.extract_name(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_category(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['description'] = self.extract_description(response)
        item['url'] = response.url
        item['gender'] = 'women'
        item['image_urls'] = []

        item['meta'] = {'requests': self.extract_image_requests(response)}

        return self.extract_next_request_or_item(item)

    def parse_image_urls(self, response):
        item = response.meta['item']
        item['image_urls'] += self.extract_image_urls(response)

        return self.extract_next_request_or_item(item)

    def extract_image_urls(self, response):
        raw_urls = json.loads(re.findall('{.+}', response.text)[0])['set']['item']

        urls = []

        if isinstance(raw_urls, dict):
            urls.append(f"{self.image_request_url_t}{raw_urls['i']['n']}")
        else:
            for raw_url in raw_urls:
                urls.append(f"{self.image_request_url_t}{raw_url['i']['n']}")

        return urls

    def extract_next_request_or_item(self, item):

        if item.get('meta') is None:
            return item

        if item['meta'].get('requests'):
            next_request = item['meta']['requests'].pop()
            next_request.meta['item'] = item
            return next_request

        del item['meta']
        return item

    def extract_skus(self, response):
        common_data = self.extract_common_data(response)

        raw_skus = common_data['pdpDetail']['product'][0]['skus']
        skus = []

        for raw_sku in raw_skus:
            sku = {}

            sku['sku_id'] = raw_sku['sku_id']

            sku['colour'] = self.extract_colour_name(response, raw_sku['color'])
            sku['size'] = self.extract_size(response, raw_sku['size'])

            sku['price'] = self.extract_price(raw_sku['prices']['sale_price'])
            sku['currency'] = self.extract_currency(raw_sku['prices']['sale_price'])

            if self.is_out_of_stock(response, raw_sku['sku_id']):
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def extract_price(self, raw_price):
        return float(raw_price[1:]) * 100

    def extract_currency(self, raw_currency):
        if '$' in raw_currency:
            return 'USD'

    def is_out_of_stock(self, response, sku_id):
        common_data = self.extract_common_data(response)

        product_id = common_data['pdpDetail']['product'][0]['product_id']
        raw_stock = common_data['inventoryDetail']['inventory']['products'][product_id]['skus']

        for stock_id, quantity in raw_stock.items():

            if stock_id == sku_id and quantity.get('show_threshold_message'):
                return True

    def extract_size(self, response, sku_id):
        common_data = self.extract_common_data(response)

        raw_sizes = common_data['pdpDetail']['product'][0]['all_available_sizes'][0]['values']

        for raw_size in raw_sizes:
            if raw_size['id'] == sku_id:
                return raw_size['value']

    def extract_colour_name(self, response, sku_id):
        common_data = self.extract_common_data(response)

        raw_colours = common_data['pdpDetail']['product'][0]['all_available_colors'][0]['values']

        for raw_colour in raw_colours:

            if raw_colour['id'] == sku_id:
                return raw_colour['name']

    def extract_image_requests(self, response):
        common_data = self.extract_common_data(response)

        raw_colours = common_data['pdpDetail']['product'][0]['all_available_colors'][0]['values']
        requests = []

        for raw_colour in raw_colours:
            url = f"https:{raw_colour['swatch_image']}".replace('swatch', 'ms?req=set,json')

            requests.append(response.follow(url, callback=self.parse_image_urls, dont_filter=True))

        return requests

    def extract_category(self, response):
        common_data = self.extract_common_data(response)
        raw_category = common_data['pdpDetail']['product'][0]['ensightenData'][0]['categoryPath']
        return raw_category.split(':')

    def extract_brand(self, response):
        css = '.mar-text-logo::text'
        return response.css(css).extract_first()

    def extract_care(self, response):
        raw_care = response.css('#tab1 ul ::text').extract()
        return [c.strip() for c in raw_care if c.strip()]

    def extract_description(self, response):
        css = '#tab1 p::text, #tab1 ul ::text'
        return response.css(css).extract()

    def extract_common_data(self, response):
        css = '#pdpInitialData::text'
        raw_data = response.css(css).extract_first()

        return json.loads(raw_data)

    def extract_retailer_sku(self, response):
        common_data = self.extract_common_data(response)
        return common_data['pdpDetail']['product'][0]['product_id']

    def extract_name(self, response):
        common_data = self.extract_common_data(response)
        return common_data['pdpDetail']['product'][0]['product_name']

    def extract_trail(self, response):
        return response.meta['trail']


class LanebryantCrawler(CrawlSpider):
    name = 'lanebryant_spider'
    allowed_domains = ['lanebryant.com']
    start_urls = ['https://www.lanebryant.com']

    listing_css = ['.mar-nav', '.mar-pagination']
    product_css = ['.mar-prd-product-item']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    lanebryant_parse = LanebryantParser()

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first().strip(), response.url)]

        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

    def parse_item(self, response):
        return self.lanebryant_parse.parse(response)

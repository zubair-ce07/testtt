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
        raw_urls = [raw_urls] if isinstance(raw_urls, dict) else raw_urls

        return [f"{self.image_request_url_t}{raw_url['i']['n']}" for raw_url in raw_urls]

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
        skus = []

        colour_map = self.extract_colour_map(response)
        size_map = self.extract_size_map(response)

        for raw_sku in self.extract_raw_product_details(response)['skus']:
            sku = {**self.extract_pricing(raw_sku['prices'])}

            sku['sku_id'] = raw_sku['sku_id']
            sku['colour'] = colour_map[raw_sku['color']]
            sku['size'] = size_map[raw_sku['size']]

            if self.is_out_of_stock(response, raw_sku['sku_id']):
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def extract_pricing(self, raw_prices):
        pricing = {}

        pricing['currency'] = 'USD' if '$' in raw_prices['sale_price'] else None

        prices = sorted([float(price[1:]) * 100 for _, price in raw_prices.items()])
        pricing['price'] = prices[0]

        if len(prices) > 1:
            pricing['previous_prices'] = prices[1:]

        return pricing

    def is_out_of_stock(self, response, sku_id):
        product_id = self.extract_raw_product_details(response)['product_id']
        raw_stock = self.extract_raw_inventory_details(response)[product_id]['skus']

        for stock_id, quantity in raw_stock.items():

            if stock_id == sku_id and quantity.get('show_threshold_message'):
                return True

    def extract_image_requests(self, response):
        raw_image_urls = self.extract_raw_product_details(response)

        requests = []

        for raw_colour in raw_image_urls['all_available_colors'][0]['values']:
            url = f"https:{raw_colour['swatch_image']}".replace('swatch', 'ms?req=set,json')

            requests.append(response.follow(url, callback=self.parse_image_urls, dont_filter=True))

        return requests

    def extract_category(self, response):
        raw_category = self.extract_raw_product_details(response)

        return raw_category['ensightenData'][0]['categoryPath'].split(':')

    def extract_brand(self, response):
        css = '.mar-text-logo::text'
        return response.css(css).extract_first()

    def extract_care(self, response):
        raw_care = response.css('#tab1 ul ::text').extract()
        return [c.strip() for c in raw_care if c.strip()]

    def extract_description(self, response):
        css = '#tab1 p::text, #tab1 ul ::text'
        return response.css(css).extract()

    def extract_retailer_sku(self, response):
        raw_product_details = self.extract_raw_product_details(response)
        return raw_product_details['product_id']

    def extract_name(self, response):
        raw_product_details = self.extract_raw_product_details(response)
        return raw_product_details['product_name']

    def extract_trail(self, response):
        return response.meta['trail']

    def extract_raw_product_details(self, response):
        raw_data = response.css('#pdpInitialData::text').extract_first()
        return json.loads(raw_data)['pdpDetail']['product'][0]

    def extract_raw_inventory_details(self, response):
        css = '#pdpInitialData::text'
        raw_data = response.css(css).extract_first()

        return json.loads(raw_data)['inventoryDetail']['inventory']['products']

    def extract_colour_map(self, response):
        raw_colours = self.extract_raw_product_details(response)

        colour_map = {}

        for raw_colour in raw_colours['all_available_colors'][0]['values']:
            colour_map[raw_colour['id']] = raw_colour['name']

        return colour_map

    def extract_size_map(self, response):
        raw_sizes = self.extract_raw_product_details(response)
        raw_sizes = raw_sizes['all_available_sizes'][0]['values']

        size_map = {}

        for raw_size in raw_sizes:
            size_map[raw_size['id']] = raw_size['value']

        return size_map


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

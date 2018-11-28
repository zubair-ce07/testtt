import json

import scrapy
from savagex.items import Item
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_parameter, add_or_replace_parameter


class SavageParseSpider(scrapy.Spider):
    name = 'savagex-parser'
    colour_url_t = "https://www.savagex.co.uk/api/products/{}"
    seen_ids = []

    def parse(self, response):
        product_id = self.extract_retailer_sku(response)
        if not self.is_unseen_item(product_id):
            return

        item = Item()
        item['retailer_sku'] = product_id
        item['name'] = self.extract_name(response)
        item['spider_name'] = self.name
        item['gender'] = 'women'
        item['industry'] = 'null'
        item['brand'] = 'Savage X'
        item['market'] = 'UK'
        item['retailer'] = 'savagex-uk'
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['trail'] = response.meta['trail']
        item['url'] = self.extract_product_url(response)
        item['category'] = self.extract_category(response)
        item['skus'] = []
        item['image_urls'] = []
        item['meta'] = {'requests': self.extract_colours_requests(response)}

        return self.next_request_or_item(item)

    def parse_colour(self, response):
        raw_colour = json.loads(response.text)
        item = response.meta['item']
        item['image_urls'] += self.extract_image_urls(raw_colour)
        item['skus'] = self.make_skus(raw_colour)

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if item['meta'].get('requests'):
            request = item['meta']['requests'].pop(0)
            request.meta['item'] = item
            return request

        del item['meta']
        return item

    def extract_colours_requests(self, response):
        colour_ids = response.css('.ColorSwatch__ColorRadioButton-qbijao-5::attr(value)').extract()

        return [Request(self.colour_url_t.format(colour_id), headers=response.request.headers,
                        callback=self.parse_colour) for colour_id in colour_ids]

    def make_skus(self, raw_product):
        skus = {}

        for raw_sku in raw_product['product_id_object_list']:
            sku = {'price': raw_product['retail_unit_price'],
                   'currency': 'GBP',
                   'colour': raw_product['color'],
                   'size': raw_sku['size']}

            if raw_sku['availability'] != 'in stock':
                sku['out_of_stock'] = True

            skus[raw_sku['item_id']] = sku

        return list(skus.values())

    def extract_care(self, response):
        return response.css('.ProductDescription__DetailsList-s19e216s-6 li::text').extract()

    def extract_description(self, response):
        return response.css('.ProductDescription__LongDescription-s19e216s-5::text').extract_first()

    def extract_name(self, response):
        return response.css('.ProductDetail__ProductName-rkmewc-4::text').extract_first()

    def extract_product_url(self, response):
        return response.url

    def extract_category(self, response):
        return [text.strip() for text, _ in response.meta['trail'] if text.strip()]

    def extract_image_urls(self, raw_colour):
        return ['https:' + image for image in raw_colour['image_view_list']]

    def extract_retailer_sku(self, response):
        script_css = 'script:contains("NEXT_DATA")::text'
        return response.css(script_css).re_first('"group_code":"(.*?)"')

    def is_unseen_item(self, product_id):
        if product_id not in self.seen_ids:
            self.seen_ids.append(product_id)
            return True


class SavageCrawlSpider(CrawlSpider):
    name = 'savagex-crawler'
    start_urls = ['https://www.savagex.co.uk/']
    allowed_domains = ['www.savagex.co.uk']

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36" \
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    listings_url_t = "https://www.savagex.co.uk/api/products?aggs=true&includeOutOfStock=true" \
                     "&page={}&size=28&defaultProductCategoryIds={}&sort=newarrivals&excludeFpls=13511"
    product_url_t = "https://www.savagex.co.uk/shop/{}-{}"

    savage_parser = SavageParseSpider()

    def parse(self, response):
        raw_menu = self.extract_menu(response)
        headers = {'x-api-key': raw_menu['api']['key'],
                   'x-tfg-storedomain': 'www.savagex.co.uk'
                   }

        for category_name, raw_category in raw_menu['productBrowser']['sections'].items():
            url = self.listings_url_t.format(1, raw_category['defaultProductCategoryIds'])
            meta = {'link_text': category_name, 'trail': self.add_trail(response)}
            yield Request(url, headers=headers,
                          meta=meta, callback=self.parse_listings)

    def parse_listings(self, response):
        raw_listings = json.loads(response.text)

        if not raw_listings['products']:
            return

        for raw_product in raw_listings['products']:
            url = self.product_url_t.format(raw_product['permalink'], raw_product['master_product_id'])
            meta = {'trail': self.add_trail(response)}
            yield Request(url, headers=response.request.headers, meta=meta, callback=self.parse_item)

        current_page = url_query_parameter(response.url, 'page') or '0'
        url = add_or_replace_parameter(response.url, 'page', int(current_page) + 1)
        meta = {'trail': self.add_trail(response)}
        yield Request(url, headers=response.request.headers, meta=meta, callback=self.parse_listings)

    def extract_menu(self, response):
        script_css = 'script:contains("CONFIG")::text'
        raw_menu = response.css(script_css).extract_first()
        raw_menu = raw_menu.strip('__CONFIG__ = ')
        return json.loads(raw_menu)

    def parse_item(self, response):
        return self.savage_parser.parse(response)

    def add_trail(self, response):
        return response.meta.get('trail') or [] + [(response.meta.get('link_text') or '', response.url)]

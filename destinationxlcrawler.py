import json

import scrapy
from destinationxl.items import DestinationxlItem, SizeItem
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_parameter


class DestinationxlParseSpider(scrapy.Spider):
    name = 'destinationxl-parser'
    start_urls = [
        'https://www.destinationxl.com/mens-big-and-tall-store/mens-tees/harbor-bay-moisture-wicking-pocket-t-shirt/cat140084/G3356']
    seen_ids = []

    color_url_t = '{}?&isSelection=true&attributes=color={}'
    product_url_t = 'https://www.destinationxl.com/public/v1/dxlproducts/{}/{}?'

    def parse(self, response):
        product_id = self.extract_base_sku(response)
        if not self.is_unseen_item(product_id):
            return

        item = DestinationxlItem()
        item['country_code'] = 'US'
        item['currency'] = 'USD'
        item['language_code'] = 'en'
        item['base_sku'] = product_id
        item['url'] = self.extract_product_url(response)

        category_info = self.extract_category_id(response)
        yield Request(self.product_url_t.format(category_info[0], category_info[1]),
                      meta={'item': item},
                      callback=self.parse_colors)

    def parse_colors(self, response):
        raw_product = json.loads(response.text)
        item = response.meta['item']
        item['brand'] = raw_product['brandName']
        item['description_text'] = raw_product['longDescription']
        item['category_names'] = self.extract_category_names(raw_product)

        for raw_color in raw_product['colorGroups']:

            if 'Save' in raw_color['name']:
                item['new_price_text'] = raw_color['name'].split(':')[0]
            else:
                item['old_price_text'] = raw_color['name']

            for color in raw_color['colors']:
                item['image_urls'] = [color['largeSwatchImageUrl'], color['swatchImageUrl']]
                item['color_name'] = color['name']
                item['color_code'] = color['id']
                item['identifier'] = '{}-{}'.format(item['base_sku'], item['color_code'])

                yield Request(self.color_url_t.format(response.url, color['id']),
                              meta={'item': item},
                              callback=self.extract_sizes_or_skus)

    def extract_sizes_or_skus(self, response):
        colour = json.loads(response.text)
        item = response.meta['item']

        if bool(colour['inStock']):
            item['available'] = 'True'

        if len(colour['sizes']) > 1:
            item['meta'] = {'requests': self.extract_sizes_requests(response)}
        else:
            item['meta'] = {}
            item['size_infos'] = self.make_skus(colour)

        return self.next_request_or_item(item)

    def parse_sizes(self, response):
        raw_product = json.loads(response.text)
        item = response.meta['item']
        size_dict = raw_product['sizes'][1]

        for size in size_dict['values']:

            if bool(size['available']):
                size_name = {size_dict['displayName']: size['name'],
                             raw_product['sizes'][0]['displayName']: response.meta['size']['name']
                             }
                size_identifier = '{}_{}'.format(size['name'], response.meta['size']['name'])

                sku = {'size_identifier': size_identifier,
                       'size_name': size_name
                       }

                sku['stock'] = 1

                item['size_infos'][response.meta['size']['name']] = sku

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if item['meta'].get('requests'):
            request = item['meta']['requests'].pop(0)
            request.meta['item'] = item
            yield request

        del item['meta']
        yield item

    def extract_sizes_requests(self, response):
        raw_product = json.loads(response.text)
        return [Request('{}@{}Size={}'.format(response.url, raw_product['sizes'][0]['displayName'], size['name']),
                        meta={'size': size}, callback=self.parse_sizes) for size in raw_product['sizes'][0]['values']]

    def make_skus(self, raw_product):
        skus = {}
        if len(raw_product['sizes']) > 0:
            for size in raw_product['sizes'][0]['values']:
                sku = {'size_identifier': size['name'],
                       'size_name': size['name']
                       }
                if bool(size['available']):
                    sku['stock'] = 1

                skus[size['name']] = sku

            return skus

    def extract_product_url(self, response):
        return response.url

    def is_unseen_item(self, product_id):
        if product_id not in self.seen_ids:
            self.seen_ids.append(product_id)
            return True

    def extract_base_sku(self, response):
        return response.css('.ng-star-inserted::attr(data-product-id)').extract_first()

    def extract_category_id(self, response):
        return response.url.split('/')[-2:]

    def extract_category_names(self, raw_product):
        return [breadcrumb['name'] for breadcrumb in raw_product['breadCrumbsItems']]


class DestinationxlCrawlSpider(CrawlSpider):
    name = 'destinationxl-crawler'
    start_urls = ['https://www.destinationxl.com/mens-big-and-tall-store',
                  'https://www.destinationxl.com/mens-big-and-tall-store/mens-shoes/cat130012?N=11070+4294944243&No=0&nocache=1541591936534']
    allowed_domains = ['www.destinationxl.com']

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36" \
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    destinationxl_parser = DestinationxlParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=('a.ng-trigger'),
                           deny=('/mens-shoes', '/brands', '/looks', '/everyday-specials')),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=('.switch-hover')), callback=destinationxl_parser.parse),
    )

    def parse(self, response):

        if not url_query_parameter(response.url, 'No') and response.url not in self.start_urls:
            for page in range(30, (int(self.extract_total_pages(response)) - 1) * 30, 30):
                url = '{}?No={}'.format(response.url, page)
                yield Request(url, callback=self.parse)

        yield from super(DestinationxlCrawlSpider, self).parse(response)

    def extract_total_pages(self, response):
        total_pages = response.css('.page-nos span:nth-last-child(-n+2)::text').extract()

        if total_pages[-1] == 'View All':
            return total_pages[-2]
        else:
            return total_pages[-1]

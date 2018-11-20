import html
import json
import re

import scrapy
from destinationxl.items import DestinationxlItem, SizeItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, replace_escape_chars
from w3lib.url import url_query_parameter


class DestinationxlParseSpider(scrapy.Spider):
    name = 'destinationxl-parser'
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
        item['meta'] = {}
        item['size_infos'] = []
        item['image_urls'] = []
        item['category_names'] = self.extract_category_names(response)

        category_info = self.extract_category_id(response)
        yield Request(self.product_url_t.format(category_info[0], category_info[1]),
                      meta={'item': item},
                      callback=self.parse_colors)

    def parse_colors(self, response):
        raw_product = json.loads(response.text)
        item = response.meta['item']

        item['title'] = raw_product['description']
        item['brand'] = raw_product['brandName']
        item['description_text'] = self.extract_description(raw_product)

        for raw_color in raw_product['colorGroups']:

            if 'Save' in raw_color['name']:
                item['new_price_text'] = raw_color['name'].split(':')[0]
            else:
                item['old_price_text'] = raw_color['name']

            for color in raw_color['colors']:
                item['image_urls'] = self.extract_image_urls(raw_product, color)
                item['color_name'] = color['name']
                item['color_code'] = color['id']
                item['identifier'] = '{}-{}'.format(item['base_sku'], item['color_code'])

                yield Request(self.color_url_t.format(response.url, color['id']),
                              meta={'item': item.copy()},
                              callback=self.extract_sizes_or_skus)

    def extract_sizes_or_skus(self, response):
        colour = json.loads(response.text)
        item = response.meta['item']

        if bool(colour['inStock']):
            item['available'] = 'True'

        if len(colour['sizes']) > 1:
            item['size_infos'] = []
            item['meta'] = {'requests': self.extract_sizes_requests(response)}

        else:
            item['size_infos'] = self.make_skus(colour)

        return self.next_request_or_item(item)

    def parse_sizes(self, response):
        raw_product = json.loads(response.text)
        item = response.meta['item']
        size_dict = raw_product['sizes'][1]

        for size in size_dict['values']:

            if bool(size['available']):
                size_name = {size_dict['displayName']: size['name'],
                             raw_product['sizes'][0]['displayName']: response.meta['size']
                             }
                size_identifier = '{}_{}'.format(size['name'], response.meta['size'])

                sku = {'size_identifier': size_identifier,
                       'size_name': size_name
                       }

                sku['stock'] = 1

                item['size_infos'].append(sku)

        return self.next_request_or_item(item.copy())

    def next_request_or_item(self, item):
        if item['meta'].get('requests'):
            request = item['meta']['requests'].pop(0)
            request.meta['item'] = item
            return request

        del item['meta']
        return item

    def extract_sizes_requests(self, response):
        raw_product = json.loads(response.text)
        requests = []
        for size in raw_product['sizes'][0]['values']:
            if bool(size['available']):
                if raw_product['sizes'][0]['displayName'] == 'shoe size':
                    raw_product['sizes'][0]['displayName'] = 'shoe'
                requests.append(
                    Request('{}@{}Size={}'.format(response.url, raw_product['sizes'][0]['displayName'], size['name']),
                            meta={'size': size['name']}, callback=self.parse_sizes))
        return requests

    def make_skus(self, raw_product):
        skus = []
        if len(raw_product['sizes']) > 0:
            for size in raw_product['sizes'][0]['values']:
                sku = {'size_identifier': size['name'],
                       'size_name': size['name']
                       }
                if bool(size['available']):
                    sku['stock'] = 1
                skus.append(sku)
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

    def extract_image_urls(self, response, color):
        images = []
        color = color['largeSwatchImageUrl'][:-17]
        images.append(color)
        index = re.findall(r'([0-9]+)', color)
        for image_count in range(1, response['alternateImagesCount'] + 1, 1):
            images.append(('{}{}_{}_alt{}'.format(color.split(index[0])[0], index[0],
                                                  color.split(index[0])[1], image_count)))
        return images

    def extract_description(self, raw_product):
        return self.clean_collected_data(html.unescape(raw_product['longDescription']))

    def extract_category_names(self, response):
        return '{} {}={}'.format(self.extract_category_breadcrumbs(response), response.meta['name'],
                                 response.meta['breadcrumbs'])

    def clean_collected_data(self, text):
        clean_text = remove_tags(text)
        return replace_escape_chars(clean_text)

    def extract_category_breadcrumbs(self, response):
        return response.css('breadcrumb.ng-star-inserted nav ul li a::attr(aria-label)').extract()[1:]


class DestinationxlCrawlSpider(CrawlSpider):
    name = 'destinationxl-crawler'
    start_urls = ['https://www.destinationxl.com/mens-big-and-tall-store']
    base_url_t = 'https://www.destinationxl.com'
    allowed_domains = ['www.destinationxl.com']

    logger_info = []

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36" \
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    destinationxl_parser = DestinationxlParseSpider()

    def parse(self, response):

        categories = self.extract_subcategories(response)
        for category in categories:
            yield response.follow(category, callback=self.parse_filters)

    def parse_filters(self, response):

        raw_category = self.extract_raw_category(response)
        for raw_filter in self.get_navigation(raw_category):
            if 'refinements' in raw_filter.keys():
                for applied_filter in raw_filter['refinements']:
                    url = applied_filter['navigationState'].split('&')[0]
                    self.logger_info.append(
                        'category={}, {}={}, total products={}'.format(response.url.split('/')[-2], raw_filter['name'],
                                                                       applied_filter['label'],
                                                                       applied_filter['count']))
                    yield response.follow(url,
                                          meta={'name': raw_filter['name'], 'breadcrumbs': applied_filter['label']},
                                          callback=self.parse_products)

    def parse_products(self, response):

        products = response.css('.switch-hover a::attr(href)').extract()
        for product in products:
            product = '{}{}'.format(self.base_url_t, product)
            yield Request(product, meta={'name': response.meta['name'], 'breadcrumbs': response.meta['breadcrumbs']},
                          callback=self.destinationxl_parser.parse)

        if not url_query_parameter(response.url, 'No') and self.extract_total_pages(response) != 0:
            for page in range(30, (int(self.extract_total_pages(response)) - 1) * 30, 30):
                url = '{}?No={}'.format(response.url.split('+')[0], page)
                yield Request(url, meta={'name': response.meta['name'], 'breadcrumbs': response.meta['breadcrumbs']},
                              callback=self.parse_products)

    def extract_total_pages(self, response):

        total_pages = response.css('.page-nos span:nth-last-child(-n+2)::text').extract()
        if total_pages:
            if total_pages[-1] == 'View All':
                return total_pages[-2]
            else:
                return total_pages[-1]
        else:
            return 0

    def extract_subcategories(self, response):
        return response.css('nav.ng-star-inserted ul li ul li:nth-child(n+2) a::attr(href)').extract()

    def extract_raw_category(self, response):
        raw_category = response.css('script#dxl-state').extract_first()
        raw_script = raw_category.split('<script id="dxl-state" type="application/json">')[1]
        clean_script = raw_script.strip('</script>')
        clean_category = clean_script.replace('&q;', '"')
        return json.loads(clean_category)

    def get_navigation(self, raw_category):
        return raw_category['plpResponse']['contents'][0]['SecondaryContent'][1]['contents'][0][
            'navigation']

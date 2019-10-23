import scrapy
import json
import re

import w3lib.url

from scrapy import Request
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from ..items import WhiteStuffItem


class WhiteStuffParser:

    def parse_details(self, response):
        item = WhiteStuffItem()
        item['retailer_sku'] = self.extract_retailor_sku(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['currency'] = self.extract_currency(response)
        item['img_urls'] = []
        item['skus'] = []

        item['request_queue'] = self.extract_skus_requests(response)

        yield self.get_item_or_request_to_yield(item)

    def extract_skus_requests(self, response):
        master_sku = response.css('::attr(data-variation-master-sku)').get()
        json_url = 'https://www.whitestuff.com/action/GetProductData-FormatProduct?Format=JSON&ReturnVariable=true'
        url = w3lib.url.add_or_replace_parameters(json_url, {'ProductID': master_sku})

        return [Request(url, callback=self.parse_skus)]

    def get_item_or_request_to_yield(self, item):
        if item['request_queue']:
            request_next = item['request_queue'].pop()
            request_next.meta['item'] = item
            return request_next

        del item['request_queue']
        del item['currency']
        return item

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="sku"]::text').get()

    def extract_gender(self, response):
        return response.css('.breadcrumb-list__item a::text').getall()[1]

    def extract_category(self, response):
        return self.clean(response.css('.breadcrumb-list__item a::text').getall())

    def extract_brand(self):
        return 'WhiteStuff'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return self.clean(response.css('[itemprop="name"]::text').get())

    def extract_description(self, response):
        return self.clean(response.css('.js-lineclamp::text').getall())

    def extract_care(self, response):
        return response.css('.ish-productAttributes ::text').getall()

    def extract_imgs_urls(self, images_dict):
        return [image['src'] for image in images_dict]

    def extract_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').get()

    def parse_skus(self, response):
        item = response.meta['item']
        product_info = self.load_product_info_json(response)

        for variant in product_info.values():
            sku = {'currency': item['currency']}
            sku['color'] = variant['colour']
            sku['size'] = variant['size']
            sku['previous_price'] = variant['listPrice']
            sku['price'] = variant['salePrice']
            sku['out_of_stock'] = not variant['inStock']
            sku['sku_id'] = sku['color'] + '_' + sku['size']
            item['img_urls'] += self.extract_imgs_urls(variant['images'])
            item['skus'].append(sku)

        yield self.get_item_or_request_to_yield(item)

    def load_product_info_json(self, response):
        product_info = re.search("(?<=\\'] = )(.*)(?<!;)", response.body, re.DOTALL | re.MULTILINE).group()
        return json.loads(product_info)['productVariations']


    def clean(self, list_to_strip):
        if isinstance(list_to_strip, basestring):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class WhiteStuffSpider(CrawlSpider):
    name = 'whitestuff'
    start_urls = [
        'https://www.whitestuff.com/',
    ]

    def __init__(self):
        self.whiteStuff_parser = WhiteStuffParser()
        self.domain = 'https://www.whitestuff.com'

    def parse(self, response):
        top_categories_sel = response.css('.navbar__item')[:4]
        for top_category_sel in top_categories_sel:
            top_menu_id = top_category_sel.css('::attr(data-testing-id)').get().split('-')[0]
            category_urls = top_category_sel.css('.navbar-subcategory__item a::attr(href)').getall()

            for url in category_urls:
                final_url = 'https://fsm6.attraqt.com/zones-js.aspx?version=19.3.8&siteId=eddfa3c1-7e81-4cea-84a4-' \
                            '0f5b3460218a&pageurl=' + url + '&zone0=banner&zone1=category&config_categorytree=' \
                            + self.get_category_tree(top_menu_id, url)
                yield response.follow(final_url, callback=self.parse_category)

    def parse_category(self, response):
        js_response = response.body_as_unicode()
        html_response = Selector(text=json.loads(re.findall('LM.buildZone\((.+)\);', js_response)[1])['html'])
        next_page = html_response.css('[rel="next"]::attr(href)').get()

        if next_page:
            url = self.domain + next_page
            next_url = 'https://fsm6.attraqt.com/zones-js.aspx?version=19.3.8&siteId=eddfa3c1-7e81-4cea-84a4-' \
                       '0f5b3460218a&pageurl=' + url + response.url[response.url.find('&zone0'):]
            yield response.follow(next_url, callback=self.parse_category)

        products_urls = html_response.css('.product-tile__title ::attr(href)').getall()

        for product_url_path in products_urls:
            yield response.follow(self.domain + product_url_path, callback=self.whiteStuff_parser.parse_details)

    def get_category_tree(self, top_menu_id, url):
        return top_menu_id + '%2F' + top_menu_id + '_' + url.split('/')[-2].replace('-', '_').replace(
            'and_', '').replace('womens', 'WW').replace('mens', 'MW')


class WhiteStuffItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()
    currency = scrapy.Field()


class WhitestuffPipeline(object):
    def process_item(self, item, spider):
        for sku in item['skus']:
            sku['price'] = float(re.search('\d*\.?\d+', sku['price']).group())*100
            sku['previous_price'] = float(re.search('\d*\.?\d+', sku['previous_price']).group())*100
        return item


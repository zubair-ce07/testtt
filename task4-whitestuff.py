import json
import re

from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameters, urljoin

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

        item['request_queue'] = self.extract_skus_requests(response)

        yield self.get_item_or_request_to_yield(item)

    def parse_skus(self, response):
        item = response.meta['item']
        raw_product = self.get_raw_product(response)
        item['image_urls'] = self.extract_imgs_urls(raw_product)
        item['skus'] = self.extract_skus(raw_product, item['currency'])

        yield self.get_item_or_request_to_yield(item)

    def extract_skus_requests(self, response):
        master_sku = response.css('::attr(data-variation-master-sku)').get()
        skus_info_url = 'https://www.whitestuff.com/action/GetProductData-FormatProduct?Format=JSON&ReturnVariable=true'
        url = add_or_replace_parameters(skus_info_url, {'ProductID': master_sku})

        return [response.follow(url, callback=self.parse_skus)]

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

    def extract_imgs_urls(self, product_info):
        img_urls = []
        for variant in product_info.values():
            img_urls.append([image['src'] for image in variant['images']])
        return img_urls

    def extract_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').get()

    def extract_skus(self, product_info, currency):
        skus = []
        for variant in product_info.values():
            sku = {'currency': currency}
            sku['color'] = variant['colour']
            sku['size'] = variant['size']
            sku['previous_price'] = variant['listPrice']
            sku['price'] = variant['salePrice']
            sku['out_of_stock'] = not variant['inStock']
            sku['sku_id'] = f"{sku['color']}_{sku['size']}"
            skus.append(sku)

        return skus

    def get_raw_product(self, response):
        product_info = re.search("(?<=\\'] = )(.*)(?<!;)", response.body.decode('utf-8'),
                                 re.DOTALL | re.MULTILINE).group()
        return json.loads(product_info)['productVariations']

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, str):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class WhiteStuffSpider(CrawlSpider):
    name = 'whitestuff'
    start_urls = [
        'https://www.whitestuff.com/',
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=('.navbar-subcategory__item a')), callback='parse_category'),
    )

    whiteStuff_parser = WhiteStuffParser()
    category_url_template = 'https://fsm6.attraqt.com/zones-js.aspx?version=19.3.8&siteId=eddfa3c1-7e81-' \
                            '4cea-84a4-0f5b3460218a&pageurl={}&zone0=banner&zone1=category&' \
                            'config_categorytree={}'
    def parse_category(self, response):
        category_tree = re.search('(?<=categorytree = ")(.*)(?=";)', response.text).group()
        category_url = self.category_url_template.format(response.url, category_tree)
        yield response.follow(category_url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        html_response = Selector(text=json.loads(re.findall('LM.buildZone\((.+)\);', response.text)[1])['html'])
        next_page = html_response.css('[rel="next"]::attr(href)').get()

        if next_page:
            url = urljoin(self.start_urls[0], next_page)
            next_url = self.category_url_template.format(url,
                                                         re.search('(?<=categorytree=)(.*)', response.url).group())
            yield response.follow(next_url, callback=self.parse_pagination)

        products_urls = html_response.css('.product-tile__title ::attr(href)').getall()
        for product_url_path in products_urls:
            yield response.follow(urljoin(self.start_urls[0], product_url_path),
                                  callback=self.whiteStuff_parser.parse_details)


class WhiteStuffItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()
    currency = scrapy.Field()


class WhitestuffPipeline(object):
    def process_item(self, item, spider):
        for sku in item['skus']:
            sku['price'] = float(re.search('\d*\.?\d+', sku['price']).group())*100
            sku['previous_price'] = float(re.search('\d*\.?\d+', sku['previous_price']).group())*100
        return item


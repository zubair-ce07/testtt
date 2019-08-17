import json
import re
from math import ceil

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider

from elabelz.items import ElabelzItem


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class ElabelzParseSpider(Spider):
    name = 'elabelzparse'
    product_url_t = 'https://www.elabelz.com/ae/product/{}/{}'

    def parse_products(self, response):
        raw_products_json = json.loads(response.text)
        for product_json in raw_products_json['products']:
            yield self.parse_item(product_json)

    def parse_item(self, product_json):
        item = ElabelzItem()
        item['retailer_sku'] = self.retailer_sku(product_json)
        item['name'] = self.product_name(product_json)
        item['gender'] = self.product_gender(product_json)
        item['category'] = self.product_category(product_json)
        item['description'] = self.product_description(product_json)
        item['url'] = self.product_url(product_json)
        item['brand'] = self.product_brand(product_json)
        item['care'] = self.product_care(product_json)
        item['image_urls'] = self.product_image_urls(product_json)
        item['skus'] = self.product_skus(product_json)
        return item

    def retailer_sku(self, product_json):
        return product_json['productNumber']

    def product_name(self, product_json):
        return product_json['name']

    def product_gender(self, product_json):
        return product_json['taxonomy']['gender']

    def product_category(self, product_json):
        taxonomy = product_json['taxonomy']
        return clean([taxonomy['category'], taxonomy.get('subCategory1', '')])

    def product_url(self, product_json):
        brand = self.product_brand(product_json)
        return self.product_url_t.format(brand, product_json['seourl'])

    def product_description(self, product_json):
        return [product_json.get['description']]

    def product_brand(self, product_json):
        return product_json['brandName']

    def product_care(self, product_json):
        return clean(product_json.get('washing', '').split('.'))

    def product_image_urls(self, product_json):
        return [images_url['url'] for images_url in product_json['images']]

    def product_skus(self, product_json):
        skus = {}

        for sku in product_json['stockProducts']:
            key = f'{sku["color"]}_{sku["size"]}'
            skus[key] = {
                'color': sku["color"],
                'size': sku['size'],
                'price': sku['price'],
                'previous_price': sku.get('fullPrice'),
            }

            if not sku["totalQuantity"]:
                skus[key]['out_of_stock'] = True

        return skus


class ElabelzCrawlSpider(CrawlSpider):
    name = 'elabelz'
    allowed_domains = ['elabelz.com']
    start_urls = ['https://www.elabelz.com/ae/']
    parse_spider = ElabelzParseSpider()

    headers = {
        'currency': '5be9a3741e418425a69adf6d',
        'Origin': 'https://www.elabelz.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    prod_per_page = 68
    request_url = 'https://api.elabelz.com/products/search'
    listing_css = ['.dgQ2N']
    category_css = ['._1QWPi']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_categories'),
    )

    def parse_categories(self, response):
        css = 'script:contains("dataManager")::text'
        category_json = json.loads(response.css(css).get())['props']['initialState']
        body = self.get_request_body(category_json)
        total_products = category_json['api']['products']['data']['metadata']['searchResult']
        total_pages = ceil(total_products / self.prod_per_page) + 1

        for page_number in range(0, total_pages):
            body['page'] = page_number
            yield Request(self.request_url, method='POST', body=json.dumps(body), headers=self.headers,
                          callback=self.parse_spider.parse_products, dont_filter=True)

    def get_request_body(self, category_json):
        query = category_json['state']['tracking']['page']['query']
        division = clean([query.get('division')])
        category = clean([query.get('category')])

        body = {"limit": self.prod_per_page,
                "seoParams": {"division": division,
                              "category": category}, }
        body.update(query)

        return body


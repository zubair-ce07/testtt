import json
import re
from math import ceil

from scrapy import Item, Field, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ElabelzItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    requests = Field()


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [st for st in raw_strs if st]
        return [re.sub('\s+', ' ', st).strip() for st in cleaned_strs]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class ElabelzSpider(CrawlSpider):
    name = 'elabelz'
    allowed_domains = ['elabelz.com']
    start_urls = [
        'https://www.elabelz.com/ae/'
    ]

    AED_hash = '5be9a3741e418425a69adf6d'
    headers = {
        'currency': AED_hash,
        'Origin': 'https://www.elabelz.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    product_url_t = 'https://www.elabelz.com/ae/product/{}/{}'
    req_url = 'https://api.elabelz.com/products/search'
    listing_css = ['.dgQ2N']
    category_css = ['._1QWPi']

    rules = (Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=category_css), callback='parse_categories'),)

    def parse_categories(self, response):
        total_pages = ceil(int(response.css('._3uvdp::text').get().split(' ')[0]) / 68) + 1
        category_json = json.loads(response.css('script:contains("dataManager")::text').get())
        query = category_json['props']['initialState']['state']['tracking']['page']['query']

        body = {
            "limit": 68,
            "seoParams": {
                "division": json.dumps(clean([query.get('division')])),
                "category": json.dumps(clean([query.get('category')]))
            },
            "filters": {},
            "page": 0
        }
        body.update(query)

        for page_number in range(1, total_pages):
            yield Request(self.req_url, method='POST', body=json.dumps(body),
                          headers=self.headers, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        raw_products_json = json.loads(response.text)

        for product_json in raw_products_json['products']:
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

            yield item

    def retailer_sku(self, prod_json):
        return prod_json['productNumber']

    def product_name(self, prod_json):
        return prod_json['name']

    def product_gender(self, prod_json):
        return prod_json['taxonomy']['gender']

    def product_category(self, prod_json):
        if prod_json['taxonomy'].get('subCategory1'):
            return [prod_json['taxonomy']['category'],
                    prod_json['taxonomy']['subCategory1']]
        return [prod_json['taxonomy']['category']]

    def product_url(self, prod_json):
        return self.product_url_t.format(self.product_brand(prod_json),
                                         prod_json['seourl'])

    def product_description(self, prod_json):
        return prod_json['description'].split('.')

    def product_brand(self, prod_json):
        return prod_json['brandName']

    def product_care(self, prod_json):
        return prod_json.get('washing').split('.')

    def product_image_urls(self, prod_json):
        return [images_url['url'] for images_url in prod_json['images']]

    def product_skus(self, prod_json):
        skus = {}
        for sku in prod_json['stockProducts']:
            skus[f'{sku["color"]}_{sku["size"]}'] = {
                'color': sku["color"],
                'size': sku['size'],
                'price': sku['price'],
                'previous_price': sku.get('fullPrice'),
                'out_of_stock': not bool(sku["totalQuantity"])
            }

        return skus


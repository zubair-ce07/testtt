import json
import re
import urllib.parse

from scrapy.spiders import Request

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, soupify

class Mixin:
    retailer = 'coach'
    default_brand = "Coach"


class MixinCN(Mixin):
    allowed_domains = ["china.coach.com"]
    retailer = Mixin.retailer + "-cn"
    market = 'CN'
    start_urls = ['https://china.coach.com/rest/default/V1/applet/categories']

    category_url_t = 'https://china.coach.com/rest/default/V2/applet/products/?catId={}&isInStock=1&page=1&pageSize=1000&sort=position&sortDir=asc'
    product_url_t = 'https://china.coach.com/rest/default/V1/applet/product/{}'


class CoachParseSpider(BaseParseSpider):

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate(garment, response)
        garment['meta'] = {'requests_queue': [self.raw_product_request(response)]}
        return self.next_request_or_garment(garment)

    def parse_raw_product(self, response):
        garment = response.meta['garment']
        raw_product = self.raw_product(response)

        garment['name'] = self.product_name(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)

        return self.next_request_or_garment(garment)

    def raw_product_request(self, response):
        data_re = 'window.D1M =\s*(.*);'
        raw_data = json.loads(re.search(data_re, response.text).group(1))
        return Request(self.product_url_t.format(urllib.parse.quote(raw_data['params']['sku'], safe='')), callback=self.parse_raw_product)

    def raw_product(self, response):
        return json.loads(response.text)['data']

    def product_name(self, raw_product):
        return raw_product['name']

    def product_description(self, raw_product):
        return [raw_product['shortDesc'] or '']

    def product_care(self, raw_product):
        return [raw_product['description'] or '']

    def product_id(self, response):
        return response.url.split('/')[-1].replace('.html','')

    def product_brand(self, raw_product):
        return raw_product['brand']['label']

    def image_urls(self, raw_product):
        image_urls = []
        for varient in raw_product['childProducts']:
            image_urls += [image['url'] for image in varient['images']]

        return image_urls

    def product_category(self, raw_product):
        if isinstance(raw_product['cats'], dict):
            raw_product['cats'] = list(raw_product['cats'].values())
        return [cat['name'] for cat in raw_product['cats']]

    def product_gender(self, raw_product):
        soup = soupify(self.product_category(raw_product))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, raw_product):
        skus = {}

        for raw_sku in raw_product['childProducts'] or [raw_product]:
            money_strs = [raw_sku['price'], raw_sku['orgPrice']]
            sku = self.product_pricing_common(None, money_strs)
            sku['colour'] = raw_sku['color']['label']
            sku['size'] = raw_sku['size']['label'] or self.one_size
            if raw_sku['stock'] == 0:
                sku['out_of_stock'] = True
            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus


class CoachCNParseSpider(MixinCN, CoachParseSpider):
    name = MixinCN.retailer + '-parse'


class CoachCrawlSpider(BaseCrawlSpider):

    def parse(self, response):
        raw_data = json.loads(response.text)

        links = []
        for item in raw_data['data']['items']:
            links += self.category_links(item)
        return [Request(link, callback=self.parse_category) for link in links]

    def parse_category(self, response):
        products = json.loads(response.text)['data']['items']
        return [Request(product['url'], callback=self.parse_item, meta=self.get_meta_with_trail(response))
                for product in products if product.get('sku')]

    def category_links(self, raw_data):
        if raw_data['level'] == 3:
            return [self.category_url_t.format(raw_data['id'])]
        links = []
        for item in raw_data['items']:
            links += self.category_links(item)
        return links


class CoachCNCrawlSpider(MixinCN, CoachCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = CoachCNParseSpider()

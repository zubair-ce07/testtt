import json
import re
from scrapy import Request
from .base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser
import urllib.parse


class Mixin:
    retailer = 'richards-br'
    allowed_domains = ['richards.com.br']
    lang = 'pt'
    market = 'BR'
    start_urls = ['http://www.richards.com.br']
    category_ids = [560931917, 3056766704, 43564721, 1005777739]
    gender_map = [
        ('1005777739', 'men'),
        ('43564721', 'women'),
        ('3056766704', 'girls'),
        ('560931917', 'boys')]


class RichardsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        raw_product = self.get_json(response)
        sku_id = raw_product['skuId']
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response)
        garment['gender'] = self.detect_gender_from_tokens(str(response.meta['id']), gender_map=self.gender_map)
        garment['name'] = raw_product['name']
        garment['brand'] = self.brand_name(garment['name'])
        garment['url'] = raw_product['url']
        garment['description'] = self.product_description(raw_product['details'])
        garment['care'] = self.product_care(raw_product['details'])
        garment['skus'] = {}
        garment['image_urls'] = []

        currency = self.currency(response)
        garment['meta'] = {'requests_queue': self.color_request(raw_product['id'], raw_product['colorList'], currency)}

        return self.next_request_or_garment(garment)

    def request_params(self, sku, prod_id):
        return {'imageProperties': 'thumb,large,zoom', 'productId': prod_id, 'selectedSkuId': sku}

    def color_request(self, prod_id, color_list, currency):
        requests = []
        for color in color_list:
            params = self.request_params(color['skuId'], prod_id)
            url_color = self.create_url(params)
            request = Request(url=url_color, callback=self.parse_color)
            request.meta['currency'] = currency
            requests.append(request)

        return requests

    def currency(self, response):
        return CurrencyParser.currency(clean(response.css('meta[property="og:price:currency"]::attr(content)'))[0])

    def brand_name(self, name):
        if "BIARRITZ" in name:
            return "BIARRITZ"
        elif "BIRKENSTOCK" in name:
            return "BIRKENSTOCK"
        return "RICHARDS"

    def parse_color(self, response):

        garment = response.meta['garment']
        raw_product = json.loads(response.text)
        currency = response.meta['currency']

        garment['skus'] = self.skus(garment['skus'], raw_product, currency, response)
        garment['image_urls'] = garment['image_urls'] + self.image_urls(raw_product['mediaSets'])

        return self.next_request_or_garment(garment)

    def product_description(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if not self.care_criteria(rd)]

    def product_care(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if self.care_criteria(rd)]

    def raw_description(self, raw_product):
        description, details = [], []
        if 'description' in raw_product.keys():
            description = [raw_product['description']['value']]
        if 'details' in raw_product.keys():
            details = [raw_product['details']['value']]
        return description+details

    def image_urls(self, images):
        return [img['zoom'] for img in images]

    def skus(self, skus, raw_product, currency, response):

        colors = raw_product['colorList']
        sizes = []
        price = [raw_product['atualPrice'], currency]
        price = self.product_pricing_common_new(response, money_strs=price)

        if 'sizeList' in raw_product.keys():
            sizes = raw_product['sizeList']
        color_sku = raw_product['skuId']
        color_name = self.color_name(colors, color_sku)

        for size in sizes:
            skus[color_sku + "_" + size['skuId']] = {"size": size['name'], 'price': price['price'],
                                                     'currency': price['currency'], 'out_of_stock': size['hasStock'],
                                                     'color': color_name}
        return skus

    def color_name(self, colors, color_sku):
        for color in colors:
            if color['skuId'] == color_sku:
                return color['name']

    def create_url(self, params):
        return 'http://www.richards.com.br/services/get-complete-product.jsp?' + urllib.parse.urlencode(params)

    def get_json(self, response):
        script = response.xpath('//script[contains(., "var globalProduct =")]/text()').extract()
        if script:
            raw_data = re.findall('var globalProduct = (.*);', script[0])[0]
            return json.loads(raw_data)


class RichardsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer+'-crawl'
    parse_spider = RichardsParseSpider()

    def parse(self, response):
        params = {'recsPerPage': 1000}
        for ids in self.category_ids:
            params.update({'N': int(ids)})
            url_params = urllib.parse.urlencode(params)
            url = self.start_urls[0] + '/services/records.jsp?' + url_params
            request = Request(url=url, callback=self.parse_urls)
            request.meta["id"] = int(ids)
            yield request

    def parse_urls(self, response):
        product_links = json.loads(response.text)
        ids = response.meta["id"]
        for record in product_links['records']:
            request = Request(url=record['url'], callback=self.parse_item)
            request.meta["id"] = ids
            yield request



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
    # category id used in post request to retrieve product from a specific gender
    gender_map = {'1005777739': 'men', '43564721': 'women', '3056766704': 'girls', '560931917': 'boys'}
    params = {'imageProperties': 'thumb,large,zoom', 'productId': 'id', 'selectedSkuId': 'sku'}


class RichardsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        raw_product = self.raw_product(response)
        sku_id = raw_product['skuId']
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response)
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

    def parse_color(self, response):

        garment = response.meta['garment']
        raw_product = json.loads(response.text)
        currency = response.meta['currency']

        garment['skus'] = self.skus(garment['skus'], raw_product, currency)
        garment['image_urls'] += self.image_urls(raw_product['mediaSets'])

        return self.next_request_or_garment(garment)

    def color_request(self, prod_id, color_list, currency):
        requests = []
        for color in color_list:
            self.params['selectedSkuId'] = color['skuId']
            self.params['productId'] = prod_id
            colour_url = self.create_url()
            requests.append(Request(url=colour_url, meta={'currency': currency}, callback=self.parse_color))
        return requests

    def currency(self, response):
        return CurrencyParser.currency(clean(response.css('meta[property="og:price:currency"]::attr(content)'))[0])

    def brand_name(self, name):
        if "BIARRITZ" in name:
            return "BIARRITZ"
        elif "BIRKENSTOCK" in name:
            return "BIRKENSTOCK"
        return "RICHARDS"

    def product_description(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if not self.care_criteria(rd)]

    def product_care(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if self.care_criteria(rd)]

    def raw_description(self, raw_product):
        return [raw_product.get('description', {}).get('value', [])] + [raw_product.get('details', {}).get('value', [])]

    def image_urls(self, images):
        return [img['zoom'] for img in images]

    def skus(self, skus, raw_product, currency):

        colors = raw_product['colorList']
        sizes = []
        price = [raw_product['atualPrice'], currency]
        price = self.product_pricing_common_new('', money_strs=price)

        color_sku = raw_product['skuId']
        color_name = self.color_name(colors, color_sku)

        for size in raw_product.get('sizeList', []):
            skus[color_sku + "_" + size['skuId']] = {"size": size['name'], 'price': price['price'],
                                                     'currency': price['currency'], 'out_of_stock': size['hasStock'],
                                                     'color': color_name}
        return skus

    def color_name(self, colors, color_sku):
        for color in colors:
            if color['skuId'] == color_sku:
                return color['name']

    def create_url(self):
        return 'http://www.richards.com.br/services/get-complete-product.jsp?' + urllib.parse.urlencode(self.params)

    def raw_product(self, response):
        script = response.xpath('//script[contains(., "var globalProduct =")]/text()').extract()
        if script:
            raw_data = re.findall('var globalProduct = (.*);', script[0])[0]
            return json.loads(raw_data)


class RichardsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer+'-crawl'
    parse_spider = RichardsParseSpider()

    def parse(self, response):
        params = {'recsPerPage': 1000}
        for category_id, gender in self.gender_map.items():
            params.update({'N': category_id})
            url_params = urllib.parse.urlencode(params)
            url = self.start_urls[0] + '/services/records.jsp?' + url_params
            yield Request(url=url, meta={'gender': gender}, callback=self.parse_listings)

    def parse_listings(self, response):
        product_links = json.loads(response.text)
        gender = response.meta["gender"]
        for record in product_links['records']:
            request = Request(url=record['url'], callback=self.parse_item)
            request.meta["gender"] = gender
            yield request



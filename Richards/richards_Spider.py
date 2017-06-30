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
    colour_request_params = {'imageProperties': 'thumb,large,zoom', 'productId': 'id', 'selectedSkuId': 'sku'}
    product_request_url = 'http://www.richards.com.br/services/get-complete-product.jsp?'
    page_request_url = start_urls[0]+'/services/records.jsp?'


class RichardsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        raw_product = self.raw_product(response)
        sku_id = raw_product['skuId']
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response, raw_product['url'])
        garment['name'] = raw_product['name']
        garment['brand'] = self.brand_name(garment['name'])
        garment['url'] = raw_product['url']
        garment['description'] = self.product_description(raw_product['details'])
        garment['care'] = self.product_care(raw_product['details'])
        garment['skus'] = {}
        garment['image_urls'] = []

        currency = self.currency(response)
        garment['meta'] = {'requests_queue': self.colour_request(raw_product, currency)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):

        garment = response.meta['garment']
        raw_product = json.loads(response.text)
        currency = response.meta['currency']

        garment['skus'].update(self.skus(raw_product, currency))
        garment['image_urls'] += self.image_urls(raw_product['mediaSets'])

        return self.next_request_or_garment(garment)

    def colour_request(self, raw_product, currency):
        requests = []
        for colour in raw_product['colorList']:
            parameters = self.colour_request_params
            parameters['selectedSkuId'] = colour['skuId']
            parameters['productId'] = raw_product['id']
            create_url = lambda params: self.product_request_url + urllib.parse.urlencode(params)
            colour_url = create_url(parameters)
            requests.append(Request(url=colour_url, meta={'currency': currency}, callback=self.parse_colour))
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

    def skus(self, raw_product, currency):

        colours = raw_product['colorList']
        price = [raw_product['atualPrice'], currency]
        common_sku = self.product_pricing_common_new('', money_strs=price)
        skus ={}
        colour_sku = raw_product['skuId']
        colour_name = self.colour_name(colours, colour_sku)

        for size in raw_product.get('sizeList', []):
            sku = {}
            sku = {"size": size['name'], 'colour': colour_name}
            if not size['hasStock']:
                sku['out_of_stock'] = size['hasStock']

            sku.update(common_sku)
            skus[colour_sku + "_" + size['skuId']] = sku
        return skus

    def colour_name(self, colours, colour_sku):
        for colour in colours:
            if colour['skuId'] == colour_sku:
                return colour['name']

    # def create_url(self, params):
    #     return lambda parameters: self.product_request_url + urllib.parse.urlencode(parameters)

    def raw_product(self, response):
        script = response.xpath('//script[contains(., "var globalProduct =")]/text()').extract()
        if not script:
            return {}

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
            url = self.page_request_url + url_params
            yield Request(url=url, meta={'gender': gender}, callback=self.parse_listings)

    def parse_listings(self, response):
        product_links = json.loads(response.text)
        gender = response.meta["gender"]
        for record in product_links['records']:
            yield Request(url=record['url'], meta={'gender': gender}, callback=self.parse_item)

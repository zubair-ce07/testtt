import json
import re
import w3lib.url

from scrapy import Request
from .base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser


class Mixin:
    retailer = 'richards-br'
    allowed_domains = ['richards.com.br']
    lang = 'pt'
    market = 'BR'
    start_urls = ['http://www.richards.com.br']
    # category id used in post request to retrieve product from a specific gender
    gender_map = {'1005777739': 'men', '43564721': 'women', '3056766704': 'girls', '560931917': 'boys'}
    colour_request_params = {'imageProperties': 'thumb,large,zoom', 'listAllColors': 'true',
                             'productId': 'id', 'selectedSkuId': 'sku'}
    product_request_url = 'http://www.richards.com.br/services/get-complete-product.jsp?'
    page_request_url = start_urls[0]+'/services/records.jsp?'
    brands = ['BIARRITZ', 'BIRKENSTOCK']


class RichardsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        raw_product = self.raw_product(response)
        sku_id = raw_product['skuId']
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response, url=raw_product['url'])
        garment['brand'] = self.brand_name(raw_product['name'])
        garment['name'] = self.product_name(raw_product['name'])
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
        colour = response.meta['colour']

        garment['skus'].update(self.skus(raw_product, currency, colour))
        garment['image_urls'] += self.image_urls(raw_product['mediaSets'])

        return self.next_request_or_garment(garment)

    def product_name(self, name):
         return name.replace(self.brand_name(name), "")

    def colour_request(self, raw_product, currency):
        requests = []
        for colour in raw_product['colorList']:
            colour_url = self.product_request_url
            parameters = self.colour_request_params
            parameters['selectedSkuId'] = colour['skuId']
            parameters['productId'] = raw_product['id']
            for parameter, value in parameters.items():
                colour_url = w3lib.url.add_or_replace_parameter(colour_url, parameter, value)
            requests.append(Request(url=colour_url, meta={'currency': currency, 'colour': colour},
                                    callback=self.parse_colour))
        return requests

    def currency(self, response):
        return CurrencyParser.currency(clean(response.css('meta[property="og:price:currency"]::attr(content)'))[0])

    def brand_name(self, name):
        brand = [brand for brand in self.brands if brand in name]
        return brand[0] if brand else "RICHARDS"

    def product_description(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if not self.care_criteria(rd)]

    def product_care(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if self.care_criteria(rd)]

    def raw_description(self, raw_product):
        description = [raw_product.get('description', {}).get('value', "")]
        description += [raw_product.get('details', {}).get('value', "")]
        return description + [raw_product.get('useMode', {}).get('value', "")]

    def image_urls(self, images):
        return [img['zoom'] for img in images]

    def skus(self, raw_product, currency, colour):
        skus = {}
        price = [raw_product['fromPrice'], raw_product['atualPrice'], currency]
        common_sku = self.product_pricing_common_new('', money_strs=price)
        colour_sku = raw_product['skuId']
        colour_name = colour['name']

        for raw_size in raw_product.get('sizeList', []):
            sku = {}
            sku['colour'] = colour_name
            sku.update(common_sku)
            sku["size"] = self.one_size if raw_size['name'] == 'UN' else raw_size['name']
            if not raw_size['hasStock']:
                sku['out_of_stock'] = True
            skus[colour_sku + "_" + raw_size['skuId']] = sku
        return skus

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
        for category_id, gender in self.gender_map.items():
            url = self.page_request_url
            url = w3lib.url.add_or_replace_parameter(url, 'N', category_id)
            url = w3lib.url.add_or_replace_parameter(url, 'recsPerPage', 1000)
            yield Request(url=url, meta={'gender': gender}, callback=self.parse_listings)

    def parse_listings(self, response):
        product_links = json.loads(response.text)
        gender = response.meta["gender"]
        for record in product_links['records']:
            yield Request(url=record['url'], meta={'gender': gender}, callback=self.parse_item)

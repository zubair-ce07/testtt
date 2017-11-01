import re
import json
from scrapy import Selector, Request
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter,url_query_parameter
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'walmart-us'
    market = 'US'
    allowed_domains = ['walmart.com']
    start_urls = [
        'https://www.walmart.com/cp/Home/4044',
        'https://www.walmart.com/cp/clothing/5438',
        'https://www.walmart.com/cp/beauty/1085666'
    ]
    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-kids')
    ]


class WalmartParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    product_jsn = None

    def parse(self, response):
        prod_regex = '__WML_REDUX_INITIAL_STATE__ = ({.*});\};'
        product_json = self.product_json(response, key='product', regex=prod_regex)
        if not product_json:
            return
        self.product_jsn = product_json
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        if self.homeware(garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        garment['image_urls'] = self.image_urls(product_json)
        garment['skus'] = self.skus(response, product_json)
        if garment['skus']:
            return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.url.split('/')[-1]

    def product_name(self, response):
        return clean(response.css('.ProductTitle div::text'))[0]

    def product_description(self, response):
        product_json = self.product_jsn
        description = list(product_json['idmlMap'].values())
        if not description:
            return
        description = description[0].get('modules', {}).get('ShortDescription', {}).get('product_short_description', {}).get('displayValue', "")
        description = Selector(text=description)
        return clean(description.css('div::text, p::text'))

    def product_care(self, response):
        product_json = self.product_jsn
        care = list(product_json['idmlMap'].values())
        if not care:
            return
        care = care[0].get('modules', {}).get('LongDescription', {}).get('product_long_description', {}).get(
            'displayValue', "")
        care = Selector(text=care)
        return clean(care.css('li::text'))

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text'))

    def product_gender(self, garment):
        soup = garment['category']
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, product_json):
        return [image['assetSizeUrls']['main'] for _, image in product_json['images'].items()]

    def homeware(self, garment):
        return 'Home' in garment['category']

    def product_json(self, response, key, regex):
        product_script = clean(response.css('#cdnHint + script + script::text'))
        if not product_script:
            return
        product_json = re.findall(regex, product_script[0], flags=re.DOTALL)
        return json.loads(product_json[0]).get(key) if product_json else None

    def skus(self,response, product_json):
        skus = {}
        for product_id, product in product_json['products'].items():
            for _, offer in product_json['offers'].items():
                if offer['productId'] == product['productId'] and offer['productAvailability'].get('availabilityStatus', "") == "IN_STOCK" and offer['pricesInfo'].get('priceMap'):
                    skus.update(self.sku(response, product, offer))
        return skus

    def sku(self, response, product, offer):
        sku = {}
        color_size = {}
        for key, value in product.get('variants', {}).items():
            if '_' in key:
                key = key.split('_')[-1]
            value = value.split(key + "-")[1]
            color_size.update({key: value})

        was_price = offer['pricesInfo']['priceMap'].get('WAS', {})
        current_price = offer['pricesInfo']['priceMap']['CURRENT']

        price_string = current_price['currencyUnitSymbol'] + str(current_price['price'])
        pprice_string = was_price.get('currencyUnitSymbol', "") + str(was_price.get('price', ""))

        prices = self.product_pricing_common_new(response, [price_string, pprice_string])

        sku_id = offer['productId']
        sku[sku_id] = color_size
        sku[sku_id].update(prices)

        return sku


class WalmartCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = WalmartParseSpider()
    category_css = '.SideBarMenuModuleItem'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_products'),
    )

    def parse_products(self, response):
        products_json = self.parse_spider.product_json(response, key='preso', regex='__WML_REDUX_INITIAL_STATE__ = ({.*});')
        if not products_json:
            return
        for product in products_json['items']:
            product_url = response.urljoin(product['productPageUrl'])
            yield Request(product_url, callback=self.parse_item)

        next_page = products_json['pagination'].get('next', {}).get('url')
        if not next_page:
            return
        page_no = url_query_parameter("?"+next_page, 'page', 1)
        pagination_url = add_or_replace_parameter(response.url, 'page', page_no)
        return Request(pagination_url, callback=self.parse_products)

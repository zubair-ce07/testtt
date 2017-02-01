import json
import re
from scrapy.http.request import Request
from skuscraper.spiders.base import CurrencyParser, BaseParseSpider, BaseCrawlSpider


class Mixin:
    allowed_domains = ["stelladot.com"]
    categories_url = 'https://www.stelladot.com/api/mage/b2c_en_us/apiv1/catalog/categories'
    product_info_url = 'https://www.stelladot.com/api/mage/b2c_en_us/apiv1/product/id/id/{}'
    start_urls = [categories_url]
    retailer = 'stelladot-us'
    market = 'US'
    lang = 'en'


class StelladotUsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product = json.loads(response.text)
        product_id = self.product_id(product)
        garment = self.new_unique_garment(product_id)
        if product['is_salable'] is not '1':
            return
        self.boilerplate(garment, response)
        garment['name'] = product['name']
        garment['brand'] = 'Stella & Dot, Covet by Stella & Dot'
        garment['image_urls'] = self.product_images(product)
        price = float(product['price'])
        if product.get('special_price'):
            special_price = float(product['special_price'])
            garment['price'] = CurrencyParser.float_conversion(special_price)
            garment['previous_prices'] = [CurrencyParser.float_conversion(price)]
        else:
            garment['price'] = CurrencyParser.float_conversion(price)
        garment['currency'] = 'USD'
        garment['gender'] = self.product_gender(product)
        garment['description'] = self.product_description(product)
        garment['category'] = self.product_category(product,response)
        garment['out_of_stock'] = product['is_in_stock'] is not '1'
        garment['url'] = product['url']
        return garment

    def product_category(self, product, response):
        category_id = response.request.meta.get('category_id')
        category = product['categories'][category_id] \
            if product['categories'] else None
        return [category]

    def product_gender(self, product):
        return 'girls' if 'girl' in product['url'] else 'women'

    def product_images(self, product):
        return [ image['url'] for image in product['media_gallery']['images'] ]

    def product_description(self, product):
        description = product['description']
        return re.sub('<[^>]+>','',description)

    def product_id(self, product):
        return product['entity_id']

    def product_brand(self, product):
        return 'Stella & Dot, Covet by Stella & Dot'

    def product_name(self, product):
        return product['name']

class StellaDotUsCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = StelladotUsParseSpider()
    def parse(self, response):
        categories = json.loads(response.text)
        for c_id in categories:
            category = categories[c_id]
            products = category['products']
            yield from [self.product_request(p,c_id) for p in products if products]

    def product_request(self, product_id, category_id):
        url = self.product_info_url.format(product_id)
        meta = {'category_id': category_id}
        return Request(url=url, meta=meta, callback=self.parse_item)

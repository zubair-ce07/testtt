import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean
from ..parsers.currencyparser import CurrencyParser


class Mixin:
    retailer = 'thefragranceshop'


class MixinUK(Mixin):
    market = 'UK'
    retailer = Mixin.retailer + '-uk'
    allowed_domains = ['thefragranceshop.co.uk']
    start_urls = [
        'http://thefragranceshop.co.uk/'
    ]


class TheFragranceShopSpider(BaseParseSpider):

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = raw_product.get('id')

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment['gender'] = self.product_gender(raw_product.get('attributes'))
        garment['category'] = self.product_category(raw_product.get('classification'))
        garment['brand'] = raw_product.get('brand')
        garment['name'] = raw_product.get('name')
        garment['description'] = clean(self.text_from_html(raw_product.get('description')))
        garment['care'] = ''
        garment['image_urls'] = self.product_image_urls(raw_product.get('images'))
        garment['skus'] = self.product_skus(response, raw_product)
        return garment

    def raw_product(self, response):
        selector = 'script[defer]:not([src])'
        raw_data = response.css(selector).re_first(r'({.*})')
        return json.loads(raw_data)

    def product_gender(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('display') == 'Gender':
                return self.gender_lookup(raw_attr.get('value'))

    def product_category(self, raw_data):
        return [raw_data.get('mainCategoryName', '')]

    def product_image_urls(self, raw_data):
        return [img.get('url') for img in raw_data]

    def product_skus(self, response, raw_data):
        product_variants = raw_data.get('variantProducts')
        size_value = re.findall(r'(\d+).', raw_data.get("uomValue"))[0]
        size_unit = raw_data.get("uom")
        size = f'{size_value}{size_unit}' if int(size_value) else 'one'

        common_sku = {
            'price': self.product_price(raw_data.get('price')),
            'previous_prices': [self.product_price(raw_data.get('listPrice'))],
            'currency': self.product_currency(response),
            'size': size
        }

        if isinstance(product_variants, list) and product_variants:
            skus = {}
            for varient in product_variants:
                sku = common_sku.copy()
                color = self.product_color(varient)
                if color:
                    sku['color'] = color

                sku_size = self.sku_size(varient.get('variantAttributes'))
                sku['size'] = sku_size if sku_size else size
                sku['price'] = self.product_price(varient.get('listPrice'))
                sku['previous_prices'] = [self.product_price(varient.get('sellPrice'))]
                skus[f'{size}_{color}'] = sku

            return skus

        return {size: common_sku}

    def product_price(self, raw_price):
        formatted_price = raw_price.get('formatted').get('withTax')
        return CurrencyParser.prices(formatted_price)[0]

    def product_currency(self, response):
        raw_data = response.css('script[type="application/ld+json"]::text').get()
        raw_data = json.loads(clean(raw_data))
        return raw_data['offers']['priceCurrency']

    def product_color(self, raw_data):
        raw_attributes = raw_data.get('variantAttributes')
        for raw_attr in raw_attributes:
            if raw_attr.get('fieldName') == 'Colour':
                raw_color = raw_attr.get('fieldLabel')
                color = self.detect_colour(raw_color, multiple=True) or raw_color
                if not color:
                    color = self.detect_colour(raw_data.get('slug'), True)
                return color

    def sku_size(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('fieldCode') == 'global.size.volume':
                return raw_attr.get('fieldValue')


class TheFragranceShopCrawler(BaseCrawlSpider):
    allow = r'/l'
    listings_css = [
        '.megaNav__list__item',
        '.pagination li:last-child'
    ]
    products_css = ['.imagePanel']

    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )


class TheFragranceShopUKSpider(MixinUK, TheFragranceShopSpider):
    name = MixinUK.retailer + '-parse'


class TheFragranceShopUKCrawler(MixinUK, TheFragranceShopCrawler):
    name = MixinUK.retailer + '-crawl'
    parse_spider = TheFragranceShopUKSpider()

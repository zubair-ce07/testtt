import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean


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
        product_raw_information = self.product_raw_information(response)
        pid = product_raw_information.get('id')

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        currency = self.product_currency(response)
        self.boilerplate_minimal(garment, response)
        garment['gender'] = self.product_gender(product_raw_information.get('attributes'))
        garment['category'] = self.product_category(product_raw_information.get('classification'))
        garment['brand'] = product_raw_information.get('brand')
        garment['name'] = product_raw_information.get('name')
        garment['description'] = [self.clean(product_raw_information.get('description'))]
        garment['care'] = ''
        garment['image_urls'] = self.product_image_urls(product_raw_information.get('images'))
        garment['skus'] = self.product_skus(product_raw_information, currency)
        garment['price'] = self.product_price(product_raw_information.get('price'))
        garment['currency'] = currency
        return garment

    def product_raw_information(self, response):
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

    def product_skus(self, raw_data, currency):
        product_variants = raw_data.get('variantProducts')
        size_value = re.findall(r'(\d+).', raw_data.get("uomValue"))[0]
        size_unit = raw_data.get("uom")
        size = f'{size_value}{size_unit}' if int(size_value) else 'one'

        common_sku = {
            'price': self.product_price(raw_data.get('price')),
            'previous_prices': [self.product_price(raw_data.get('listPrice'))],
            'size': size,
            'currency': currency
        }

        if isinstance(product_variants, list) and product_variants:
            skus = {}
            for varient in product_variants:
                sku = common_sku.copy()
                color = self.product_color(varient.get('variantAttributes'))
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
        REGEX_PRICE_CLEANER = r'\W'
        formatted_price = raw_price.get('formatted').get('withTax')
        clean_price = re.sub(REGEX_PRICE_CLEANER, '', str(formatted_price))
        return int(clean_price)

    def product_currency(self, response):
        raw_data = response.css('script[type="application/ld+json"]::text').get()
        raw_data = json.loads(self.clean(raw_data))
        return raw_data['offers']['priceCurrency']

    def product_color(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('fieldName') == 'Colour':
                raw_color = raw_attr.get('fieldLabel')
                return raw_color.split(' - ')[1]

    def sku_size(self, raw_data):
        for raw_attr in raw_data:
            if raw_attr.get('fieldCode') == 'global.size.volume':
                return raw_attr.get('fieldValue')

    def clean(self, raw_data):
        REGEX_TAG_CLEANER = r'<.*?>'
        return re.sub(REGEX_TAG_CLEANER, '', clean(raw_data))


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

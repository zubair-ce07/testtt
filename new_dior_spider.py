import json
import re

from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, Gender, clean


class Mixin:
    retailer = 'dior'
    allowed_domains = ['www.dior.com', 'api.dior.com']
    default_brand = 'Dior'
    one_sizes = ['U', 'TU']
    deny_care = ['Delivery and returns']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    start_urls = ['https://www.dior.com/en_gb']
    market = 'UK'


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    start_urls = ['http://www.dior.com/it_it/']
    market = 'IT'


class ParseSpider(BaseParseSpider):
    def parse(self, response):
        raw_product = self.raw_product(response)

        pid = self.product_id(raw_product)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(raw_product)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['skus'] = skus = self.skus(raw_product)

        if not skus:
            garment['out_of_stock'] = True

        return self.next_request_or_garment(garment)

    def product_id(self, raw_product):
        raw_details = raw_product['dataLayer']['ecommerce']['detail']['products']
        return raw_details['id']

    def merch_info(self, raw_product):
        raw_details = raw_product['dataLayer']['ecommerce']['detail']['products']
        return ['Notify Me'] if not raw_details['price'] else []

    def product_gender(self, raw_product):
        soup = raw_product['dataLayer']['subUniverse']
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_name(self, raw_product):
        name = raw_product['dataLayer']['ecommerce']['detail']['products']['name']
        brand_r = self.product_brand(raw_product)
        return clean(re.sub(re.escape(brand_r), '', name, flags=re.I))

    def product_category(self, raw_product):
        raw_category = raw_product['dataLayer']['ecommerce']['detail']['products']
        return raw_category['category'].split('/')

    def image_urls(self, response):
        return clean(response.css('.product-image-grid img::attr(src)'))

    def product_brand(self, raw_product):
        brand = raw_product['dataLayer']['ecommerce']['detail']['products'].get('brand')
        return brand or super().product_brand(raw_product)

    def raw_description(self, raw_product):
        raw_desc = raw_product['cmsContent']['elements'][4]['sections']
        return sum([clean(Selector(text=desc['content']).css('::text')) for desc in raw_desc], [])

    def raw_product(self, response):
        css = 'script:contains("initialState")::text'
        json_product = clean(response.css(css))[0]
        json_product = re.findall('({"universe":.+),"ENGRAVING":\[\]', json_product)[0]
        return json.loads(json_product)

    def skus(self, raw_product):
        skus = {}
        currency_str = raw_product['dataLayer']['ecommerce']['currencyCode']
        raw_details = raw_product['dataLayer']['ecommerce']['detail']['products']
        common_price = {'value': raw_details['price']}
        stock_msg = raw_details['dimension25']

        one_size = [{'title': self.one_size, 'price': common_price, 'status': stock_msg}]
        default_colour = [
            {
                'title': raw_details['variant'],
                'price': common_price,
                'status': stock_msg
            }
        ]

        variants = raw_product['cmsContent']['elements'][3]
        raw_sizes = variants['variations'] if variants.get('variationsType') == 'SIZE' else one_size
        for raw_size in raw_sizes:
            raw_colours = variants['variations'] if variants.get('variationsType') == 'SWATCH' else default_colour

            for raw_colour in raw_colours:

                if (raw_size.get('status') or raw_colour.get('status')).lower() == 'outofstock':
                    continue

                money_strs = [
                    str(raw_size.get('price', {}).get('value') or ''),
                    str(raw_colour.get('price', {}).get('value') or ''),
                ]

                if not clean(money_strs):
                    continue

                money_strs += [currency_str]
                sku = self.product_pricing_common(None, money_strs=money_strs)

                sku['size'] = size = raw_size['title']
                sku['colour'] = colour = raw_colour['title']

                skus[f'{colour}_{size}'] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = '.header-navigation'
    products_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class UKParseSpider(MixinUK, ParseSpider):
    name = MixinUK.retailer + '-parse'


class UKCrawlSpider(MixinUK, CrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = UKParseSpider()


class ITParseSpider(MixinIT, ParseSpider):
    name = MixinIT.retailer + '-parse'


class ITCrawlSpider(MixinIT, CrawlSpider):
    name = MixinIT.retailer + '-crawl'
    parse_spider = ITParseSpider()

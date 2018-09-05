import json

from scrapy.http import Response
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'lagarconne'
    allowed_domains = ['lagarconne.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    lang = 'en'

    start_urls_with_meta = [
        ('https://lagarconne.com/collections/bags', {'gender': 'women'}),
        ('https://lagarconne.com/collections/shoes', {'gender': 'women'}),
        ('https://lagarconne.com/collections/jewelry', {'gender': 'women'}),
        ('https://lagarconne.com/collections/clothing', {'gender': 'women'}),
        ('https://lagarconne.com/collections/clergerie', {'gender': 'women'}),
        ('https://lagarconne.com/collections/accessories', {'gender': 'women'}),
        ('https://lagarconne.com/collections/new-arrivals', {'gender': 'women'}),
        ('https://lagarconne.com/collections/back-in-stock', {'gender': 'women'}),
        ('https://lagarconne.com/collections/la-garconne-moderne', {'gender': 'women'}),

        ('https://lagarconne.com/collections/beauty', {'industry': 'beauty'}),
        ('https://lagarconne.com/collections/interiors', {'industry': 'homeware'})
    ]


class LaGarconneParseSpider(BaseParseSpider):
    price_css = '[itemprop="price"] .money::text'
    raw_description_css = '.lg-desc-product p::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        if self.out_of_stock(response, response):
            return self.out_of_stock_garment(response, pid)

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(raw_product)
        garment['care'] = self.product_care(response)
        garment['description'] = self.product_description(response)
        garment['category'] = self.product_category(garment)
        garment['brand'] = self.product_brand(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(response, raw_product)

        return garment

    def raw_product(self, response):
        css = 'script:contains("productJSON")::text'
        return json.loads(response.css(css).re('{.*}')[0])

    def out_of_stock(self, hxs, response):
        oos_css = '.lg-product-details:contains("SOLD OUT"), .lg-product-details:contains("Call to Order")'
        return response.css(oos_css)

    def product_id(self, response):
        return clean(response.css('.lg-desc-product #sku::text'))[0]

    def product_category(self, garment):
        if isinstance(garment, Response):
            return
        if garment['trail']:
            return clean([x[0].upper() for x in garment['trail'] if x[0]])

    def product_name(self, raw_product):
        return raw_product['title']

    def product_brand(self, raw_product):
        return raw_product['vendor']

    def image_urls(self, raw_product):
        return raw_product['images']

    def skus(self, response, raw_product):
        skus = {}
        previous_price = raw_product['compare_at_price']
        common_sku = self.product_pricing_common(response, money_strs=[previous_price])
        common_sku['color'] = self.detect_colour(raw_product['description'])
        for raw_sku in raw_product['variants']:
            sku = common_sku.copy()
            if not raw_sku['available']:
                sku['out_of_stock'] = True

            sku['size'] = raw_sku['option1']
            skus[raw_sku['sku']] = sku

        return skus


class LaGarconneCrawlSpider(BaseCrawlSpider):
    listings_css = '.pagination'
    products_css = '.lg-product-list-item'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class LaGarconneParseSpiderUS(LaGarconneParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class LaGarconneCrawlSpiderUS(LaGarconneCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = LaGarconneParseSpiderUS()

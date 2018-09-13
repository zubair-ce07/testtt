import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'lagarconne'
    allowed_domains = ['lagarconne.com']

    MERCH_INFO = [
        'La Garçonne Exclusive'
    ]


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'

    start_urls = ['https://lagarconne.com']
    one_sizes = ['one size']
    gender = Gender.WOMEN.value


class LaGarconneParseSpider(BaseParseSpider):
    price_css = '[itemprop="price"] .money::text, .lg-price-cut ::text'
    raw_description_css = '.lg-desc-product p::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate(garment, response)
        raw_product = self.raw_product(response)
        garment['care'] = self.product_care(response)
        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['description'] = self.product_description(response)
        garment['merch_info'] = self.merch_info(garment)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
            garment['gender'] = None

        if self.out_of_stock(response, response):
            garment['out_of_stock'] = True
            garment.update(self.product_pricing_common(response))
            return garment

        garment['skus'] = self.skus(response, raw_product)
        return garment

    def raw_product(self, response):
        css = 'script:contains("productJSON")::text'
        return json.loads(response.css(css).re('{.*}')[0])

    def product_id(self, response):
        return clean(response.css('.product_id::text'))[0]

    def out_of_stock(self, hxs, response):
        css = '.lg-product-details:contains("SOLD OUT"), .lg-product-details:contains("Call to Order")'
        return response.css(css)

    def product_category(self, raw_product):
        return [raw_product['type']]

    def product_name(self, raw_product):
        return raw_product['title']

    def product_brand(self, raw_product):
        return raw_product['vendor']

    def image_urls(self, raw_product):
        return raw_product['images']

    def skus(self, response, raw_product):
        skus = {}
        common_sku = self.product_pricing_common(response)
        for raw_sku in raw_product['variants']:
            sku = common_sku.copy()

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            size = raw_sku['option1']
            sku['size'] = self.one_size if size.lower() in self.one_sizes else size

            if raw_sku['option2']:
                sku['colour'] = raw_sku['option2']

            skus[raw_sku['sku']] = sku

        return skus

    def merch_info(self, garment):
        info = garment['description'] + garment['care']
        return [m for m in self.MERCH_INFO for i in info if m in i]

    def is_homeware(self, response):
        return 'interiors' in response.url


class LaGarconneCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.lg-filter-list-desktop',
        '.pagination'
    ]

    products_css = '.lg-product-list-item-title'

    deny = '/pages'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny), callback='parse_item')
    )


class LaGarconneParseSpiderUS(LaGarconneParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class LaGarconneCrawlSpiderUS(LaGarconneCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = LaGarconneParseSpiderUS()

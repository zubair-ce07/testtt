import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'fila-uk'
    market = 'UK'
    default_brand = 'Fila'

    allowed_domains = ['fila.co.uk']
    start_urls = ['https://www.fila.co.uk']


class FilaParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    raw_description_css = '.product_desc_div ::text'
    price_css = '[itemprop="priceCurrency"]::attr(content)'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        css = '.product-info-main .price-final_price::attr(data-product-id)'
        return clean(response.css(css))[0]

    def product_name(self, response):
        return clean(response.css('.items .product ::text'))[0]

    def image_urls(self, response):
        return clean(response.css('.gallery_zoom_full_view img::attr(src)'))

    def product_gender(self, response):
        trail = soupify([f'{cat} {url}' for cat, url in response.meta.get('trail', [])])

        return self.gender_lookup(trail) or Gender.ADULTS.value

    def product_category(self, response):
        return clean([category for category, _ in response.meta.get('trail') or []])

    def skus(self, response):
        skus = {}

        raw_stock = self.available_raw_stock(response)
        raw_products = self.magento_product_data(response, 'spConfig', 'spConfig":\s({.*})')

        for sku_id, raw_sku in self.magento_product_map(raw_products).items():
            raw_prices = [price.get('amount') for price in raw_sku[0]['prices'].values() if price]

            sku = self.product_pricing_common(response, money_strs=raw_prices)
            sku['size'] = clean(raw_sku[0]['label'])

            if not raw_stock.get(raw_sku[0]['id'], {}).get('is_in_stock'):
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus


    def available_raw_stock(self, response):
        css = 'script:contains("amstockstatusRenderer")::text'
        stock_info = json.loads(response.css(css).re_first('.*?(\{.*\})'))

        return stock_info


class FilaCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = FilaParseSpider()

    listings_css = ['.subnav-column:not(.heading)']
    products_css = ['.product-item-name']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify


class Mixin:
    market = 'ES'
    retailer = 'decimas-es'
    default_brand = 'Decimas'

    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es/']

    restrict_brand_map = True
    spider_brand_map = {
        'nike': ['nike'],
        'adidas': ['adidas'],
        'asics': ['asics'],
        'reebok': ['reebok'],
        'puma': ['puma'],
        'head': ['head'],
        '47': ['47 brand', '47'],
        'tenth': ['tenth'],
        'new balance': ['new balance'],
        'ipanema': ['ipanema'],
        'polinesia': ['polinesia'],
        'PLNS': ['plns'],
        'rider': ['rider'],
        'arena': ['arena'],
        'joma': ['joma']
    }


class DecimesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    raw_description_css = '[itemprop="description"] ::text'
    sku_re = r'"jsonConfig"\s*:\s*(.*),'

    def parse(self, response):
        product_id = self.product_id(response)  # defined below

        # returns a new item, with lang, gender, outlet, skuid and also checks for duplication
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        # extracts care, description, brand, category, requires a method product_name to extract name
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        return response.css('script:contains(productID)').re_first('productID":\s*"(.*?)"')

    def raw_name(self, response):
        return clean(response.css('.name h1 ::text'))[0]

    def product_name(self, response):
        return self.remove_brand_from_text(self.product_brand(response), self.raw_name(response))

    def brand_soup(self, response):
        return self.raw_name(response)

    def product_category(self, response):
        return clean(response.css('.breadcrumbs .item:not(.home):not(.product) ::text'))

    def product_gender(self, response):
        trail = [t for t, _ in response.meta.get('trail') or []] or [response.url]
        soup = soupify(self.product_description(response) + trail)
        name_l = self.raw_name(response)
        return self.gender_lookup(name_l) or self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        product_data = self.magento_product_data(response, config='ezSwatchRenderer', regex=self.sku_re)
        return [re.sub(r'_\d+', '', img['full']) for images in product_data['images'].values() for img in images]

    def skus(self, response):
        product_data = self.magento_product_data(response, config='jsonConfig', regex=self.sku_re)

        skus = {}
        for sku_id, raw_sku in self.magento_product_map(product_data).items():
            money_strs = [
                product_data['optionPrices'][sku_id]['finalPrice']['amount'],
                product_data['optionPrices'][sku_id]['oldPrice']['amount'],
                product_data['currencyFormat']
            ]

            sku = self.product_pricing_common(None, money_strs=money_strs)
            sku['size'] = clean(raw_sku[0]['label'])
            sku['colour'] = re.sub('(\d+\s)', '', clean(raw_sku[1]['label']))

            skus[sku_id] = sku

        return skus


class DecimesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DecimesParseSpider()

    listings_css = ['.mobile-menu-body', '.pages']
    products_css = ['.product-item-link']

    deny = ['blog', 'campana']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

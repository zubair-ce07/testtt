import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'moosejaw-us'
    lang = 'en'
    market = 'US'
    allowed_domains = ['moosejaw.com']
    start_urls = [
        'https://www.moosejaw.com/moosejaw/shop/navigation__Jackets_____',
        'https://www.moosejaw.com/moosejaw/shop/navigation__Clothing_____',
        'https://www.moosejaw.com/moosejaw/shop/navigation__Footwear_____',
        'https://www.moosejaw.com/moosejaw/shop/search_Jackets-Sale____',
        'https://www.moosejaw.com/moosejaw/shop/search_Clothing-Sale____',
        'https://www.moosejaw.com/moosejaw/shop/search_Footwear-Sale____,',
    ]


class MooseJawParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    image_re = re.compile('\?(.*)')

    gender_map = [
        ('Baby, Kids', 'unisex-children'),
        ('Mens', 'men'),
        ('Womens', 'women'),
        ('Boys, Kids', 'boys'),
        ('Boys', 'boys'),
        ('Girls', 'girls'),
        ('Kids, Girls', 'girls'),
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = self.skus(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)

        return garment

    def skus(self, response):
        skus = {}
        raw_skus_s = response.css('[itemprop="offers"]')

        original_price = self.original_price(response)

        for sku_s in raw_skus_s:
            sku = {
                'size': self.sku_size(sku_s),
                'colour': self.sku_colour(sku_s)
            }

            sku.update(
                self.sku_pricing(response, sku_s, original_price))

            skus[self.sku_key(sku_s)] = sku

        return skus

    def colour_variant(self, raw_sku_s):
        css = '[itemprop="color"]::attr(content)'
        raw_colour_variant = clean(raw_sku_s.css(css))[0]

        return raw_colour_variant.split(', ')

    def sku_size(self, raw_sku_s):
        raw_colour_variant = self.colour_variant(raw_sku_s)

        return raw_colour_variant[1]

    def sku_colour(self, raw_sku_s):
        raw_colour_variant = self.colour_variant(raw_sku_s)

        return raw_colour_variant[0]

    def original_price(self, response):
        css = '#adwordsTotalValue::attr(value)'

        return clean(response.css(css))

    def sku_pricing(self, response, raw_sku_s, original_price):
        price_css = '[itemprop="price"]::attr(content)'
        currency_css = '[itemprop="priceCurrency"]::attr(content)'

        pricing = clean(raw_sku_s.css(price_css))
        pricing += clean(raw_sku_s.css(currency_css))
        pricing += original_price

        return self.product_pricing_common_new(response, money_strs=pricing)

    def product_gender(self, response):
        raw_gender = self.raw_gender(response) + self.raw_name(response)

        for gender_key, gender in self.gender_map:
            if gender_key in raw_gender:
                return gender

        return 'unisex-adults'

    def raw_gender(self, response):
        xpath = '//*[contains(text(), "Gender")]/following-sibling::td/text()'

        return clean(response.xpath(xpath))[0]

    def image_urls(self, response):
        css = '.alt-color-img-box img::attr(src)'

        return [self.image_re.sub('?$product1000$', img)
                for img in clean(response.css(css))]

    def product_id(self, response):
        css = '#adwordsProdId::attr(value)'

        return clean(response.css(css))[0]

    def raw_name(self, response):
        css = '[itemprop="name"]::text'

        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '#breadcrumb [itemprop="title"]::text'

        return clean(response.css(css))[1:]

    def product_brand(self, response):
        css = '[itemprop="brand"]::attr(content)'

        return clean(response.css(css))[0]

    def product_name(self, response):
        raw_name = self.raw_name(response)
        brand = self.product_brand(response)

        return clean(raw_name.replace(brand, ''))

    def product_description(self, response):
        css = '[itemprop="description"] p::text'
        return clean(response.css(css))

    def product_care(self, response):
        css = '.pdp-specifications td::text'
        raw_care = clean(response.css(css))

        return [rc for rc in raw_care
                if self.care_criteria_simplified(rc)]

    def sku_key(self, raw_sku_s):
        css = '[itemprop="sku"]::attr(content)'

        return clean(raw_sku_s.css(css))[0]


class MooseJawCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseJawParseSpider()

    pagination_css = '[title="Next Page"]'

    product_css = '.prod-item .pdpLink'

    rules = (
        Rule(LinkExtractor(restrict_css=pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'moosejaw-us'
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
    previous_prices_re = re.compile(':(\d+):[$\d.]+:(\$[.\d]+):')

    price_css = '[itemprop="price"]::attr(content),' \
                '[itemprop="priceCurrency"]::attr(content)'

    gender_map = [
        ('womens', 'women'),
        ('mens', 'men'),
        ('boys', 'boys'),
        ('girls', 'girls'),
        ('baby', 'unisex-children'),
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

        sku_variants_css = '[itemprop="color"]::attr(content)'

        skus_previous_price = self.skus_previous_price(response)

        for sku_s in raw_skus_s:
            sku = {}
            sku_key = self.sku_key(sku_s)

            previous_price = [skus_previous_price[sku_key]]

            colour_variant = clean(sku_s.css(sku_variants_css))[0]
            sku['colour'], sku['size'] = colour_variant.split(', ')

            sku.update(self.product_pricing_common_new(sku_s, money_strs=previous_price))

            skus[sku_key] = sku

        return skus

    def skus_previous_price(self, response):
        xpath = '//script[contains(text(), "itemPriceSku")]/text()'
        price_script_text = clean(response.xpath(xpath))[0]

        return dict(self.previous_prices_re.findall(price_script_text))

    def product_gender(self, response):
        xpath = '//*[contains(text(), "Gender")]/following-sibling::td/text()'

        raw_gender = clean(response.xpath(xpath)) + [self.raw_name(response)]
        raw_gender = ' '.join(raw_gender).lower()

        for gender_key, gender in self.gender_map:
            if gender_key in raw_gender:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        css = '.alt-color-img-box img::attr(src)'

        return [self.image_re.sub('?$product1000$', img) for img in clean(response.css(css))]

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

    def raw_description(self, response):
        css = '.pdp-specifications tr'
        return [' '.join(clean(row_s.css(' ::text'))) for row_s in response.css(css)]

    def product_description(self, response):
        css = '[itemprop="description"] p::text'
        description = clean(response.css(css))
        description += [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

        return description

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def sku_key(self, raw_sku_s):
        css = '[itemprop="sku"]::attr(content)'
        return clean(raw_sku_s.css(css))[0]


class MooseJawCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseJawParseSpider()

    listing_css = '[title="Next Page"]'

    product_css = '.prod-item .pdpLink'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


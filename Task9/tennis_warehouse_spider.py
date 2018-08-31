from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, Gender, soupify


class MixinUS:
    retailer = 'tennis-warehouse-us'
    market = 'US'
    default_brand = 'tennis_warehouse'
    allowed_domains = ['tennis-warehouse.com']
    start_urls = ['https://www.tennis-warehouse.com/equipment.html']


class ParseSpider(BaseParseSpider):
    raw_description_css = '.desc_column *::text'
    price_css = '.product_pricing *::text'
    brand_css = 'meta[itemprop="brand"]::attr(content)'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["gender"] = self.product_gender(garment)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)

        if not garment["skus"]:
            garment["out_of_stock"] = True

        return garment

    def product_id(self, response):
        return response.css('.wishlist_poplink::attr(data-code)').extract_first()

    def product_name(self, response):
        return response.css('.product_header h1::text').extract_first()

    def image_urls(self, response):
        return response.css('.multiview img::attr(src)').re('(.+)&')

    def product_category(self, response):
        return [trail[0] for trail in response.meta["trail"] if trail[0] != '']

    def product_gender(self, garment):
        soup = [garment["name"], garment["url"]] + garment["category"]
        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def skus(self, response):
        raw_skus = response.css('.styled_subproduct_list tr')

        skus = {}
        for raw_sku in raw_skus:
            name = raw_sku .css('.name strong::text').extract_first().split()
            sku = self.product_pricing_common(response)

            sku["colour"] = name[-2]
            sku["size"] = name[-1]

            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku

        return skus


class CrawlSpider(BaseCrawlSpider, MixinUS):
    listings_xpath = [
        '//div[text()="Apparel"]/following-sibling::ul[1]',
        '//a[text()="Junior Shoes"]',
        '//a[text()="Tennis Bags"]'
    ]

    listings_css = [
        '.lnav_col_header',
        '.appwrap',
        'div[class*="_featured_brands"]',
        'div[class*="_brandlist"]'
    ]

    product_css = ['.cat_border_table .name', '.cat_list .name']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )


class TennisWarehouseUSParseSpider(ParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class TennisWarehouseUSCrawlSpider(CrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = TennisWarehouseUSParseSpider()

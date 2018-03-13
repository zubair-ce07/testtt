import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean


class MixinUS:
    retailer = "modells-us"
    market = "US"
    allowed_domains = ["modells.com"]
    start_urls = ["https://www.modells.com/"]
    spider_gender_map = [
        ('youth', 'unisex-kids'),
    ]
    unwanted_categories = ['fitness', 'sporting goods', 'chair', 'glasses', 'hockey stick', 'ball', 'stick']

    merch_info_map = [
        ('limited edition', 'Limited Edition'),
        ('online exclusive', 'Online Exclusive')
    ]



class ModellsParseSpider(BaseParseSpider):
    price_css = '.pdp__pricing .price-standard::text, .pdp__pricing .price-sales::text'
    raw_description_css = '.description-content ::text'

    def parse(self, response):
        sku_id = self.product_id(response)

        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        if self.is_unwanted(response):
            return

        self.boilerplate_normal(garment, response)
        garment["gender"] = self.product_gender(response)
        garment['merch_info'] = self.merch_info(response)
        garment["skus"] = {}
        garment["image_urls"] = []

        if not clean(response.css(self.price_css)):
            garment['out_of_stock'] = True
            return garment

        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        if not garment['meta']['requests_queue']:
            garment['skus'] = self.skus(response)
            garment['image_urls'] = self.image_urls(response)
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def is_unwanted(self, response):
        soup = ' '.join(self.product_category(response) + [self.product_name(response)]).lower()
        return any(x in soup for x in self.unwanted_categories)

    def product_id(self, response):
        return clean(response.css('.product-number .pdp__id::text'))[0]

    def product_name(self, response):
        name = clean(response.css('.product-name::text'))[0]
        return clean(re.sub(self.product_brand(response), '', name, re.I))

    def product_brand(self, response):
        brand = clean(response.css('.pdp__brand-name::text'))
        return clean(brand or response.css('.pdp__brand-img::attr(alt)') or ['Modells'])[0]

    def product_category(self, response):
        categories = clean(response.css('.breadcrumb-list a::text'))
        return [x for x in categories if 'Search Term' not in x]

    def product_gender(self, response):
        soup = ' '.join(self.product_category(response) + [response.url]).lower()
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        images_s = response.css('.pdp__gallery__main .pdp__gallery-item')
        images = clean(images_s.css('::attr(src)')) + clean(images_s.css('::attr(data-lazy)'))
        return [img for img in images if img != 'null']

    def skus(self, response):
        skus = {}
        colour = clean(response.css('.product-variations span.p--2::text').re('\[(.*)\]'))
        colour = colour[0] if colour else ""
        common = self.product_pricing_common_new(response)
        common['colour'] = colour

        css = '.pdp__options-combo option:not([class="emptytext"])::text'
        for size in clean(response.css(css)) or ['1 Size']:
            sku = common.copy()
            sku['size'] = self.one_size if size == '1 Size' else size
            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def colour_requests(self, response):
        urls = clean(response.css('.swatches.color a::attr(href)'))
        return [Request(u, callback=self.parse_colour) for u in urls]

    def merch_info(self, response):
        soup = ' '.join(self.product_description(response)).lower()
        for token, m_info in self.merch_info_map:
            if token in soup:
                return [m_info]
        return []


class ModellsCrawlSpider(BaseCrawlSpider):
    listings_css = ['#navigation',
                    '.pagination__list']

    products_css = [
        '.product-tile__link'
    ]

    deny_r = [
        'hockey-goals-and-nets',
        'games-lawn-games',
        'games-sports-and-arcade',
        'sports-medicine-tape-and-wrap',
        'exercise-equipment-strength-training-weights',
        'lacrosse-sticks',
        'games-darts-and-billiards',
        'baseball-bats',
        'swim-and-water-sports-pool-games',
        'hockey-mini-hockey-and-soft-sets',
        'baseball-catchers-gear',
        'water-bottles-water-bottles'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner), callback='parse_item')
    )


class USParseSpider(MixinUS, ModellsParseSpider):
    name = MixinUS.retailer + '-parse'


class USCrawlSpider(MixinUS, ModellsCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = USParseSpider()

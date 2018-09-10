from itertools import product

from scrapy.link import Link
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'lindex'
    allowed_domains = ['lindex.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['https://www.lindex.com/uk/']


class LindexParseSpider(BaseParseSpider):
    price_css = '.info .amount::text'
    care_css = '.more_info ::text'
    description_css = '.description ::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)
        return garment

    def product_id(self, response):
        return clean(response.css('.product_id ::text'))[1]

    def product_name(self, response):
        return clean(response.css('.name::text'))[0]

    def product_brand(self, response):
        return clean(response.css('#ProductPage ::attr(data-product-brand)'))[0]

    def product_category(self, response):
        return clean(response.css('#breadcrumbs ::text').re('[a-z A-Z]+'))

    def product_gender(self, garment):
        soup = ' '.join(garment['category']).lower()
        return self.gender_lookup(soup)

    def skus(self, response):
        skus = {}
        colour = response.css('#ProductPage .colors li')
        sizes = response.css('.sizeSelector option:not([selected])')
        common_skus = self.product_pricing_common(response)

        for colour_s, size_s in product(colour, sizes):
            sku = common_skus.copy()

            size = clean(size_s.css('::text'))[0]
            colour_id = clean(colour_s.css('::attr(data-colorid)'))[0]
            size_id = clean(size_s.css('::attr(value)'))[0].split(';')[0]
            split_on_t = '('

            if 'out of stock' in size:
                sku['out_of_stock'] = True
                split_on_t = '-'

            sku['colour'] = clean(colour_s.css('::attr(title)'))[0]
            sku['size'] = size.split(split_on_t)[0]

            skus[f"{colour_id}_{size_id}"] = sku

        return skus

    def image_urls(self, response):
        return clean(response.css('.pagination ::attr(src)'))


class PaginationLE:
    def extract_links(self, response):
        if not response.css('#productGrid'):
            return []
        base_url = response.urljoin('#!/page/only')
        total_count = int(clean(response.css('#productGrid ::attr(data-page-count)'))[0])

        return [
            Link(base_url.replace('page', 'page' + str(idx)))
            for idx in range(1, total_count + 1)
        ]


class LindexCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.mainMenu'
    ]

    products_css = [
        '.info .productCardLink'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(PaginationLE(), 'parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class LindexParseSpiderUK(LindexParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class LindexCrawlSpiderUK(LindexCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = LindexParseSpiderUK()

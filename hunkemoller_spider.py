import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'hunkemoller'
    allowed_domains = ['hunkemoller.de']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'

    start_urls = ['https://www.hunkemoller.de/']
    default_brand = 'Hunkemöller'


class HunkemollerParseSpider(BaseParseSpider):
    price_css = '.product-info [itemprop="price"]'
    care_css = '.washing-tips ::text'
    raw_description_css = '.description ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        product_id = clean(response.css('.article-number::text'))[0]
        return product_id.split()[1]

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs ::attr(title)'))

    def image_urls(self, response):
        raw_image_urls = clean(response.css(".scroller ::attr(rel)"))
        return [json.loads(url)['zoomimage'] for url in raw_image_urls]

    def skus(self, response):
        skus = {}
        currency = clean(response.css('.product-info [itemprop="priceCurrency"]::attr(content)'))
        colour = clean(response.css('.pdp-colors [class="active"] ::attr(title)'))
        sizes = response.css('.product-info .selectmenu :not([selected]):not(span)')

        common_sku = self.product_pricing_common(response)
        common_sku['color'] = colour[0]
        common_sku['currency'] = currency[0]

        for size_s in sizes:
            sku = common_sku.copy()
            sku_id, sku_data = json.loads(clean(size_s.css('::attr(data-additional)'))[0]).popitem()

            if not sku_data['is_in_stock']:
                sku['out_of_stock'] = True

            size = clean(size_s.css('::text'))[0]
            sku['size'] = size

            skus[sku_id] = sku

        return skus


class HunkemollerCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.nav',
        '.pages',
        '.color-options'
    ]

    products_css = [
        '.product-image'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class HunkemollerDEParseSpider(HunkemollerParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class HunkemollerDECrawlSpider(HunkemollerCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = HunkemollerDEParseSpider()

import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'hunkemoller'
    allowed_domains = ['hunkemoller.de']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    currency = 'EUR'

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

        raw_sku_css = '.product-info .selectmenu :not([selected]):not(span)'
        raw_skus = response.css(f"{raw_sku_css} ::attr(data-additional)").extract()
        sizes = clean(response.css(f"{raw_sku_css}::text"))

        colour = clean(response.css('.pdp-colors [class="active"] ::attr(title)'))[0]
        previous_price, price, _ = self.product_pricing(response)
        common_sku = {
            'price': price,
            'currency': self.currency,
        }
        if previous_price:
            common_sku['previous_prices'] = previous_price
        if colour:
            common_sku['colour'] = colour

        for size, raw_variant in zip(sizes, raw_skus):
            sku = common_sku.copy()
            sku_data = json.loads(raw_variant)

            if not next((key['is_in_stock'] for key in sku_data.values())):
                sku['out_of_stock'] = True

            sku['size'] = size
            skus[next(iter(sku_data))] = sku

        return skus


class HunkemollerCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.nav',
        '.pages',
        '.color-options'
    ]

    product_css = [
        '.product-image'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class HunkemollerDEParseSpider(HunkemollerParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class HunkemollerDECrawlSpider(HunkemollerCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = HunkemollerDEParseSpider()

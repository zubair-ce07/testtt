from copy import deepcopy

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'liujo-uk'
    market = 'UK'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb/']
    gender = 'women'


class LiujoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-main-info .price::text'

    def parse(self, response):

        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        common = deepcopy(self.product_pricing_common_new(response))
        colors = response.css('#configurable_swatch_color [name]')
        sizes = response.css('#configurable_swatch_liujo_size [name]')
        sku_ids = [color_sel.css('::attr(id)') for color_sel in colors] if colors else [size_sel.css('::attr(id)') for size_sel in sizes]

        skus = {}

        if not sku_ids:
            common['size'] = self.one_size
            skus[self.one_size] = common
            return skus

        for color_sel in colors:
            sku = deepcopy(common)
            sku_id = clean(color_sel.css('::attr(id)'))[0]
            sku['color'] = clean(color_sel.css('::attr(name)'))[0]

            if sizes:
                for size_sel in sizes:
                    size = clean(size_sel.css('::attr(title)'))[0]
                    sku['size'] = size
                    skus[sku_id + '-' + size] = deepcopy(sku)
            else:
                sku['size'] = self.one_size
                skus[sku_id] = sku

        if not skus:
            for size_sel in sizes:
                sku_id = clean(size_sel.css('::attr(id)'))[0]
                skus[sku_id] = deepcopy(common)
                skus[sku_id]['size'] = clean(size_sel.css('::attr(title)'))[0]

        return skus

    def product_category(self, response):
        return [t for t, _ in response.meta['trail'] if t] if response.meta['trail'] else ''

    def image_urls(self, response):
        return clean(response.css('.product-media-gallery img::attr(data-more-views)'))

    def product_id(self, response):
        return clean(response.css('.product-ids::text'))[0].replace('Item ', '')

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_description(self, response):
        return clean(response.css('.short-description-value ::text')) + [care for care in clean(response.css('.details-value ::text')) if not self.care_criteria_simplified(care)]

    def product_care(self, response):
        return [care for care in clean(response.css('.details-value ::text')) if self.care_criteria_simplified(care)]

    def product_brand(self, response):
        return 'Liujo'


class LiujoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LiujoParseSpider()

    listing_css = '.second-level [target="_self"]'

    pagination_css = '[rel="next"]'

    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=pagination_css),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item')
    )
    #
    # def paging_request(self, response):
    #     for request in self.parse(response):
    #         yield request
    #
    #     if response.css(self.pagination_css):
    #         yield Request(url=clean(response.css(self.pagination_css))[0], callback=self.paging_request)
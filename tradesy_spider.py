from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'tradesy-us'
    market = 'US'
    gender = Gender.WOMEN.value

    allowed_domains = ['tradesy.com']
    start_urls = [
        'https://www.tradesy.com'
    ]


class TradesyParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.item-price-original-list span::text,.item-price-retail::text,.item-price::text'
    raw_description_css = '#idp-info .truncate-copy::text'

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
        return clean(response.css('.item-id::text').re_first('(\d+)'))

    def product_name(self, response):
        return clean(response.css('#idp-title::text'))[0]

    def product_brand(self, response):
        return clean(response.css('.idp-details p:contains(Brand) + p ::text'))[0]

    def product_category(self, response):
        return clean(response.css('#idp-breadcrumbs li span[itemprop=name]::text')[1:])

    def skus(self, response):
        sku = self.product_pricing_common(response)

        size = response.css('.idp-details p:contains(Size) + p ::text')
        sku_id = sku['size'] = clean(size)[0] if size else self.one_size
        colour = self.product_colour(response)

        if colour:
            sku['colour'] = colour
            sku_id = f"{sku['size']}_{colour}"

        return {sku_id: sku}

    def image_urls(self, response):
        return clean(response.css('#idp-main-gallery ::attr(href)'))

    def product_colour(self, response):
        colour_sel = response.css('.idp-details p:contains(Color) + p')

        if colour_sel:
            return ''.join(clean(sel.css('::text'))[0] for sel in colour_sel)


class TradesyCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = TradesyParseSpider()

    products_css = '.item-tile'
    listings_css = [
        '.trd-dropdown',
        '#page-next'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

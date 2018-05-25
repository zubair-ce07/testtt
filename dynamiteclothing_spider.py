from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'dynamite-ca'
    market = 'CA'
    default_brand = 'Dynamite'
    gender = Gender.WOMEN.value

    allowed_domains = ['www.dynamiteclothing.com']
    start_urls = ['https://www.dynamiteclothing.com/ca']


class DynamiteParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    price_css = '.prodPricePDP ::text'
    raw_description_css = '#descTabDescriptionContent ::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        color_css = '#productColours .swatchColor::text'
        common_sku['colour'] = colour = clean(response.css(color_css))[0]

        sizes = clean(response.css('#productSizes > span::text'))
        unavailable_sizes = clean(response.css('#productSizes > .unavailable::text'))

        for size in sizes or [self.one_size]:
            sku = common_sku.copy()
            if size in unavailable_sizes:
                sku['out_of_stock'] = True

            sku['size'] = size = size.strip()

            skus[f'{colour}_{size}'] = sku

        return skus

    def product_id(self, response):
        return clean(response.css('input[name="product"]::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.prodName::text'))[0]

    def image_urls(self, response):
        return clean(response.css('#additionalViewsPDP ::attr(href)'))


class DynamiteCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DynamiteParseSpider()

    listings_css = [
        '.subCatLink',
        '#catPageNext'
    ]

    deny_re = [
        'community/rsvp-collection-editorial',
        'giftcard/giftcard.jsp'
    ]

    products_css = '.prodListingImg'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

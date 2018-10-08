from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'bonton'
    default_brand = 'bonton'
    allowed_domains = ['bonton.fr']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.bonton.fr/fr/']


class BontonParseSpider(BaseParseSpider):
    one_sizes = [
        'TU'
    ]

    description_css = '[itemprop="description"] ::text'
    care_css = '.composition ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['url'] = garment['url_original']
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        return clean(response.css('#product_id ::attr(value)'))[0]

    def product_gender(self, response):
        trail = [url for _, url in response.meta.get('trail') or []]
        soup = [response.url] + self.product_category(response) + trail
        return self.gender_lookup(soupify(soup)) or Gender.KIDS.value

    def product_category(self, response):
        return clean(response.css('.breadcrumb [itemprop="title"] ::text'))

    def image_urls(self, response):
        return clean(response.css('.swiper-slide .zoom img::attr(data-src)'))

    def product_name(self, response):
        return clean(response.css('[itemprop="name"] ::text'))[0]

    def skus(self, response):
        skus = {}
        colour = clean(response.css('.color-active ::text'))

        for size_id in clean(response.css('[data-attribute-code="size"] a::attr(data-entity-id)')):

            money_str = clean(response.css(f'[id*="{size_id}"] ::text'))
            sku = self.product_pricing_common(None, money_strs=money_str)

            if colour:
                sku['colour'] = colour[0]

            size = clean(response.css(f'li [data-entity-id="{size_id}"] ::text'))[0]
            sku['size'] = self.one_size if size.lower() in self.one_sizes else size

            if clean(response.css(f'[class*="{size_id}"] ::attr(content)'))[0] != 'in_stock':
                sku['out_of_stock'] = True

            skus[f"{colour[0]}_size" if colour else size] = sku

        return skus


def see_all(url):
    return url + '?limit/1000/'


class BontonCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.level-top[href*=garcon]',
        '.level-top[href*=fille]',
        '.level-top[href*=bebe]'
    ]

    products_css = [
        '.product-name'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, process_value=see_all), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    ]


class BontonFRParseSpider(MixinFR, BontonParseSpider):
    name = MixinFR.retailer + '-parse'


class BontonFRCrawlSpider(MixinFR, BontonCrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = BontonFRParseSpider()

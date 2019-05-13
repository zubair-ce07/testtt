import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'cabourn-us'
    market = 'US'
    default_brand = 'Nigel Cabourn'

    allowed_domains = ['cabourn.com']
    start_urls = ['https://www.cabourn.com/']


class CabournParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'
    price_css = '.regular-price .price::text , .special-price .price::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        return garment

    def product_id(self, response):
        return clean(response.css('.no-display input::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def image_urls(self, response):
        css = '.MagicToolboxSelectorsContainer a::attr(href),.MagicToolboxContainer a::attr(href)'
        return response.css(css).getall()

    def raw_description(self, response):
        return clean(response.css('.pp-description p::text'))

    def product_description(self, response):
        desc = clean(response.css('.description::text'))
        return desc + [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_gender(self, response):
        soup = ' '.join(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, response):
        return response.url.split('/')[4:]

    def variants(self, response):
        script_text = response.xpath('//script[contains(., "Product.ConfigDefaultText")]/text()').getall()
        raw_text = script_text[0].split('Product.ConfigDefaultText(')[1].split(')')[0]
        raw_json = json.loads(raw_text)

        return raw_json

    def skus(self, response):
        retailer_sku = self.product_id(response)
        common_sku = self.product_pricing_common(response)
        colour = self.detect_colour_from_name(response)

        if colour:
            common_sku['colour'] = colour

        skus = {}
        raw_json = self.variants(response)
        for variant in raw_json['attributes']['174']['options']:
            sku = common_sku.copy()
            size = variant['label']
            sku['size'] = size
            sku['sku_id'] = retailer_sku + size

            skus[f'{retailer_sku}_{size}'] = sku

        return skus


class CabournCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = CabournParseSpider()

    listings_css = [
        '.sub-menu'
    ]
    products_css = [
        '.product-name'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

    def parse(self, response):
        yield from super().parse(response)

        next_page_url = clean(response.css('.next.i-next ::attr(href)'))
        if next_page_url:
            response.meta['trail'] = self.add_trail(response)
            yield response.follow(next_page_url[0], callback=self.parse)

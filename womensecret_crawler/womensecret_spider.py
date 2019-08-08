import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'womensecret-es'
    market = 'ES'

    allowed_domains = ['womensecret.com']
    start_urls = ['https://womensecret.com/es/es']


class WomenSecretParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    price_css = '.c02__sales-price ::text , .c02__standard-price ::text'
    description_css = '.c02__product-description ::text'
    care_css = '[data-target="composition-care"] ::text'
    deny_care = ['Composición y cuidados']

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('#pid::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.c02__product-name::text'))[0]

    def image_urls(self, response):
        return clean(response.css('dataimage::attr(data-image-large)'))

    def product_gender(self, response):
        return 'men' if 'men' in response.url else "women"

    def product_brand(self, response):
        gender = self.product_gender(response)
        return "Men'secret" if gender == 'men' else "Women'secret"

    def product_category(self, response):
        raw_json = response.css('script:contains("breadcrumb")::text').re_first('breadcrumb = (.*)?;')
        return clean(json.loads(raw_json))

    def colour_requests(self, response):
        css = '.c02__swatch-list li:not(.selected) a::attr(href)'
        color_urls = clean(response.css(css))
        
        return [response.follow(url, callback=self.parse_colour) for url in color_urls]

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        colour = clean(response.css('.c02__color-description span::text'))[0]
        if colour:
            common_sku['colour'] = colour

        skus = {}
        for size_s in response.css('.c02__sizes .swatch-item'):
            sku = common_sku.copy()
            sku['size'] = size = clean(size_s.css('::text'))[0]

            if size_s.css('.unselectable'):
                sku['out_of_stock'] = True

            size_type = response.css('.c02__cups .swatch-item')
            for size_type_s in size_type:
                sku_type = sku.copy()
                sku_type['size'] = f'{size}_{clean(size_type_s.css("::text"))[0]}'

                if size_type_s.css('.unselectable'):
                    sku_type['out_of_stock'] = True

                skus[f'{sku_type["size"]}_{colour}'] = sku_type

            if not size_type:
                skus[f'{sku["size"]}_{colour}'] = sku

        return skus


class WomenSecretCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = WomenSecretParseSpider()

    listings_css = [
        '.c03__item--level-3',
        '.pagination__list'
    ]
    products_css = [
        '.product-name'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, tokenize, clean
from scrapy import Request


class Mixin(object):
    market = 'DE'
    retailer = 'schuhcenter-de'
    lang = 'de'
    allowed_domains = ['www.schuhcenter.de']
    start_urls = [
        'http://www.schuhcenter.de/'
    ]
    GENDER_MAP = [
        ('herren', 'boys'),
        ('damen', 'girls'),
        ('mädchen', 'girls')
    ]


class SchuhcenterParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//span[contains(@itemprop, 'price')]//text()|//span[" \
              "@class='oldPrice']//text()"

    care_materials = [
        'obermaterial'
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response, response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        if not garment['skus']:
            garment['out_of_stock'] = True

        return [garment] + self.color_requests(response)

    def raw_description(self, response):
        return clean(response.css('.visible-lg li > label::text,[itemprop="description"] li ::text').extract())

    def product_care(self, response):
        return [x for x in self.raw_description(response) if \
                self.care_criteria_simplified(x)]

    def product_description(self, response):
        return [x for x in self.raw_description(response) if not self.care_criteria_simplified(x)]

    def raw_name(self, response):
        return response.css('h1[itemprop=name]::text').extract_first()

    def product_brand(self, response):
        raw_name = self.raw_name(response)
        return clean(raw_name.split('-'))[0]

    def currency(self, response):
        css = '[itemprop=priceCurrency]::attr(content)'
        return clean(response.css(css).extract_first())

    def color_requests(self, response):
        request_urls = response.css('.col_sel a::attr(href)').extract()
        return [Request(url, callback=self.parse) for url in request_urls]

    def product_id(self, response):
        return clean(response.css('.visible-lg > p ::text').extract_first().split('.:'))[1]

    def product_category(self, response):
        return clean(response.css('[itemprop=title]::text').extract())[1:]

    def product_gender(self, garment):
        soup = tokenize(garment['category'] + garment['description'])
        for token, gender in self.GENDER_MAP:
            if token in soup:
                return gender
        return 'unisex-kids'

    def product_color(self, response):
        raw_name = self.raw_name(response).split('-')
        return clean(raw_name)[-1]

    def skus(self, response):
        skus = {}
        common = {
            'colour': self.product_color(response),
            'currency': self.currency(response),
        }
        for size_var in response.css('.size_info li > a'):
            sku = common.copy()
            previous_price, sku['price'], _ = self.product_pricing(response)
            sku['size'] = clean(size_var.css('span::text'))[0]

            if previous_price:
                sku['previous_prices'] = [previous_price]

            if size_var.css('.no_stock'):
                sku['out_of_stock'] = True

            size_id = size_var.css('::attr(data-selection-id)').extract_first()
            skus[common['colour'] + '_' + size_id] = sku

        return skus

    def image_urls(self, response):
        css = '.otherPictures img::attr(src)'
        return [i.replace('87_87', '1000_1000') for i in response.css(
            css).extract()]

    def product_name(self, response):
        raw_name = self.raw_name(response).split('-')
        return clean(''.join(raw_name[1:-1]))


class SchuhcenterCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SchuhcenterParseSpider()
    listings_css = [
        '.flyoutholder .main_categories ul',
        '.next'
    ]
    products_css = '.over-links'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

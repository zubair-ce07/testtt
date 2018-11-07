# -*- coding: utf-8 -*-
import json
import re

from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

from ..items import Item
from ..utilities import pricing


class Mixin:
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['https://www.mooseknucklescanada.com']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    }


class MooseknucklesParseSpider(Mixin, Spider):
    name = 'mooseknuckles-parse'

    def parse(self, response):
        item = Item()

        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['gender'] = self.extract_gender(response)
        item['category'] = self.extract_category(response)
        item['url'] = self.extract_product_url(response)
        item['skus'] = self.make_skus(response)

        return item

    def extract_retailer_sku(self, response):
        retailer_sku_css = 'meta[property="product:retailer_item_id"]::attr(content)'
        return response.css(retailer_sku_css).extract_first()

    def extract_name(self, response):
        name_css = 'meta[property="og:title"]::attr(content)'
        return response.css(name_css).extract_first()

    def extract_gender(self, response):
        gender_css = 'button.btn-cart::attr(data-category)'
        return response.css(gender_css).extract_first().split('/')[0]

    def extract_care(self, response):
        care_css = 'div.tab-content > li::text'
        return ' '.join(response.css(care_css).extract())

    def extract_description(self, response):
        description_css = 'div.tab-content > div::text'
        description = response.css(description_css).extract()
        return description[0].strip() if description else None

    def extract_image_urls(self, response):
        image_urls_css = 'div.product-image-gallery img::attr(src)'
        return response.css(image_urls_css).extract()

    def extract_product_url(self, response):
        return response.url

    def extract_category(self, response):
        category_css = 'button.btn-cart::attr(data-category)'
        return response.css(category_css).extract_first().split('/')

    def extract_money_strings(self, raw_price):
        return [raw_price['basePrice'], raw_price['oldPrice']]

    def extract_currency(self, response):
        currency_css = 'meta[property="product:price:currency"]::attr(content)'
        return response.css(currency_css).extract_first()

    def extract_raw_skus(self, response):
        raw_skus = response.css('div.product-options script::text').extract_first()
        raw_skus = re.search('Product.Config[(](.*)[)];', raw_skus).group(1)
        return json.loads(raw_skus)

    def make_skus(self, response):
        raw_skus = self.extract_raw_skus(response)
        skus = {}

        common_sku = pricing(self.extract_money_strings(raw_skus))
        common_sku['currency'] = self.extract_currency(response)

        raw_colours = raw_skus['attributes']['141']['options']
        raw_sizes = raw_skus['attributes']['142']['options']

        for raw_colour in raw_colours:
            colour = raw_colour['label']

            for raw_size in raw_sizes:
                sku = common_sku.copy()
                
                size = 'One Size' if raw_size['label'] == 'OS' else raw_size['label']

                sku['size'] = size
                sku['colour'] = colour

                if not self.check_common_product(raw_colour, raw_size):
                    sku['out_of_stock'] = True

                skus[f'{colour}_{size}'] = sku

        return skus

    def check_common_product(self, raw_colour, raw_size):
        return set(raw_colour['products']).intersection(raw_size['products'])


class MooseknucklesCrawlSpider(Mixin, CrawlSpider):
    name = 'mooseknuckles-crawl'

    listings_x = ['//ol[contains(@class, "nav-primary")]', '//div[@class="pager"]']
    products_x = ['//a[contains(@class,"shop-now")]']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_x)),
        Rule(LinkExtractor(restrict_xpaths=products_x), callback='parse_product')
    )

    product_parser = MooseknucklesParseSpider()

    def parse_product(self, response):
        return self.product_parser.parse(response)

    def parse(self, response):
        for request_or_item in super().parse(response):
            if isinstance(request_or_item, Request):
                request_or_item.meta['trail'] = self.make_trail(response)
                yield request_or_item

    def make_trail(self, response):
        link_text = response.meta.get('link_text') or ''
        return (response.meta.get('trail') or []) + [(link_text, response.url)]

import json

import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule, Request, Spider


class Product(Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    requests_queue = scrapy.Field()


class OnlyParser(Spider):
    name = 'onlyparser'

    default_brand = 'Only'
    default_size = 'One_Size'

    default_gender = 'unisex'
    gender_map = {
        'kids': 'kids',
        'femmes': 'women',
    }

    def parse(self, response):
        item = Product()
        raw_item = self.extract_raw_item(response)

        item['url'] = response.url
        item['brand'] = self.extract_brand_name(response)
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_category(raw_item)
        item['gender'] = self.extract_gender(raw_item)
        item['description'] = self.extract_description(raw_item)
        item['requests_queue'] = self.construct_sku_requests(raw_item)
        item['image_urls'] = self.extract_image_urls(raw_item)
        item['skus'] = []

        return self.get_item_or_next_request(item)

    def parse_sku(self, response):
        item = response.meta['item']
        item['skus'] += self.extract_skus(response)

        return self.get_item_or_next_request(item)

    def extract_pricing(self, response):
        pricing = {}
        price_css = '.value__price--discounted ::text, .value__price ::text'
        previous_price_css = '.nonsticky-price__container--visible .value__price--discounted ::text'
        currency_css = '[property="og:price:currency"] ::attr(content)'

        pricing['price'] = clean(response.css(price_css))[0]
        pricing['previous_prices'] = clean(response.css(previous_price_css))
        pricing['currency'] = clean(response.css(currency_css))[0]

        return pricing

    def extract_gender(self, raw_item):
        for gender in self.gender_map.keys():
            if gender in raw_item['@graph'][0]['description'].lower():
                return self.gender_map[gender]

        return self.default_gender

    def extract_lengths(self, response):
        length_css = '.length .swatch__item-inner-text__text-container ::text'
        return clean(response.css(length_css))

    def extract_colour(self, response):
        return clean(response.css('.color-combination ::text'))

    def extract_size(self, response):
        size_css = '.size .swatch__item--selected .swatch__item-inner-text__text-container ::text'
        return clean(response.css(size_css))

    def extract_image_urls(self, raw_item):
        return [item['image'] for item in raw_item['@graph'] if item.get('image')]

    def extract_item_name(self, response):
        return clean(response.css('.product-name--visible ::text'))[0]

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_retailer_sku(self, response):
        return response.css('.pdp-description__text__value--article-nr ::text').re_first(r'(\d+)')

    def extract_care(self, response):
        css = '.pdp-description__list li:not(.pdp-description__text__value--article-nr)' \
              ':not(.pdp-description__text__value--ean) ::text'
        return clean(response.css(css))

    def extract_raw_item(self, response):
        return json.loads(clean(response.css('script[class="js-structuredData"]::text'))[0])

    def extract_category(self, raw_item):
        return clean(raw_item['@graph'][0]['category'])

    def extract_description(self, raw_item):
        raw_description = clean(raw_item['@graph'][0]['description'])
        return [desc for sublist in raw_description for desc in sublist.split('.') if desc]

    def get_item_or_next_request(self, item):
        if not item['requests_queue']:
            del item['requests_queue']
            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_sku_requests(self, raw_item):
        return [Request(item['url'], callback=self.parse_sku) for item in raw_item['@graph']]

    def extract_skus(self, response):
        skus = []
        common_sku = self.extract_pricing(response)
        colour = self.extract_colour(response)

        if colour:
            common_sku['colour'] = colour[0]

        size = (self.extract_size(response) or [self.default_size])[0]
        lengths = self.extract_lengths(response)

        for length in lengths:
            sku = common_sku.copy()
            size_length = f'{size}/{length}'
            sku['size'] = size_length
            sku['sku_id'] = f'{size_length}_{colour[0]}' if colour else size_length

            skus.append(sku)

        if not skus:
            common_sku['size'] = size
            common_sku['sku_id'] = f'{size}_{colour[0]}' if colour else size
            skus.append(common_sku)

        return skus


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip().split(' > ')
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]


class OnlyCrawler(CrawlSpider, OnlyParser):
    name = 'only'
    allowed_domains = ['only.com']
    start_urls = ['https://www.only.com/fr/fr/home']

    category_css = '.category-navigation__item:not(.category-navigation__item--see-all)'
    pagination_css = '.paging-controls__page-numbers-boxes'
    product_css = '.plp__products__item .product-tile__image'

    parser = OnlyParser()

    rules = (
        Rule(LinkExtractor(restrict_css=(category_css, pagination_css),
                           attrs=('data-href', 'href'))),
        Rule(LinkExtractor(restrict_css=product_css), callback=parser.parse),
    )

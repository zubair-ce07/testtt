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
        raw_product = self.extract_raw_product(response)

        item['url'] = response.url
        item['brand'] = self.extract_brand_name(response)
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['care'] = self.extract_care(response)
        item['category'] = self.extract_category(raw_product)
        item['gender'] = self.extract_gender(raw_product)
        item['description'] = self.extract_description(raw_product)
        item['requests_queue'] = self.construct_sku_requests(response, raw_product)
        item['image_urls'] = self.extract_image_urls(raw_product)
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

    def extract_gender(self, raw_product):
        for gender_key, gender in self.gender_map.items():
            if gender_key in raw_product['@graph'][0]['description'].lower():
                return gender

        return self.default_gender

    def extract_lengths(self, response):
        length_css = '.length .swatch__item--selectable:not(.swatch__item--unavailable) ::text,' \
                     '.length .swatch__item--selected:not(.swatch__item--unavailable) ::text'

        return clean(response.css(length_css))

    def extract_colour(self, response):
        return clean(response.css('.color-combination ::text'))

    def has_length(self, response):
        length_css = '.length .swatch__item--selectable:not(.swatch__item--unavailable),' \
                     '.length .swatch__item--selected:not(.swatch__item--unavailable)'

        if not clean(response.css('.length')):
            return True
        elif clean(response.css(length_css)):
            return True

        return False

    def has_skus(self, response):
        size_css = '.size .swatch__item--selectable:not(.swatch__item--unavailable) ::text,' \
                   '.size .swatch__item--selected:not(.swatch__item--unavailable) ::text'

        return clean(response.css(size_css))

    def extract_size(self, response):
        size_css = '.size .swatch__item--selected .swatch__item-inner-text__text-container ::text'
        return clean(response.css(size_css))

    def extract_image_urls(self, raw_product):
        return [product['image'] for product in raw_product['@graph'] if product.get('image')]

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

    def extract_raw_product(self, response):
        return json.loads(clean(response.css('script[class="js-structuredData"]::text'))[0])

    def extract_category(self, raw_product):
        return clean(raw_product['@graph'][0]['category'])

    def extract_description(self, raw_product):
        raw_description = clean(raw_product['@graph'][0]['description'])
        return [desc for sublist in raw_description for desc in sublist.split('.') if desc]

    def get_item_or_next_request(self, item):
        if not item['requests_queue']:
            del item['requests_queue']
            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_sku_requests(self, response, raw_product):
        return [Request(item['url'], callback=self.parse_sku) for item in raw_product['@graph']] \
            if self.has_skus(response) else []

    def extract_skus(self, response):
        skus = []

        if not self.has_length(response):
            return skus

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


def clean(raw_product):
    if isinstance(raw_product, str):
        return raw_product.strip().split(' > ')
    elif isinstance(raw_product, SelectorList):
        return [r.strip() for r in raw_product.getall() if r.strip()]

    return [r.strip() for r in raw_product if r.strip()]


class OnlyCrawler(CrawlSpider):
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

import json
import re

import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule, Spider


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
    currency = scrapy.Field()
    requests_queue = scrapy.Field()
    raw_colour = scrapy.Field()
    raw_size = scrapy.Field()


class SmiloDoxParser(Spider):
    name = 'smilodox_parser'
    default_brand = 'Smilo'
    default_size = 'One_Size'

    default_gender = 'unisex'
    gender_terms = [
        'women',
        'men',
    ]
    care_terms = [
        'cotton',
        'machine wash',
        'polyester'
    ]

    def parse(self, response):
        item = Product()
        item['url'] = response.url
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['brand'] = self.extract_brand_name(response)
        item['category'] = self.extract_category(response)
        item['gender'] = self.extract_gender(response)
        item['currency'] = self.extract_currency(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['description'] = self.extract_description(response)
        item['requests_queue'] = self.construct_variant_requests(response)

        return self.get_item_or_next_request(item)

    def parse_variants(self, response):
        item = response.meta['item']
        raw_variants = json.loads(re.findall(r'variations+\s=\s([^;]*);}', response.text)[0])
        skus = []
        common_sku = {
            'currency': item['currency']
        }

        for key in raw_variants.keys():
            sku = common_sku.copy()

            if raw_variants[key].get('valueIds'):
                colour_size_code = raw_variants[key]['valueIds']
                sku['colour'] = colour_size_code[0]
                sku['size'] = colour_size_code[1]

            sku['price'] = raw_variants[key]['variationPrice']

            skus.append(sku)

        item['skus'] = skus

        colour_url = re.findall(r'([/a-z_]*/ec/[a-z0-9_.]*)', response.text)
        size_url = re.findall(r'([/a-z_]*/c8/[a-z0-9_.]*)', response.text)

        item['requests_queue'] += [response.follow(url=colour_url[0], callback=self.parse_colours)] \
            if colour_url else []
        item['requests_queue'] += [response.follow(url=size_url[0], callback=self.parse_sizes)] \
            if size_url else []

        return self.get_item_or_next_request(item)

    def parse_colours(self, response):
        item = response.meta['item']
        item['raw_colour'] = json.loads(re.findall(r'"values":(.*)};}', response.text)[0])
        item['skus'] = self.extract_skus(item)

        return self.get_item_or_next_request(item)

    def parse_sizes(self, response):
        item = response.meta['item']
        item['raw_size'] = json.loads(re.findall(r'"values":(.*)};}', response.text)[0])
        item['skus'] = self.extract_skus(item)

        return self.get_item_or_next_request(item)

    def extract_skus(self, item):
        skus = item['skus']
        for sku in skus:
            sku['size'] = self.extract_size(sku['size'], item['raw_size']) \
                if item.get('raw_size') else self.default_size
            sku['sku_id'] = sku['size']

            if item.get('raw_colour'):
                sku['colour'] = self.extract_colour(sku['colour'], item['raw_colour'])
                sku['sku_id'] += f'_{sku["colour"]}'

        return skus

    def get_item_or_next_request(self, item):
        if not item['requests_queue']:
            del item['raw_colour']
            del item['raw_size']
            del item['currency']
            del item['requests_queue']

            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_variant_requests(self, response):
        return [response.follow(url=self.extract_variant_url(response)[0], callback=self.parse_variants)]

    def extract_colour(self, colour_code, colours):
        return colours[str(colour_code)]['name']

    def extract_currency(self, response):
        raw_currency = json.loads(response.css('script::text').re_first(r'\d\,\s+\d,\s(.+)\);'))
        return raw_currency['currency']['name']

    def extract_size(self, size_code, sizes):
        return sizes[str(size_code)]['name'] if sizes.get(str(size_code)) else self.default_size

    def extract_variant_url(self, response):
        return clean(response.css('.div_plenty_attribute_selection script ::attr(src)'))

    def extract_item_name(self, response):
        return clean(response.css('[itemprop=name]::text'))[0]

    def extract_brand_name(self, response):
        return self.default_brand

    def extract_retailer_sku(self, response):
        return clean(response.css('[itemprop=mpn]::text'))[0]

    def extract_category(self, response):
        return clean(response.css('.breadcrumb a::text'))

    def extract_gender(self, response):
        for gender in self.extract_category(response):
            if gender.lower() in self.gender_terms:
                return gender.lower()

        return self.default_gender

    def extract_image_urls(self, response):
        return clean(response.css('.list-unstyled ::attr(data-img-link)'))

    def extract_description(self, response):
        raw_description = self.raw_description(response)
        return [desc for desc in raw_description if all(c not in desc for c in self.care_terms)]

    def extract_care(self, response):
        raw_cares = self.raw_description(response)
        return [c for c in raw_cares if any(care_t in c.lower() for care_t in self.care_terms)]

    def raw_description(self, response):
        css = '.product_description p::text'
        raw_description = clean(response.css(css))

        return [desc for sublist in raw_description for desc in sublist.split('.') if desc]


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip()
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]


class SmiloDoxCrawler(CrawlSpider):
    name = 'smilodox'

    allowed_domains = ['smilodox.com']
    start_urls = ['https://www.smilodox.com/']
    listings_css = ['.dropdown-menu .menu-level3', '[rel="next"]']
    product_css = '.thumb'

    parser = SmiloDoxParser()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css, attrs='data-href', tags='article'),
             callback=parser.parse)
    )

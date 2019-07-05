import json
import re

import scrapy
from scrapy.item import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule, Spider, Request


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
    variant_json = scrapy.Field()
    colour_map = scrapy.Field()
    size_map = scrapy.Field()


class SmiloDoxParser(Spider):
    name = "smilodpx_parser"
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

    size_map_t = 'https://www.smilodox.com/tpl/item/attribute_check/attribute/en/c8{}'
    colour_map_t = 'https://www.smilodox.com/tpl/item/attribute_check/attribute/en/ec{}'

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

    def get_item_or_next_request(self, item):
        if not item['requests_queue']:
            item['skus'] = self.extract_skus(item)

            del item['variant_json']
            del item['colour_map']
            del item['size_map']
            del item['currency']
            del item['requests_queue']

            return item

        request = item['requests_queue'].pop()
        request.meta['item'] = item

        return request

    def construct_variant_requests(self, response):
        return [response.follow(url=self.extract_variant_url(response)[0], callback=self.extract_variants)]

    def extract_variants(self, response):
        item = response.meta['item']
        item['variant_json'] = json.loads(re.findall(r'variations+\s=\s([^;]*);}', response.text)[0])

        colour_url = re.findall(r'/en/ec([/a-zA-z0-9_.]*)', response.text)
        size_url = re.findall(r'/en/c8([/a-zA-z0-9_.]*)', response.text)

        item['requests_queue'] += [Request(url=self.colour_map_t.format(colour_url[0]),
                                           callback=self.extract_colour_map)] if colour_url else []
        item['requests_queue'] += [Request(url=self.size_map_t.format(size_url[0]),
                                           callback=self.extract_size_map)] if size_url else []

        return self.get_item_or_next_request(item)

    def extract_colour_map(self, response):
        item = response.meta['item']
        item['colour_map'] = json.loads(re.findall(r'"values":(.*)};}', response.text)[0])

        return self.get_item_or_next_request(item)

    def extract_size_map(self, response):
        item = response.meta['item']
        item['size_map'] = json.loads(re.findall(r'"values":(.*)};}', response.text)[0])

        return self.get_item_or_next_request(item)

    def extract_skus(self, item):
        skus = []
        common_sku = {
            'currency': item['currency']
        }

        for key in item['variant_json'].keys():
            sku = common_sku.copy()
            colour_size_code = item['variant_json'][key]['valueIds']

            sku['size'] = self.extract_size(colour_size_code[1], item['size_map']) \
                if item.get('size_map') else self.default_size
            sku['sku_id'] = sku['size']

            if item.get('colour_map'):
                sku['colour'] = self.extract_colour(colour_size_code[0], item['colour_map'])
                sku['sku_id'] += f'_{sku["colour"]}'

            sku['price'] = item['variant_json'][key]['variationPrice']

            skus.append(sku)

        return skus

    def extract_colour(self, colour_code, colour_json):
        return colour_json[str(colour_code)]['name']

    def extract_currency(self, response):
        raw_currency = json.loads(response.css('script::text').re_first(r'\d\,\s+\d,\s(.+)\);'))
        return raw_currency['currency']['name']

    def extract_size(self, size_code, size_json):
        return size_json[str(size_code)]['name']

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

    category_css = '.dropdown-menu .menu-level3'
    pagination_css = '[rel="next"]'
    product_css = '.thumb'

    parser = SmiloDoxParser()

    rules = (
        Rule(LinkExtractor(restrict_css=(category_css, pagination_css))),
        Rule(LinkExtractor(restrict_css=product_css, attrs='data-href', tags='article'),
             callback=parser.parse)
    )

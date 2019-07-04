import json

import scrapy
from scrapy.item import Item
from scrapy.selector import SelectorList
from scrapy.spiders import Request


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
    variant_json = scrapy.Field()
    colour_map = scrapy.Field()
    size_map = scrapy.Field()


class SmiloDoxParser:
    default_brand = 'Smilo'
    default_gender = 'unisex'
    default_size = 'One_Size'
    default_currency = 'EUR'

    gender_terms = [
        'women',
        'men',
    ]
    care_terms = [
        'cotton',
        'machine wash',
        'polyester'
    ]

    colour_map_url = 'https://www.smilodox.com/tpl/item/attribute_check/attribute/en/ec/' \
                     'attribute_id_3__date_03_07_2019_9_2063.js'
    size_map_url = 'https://www.smilodox.com/tpl/item/attribute_check/attribute/en/c8/' \
                   'attribute_id_2__date_03_07_2019_9_2063.js'

    def parse_item(self, response):
        item = Product()
        item['url'] = response.url
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['brand'] = self.extract_brand_name(response)
        item['category'] = self.extract_category(response)
        item['gender'] = self.extract_gender(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['description'] = self.extract_description(response)

        return self.get_item_or_variant_request(item, response)

    def get_item_or_variant_request(self, item, response):
        if item.get('variant_json') or not self.extract_variant_url(response):
            item.pop('variant_json', None)
            item.pop('colour_map', None)
            item.pop('size_map', None)

            return item

        request = response.follow(url=self.extract_variant_url(response)[0],
                                  callback=self.extract_variants)
        request.meta['item'] = item

        return request

    def extract_variants(self, response):
        item = response.meta['item']
        regex = r'variations = (.*);}if \(PY\.Item\[\d+\]\.images === undefined\)'
        item['variant_json'] = json.loads(response.css('*').re_first(regex))

        request = Request(url=self.colour_map_url, callback=self.extract_colour_map)
        request.meta['item'] = item

        return request

    def extract_colour_map(self, response):
        item = response.meta['item']
        item['colour_map'] = json.loads(response.css('*').re_first(r'"values":(.*)};}'))

        request = Request(url=self.size_map_url, callback=self.extract_size_map)
        request.meta['item'] = item

        return request

    def extract_size_map(self, response):
        item = response.meta['item']
        item['size_map'] = json.loads(response.css('*').re_first(r'"values":(.*)};}'))
        item['skus'] = self.extract_skus(item)

        return self.get_item_or_variant_request(item, response)

    def extract_skus(self, item):
        skus = []

        for key in item['variant_json'].keys():
            sku = {}
            colour = self.extract_colour(item['variant_json'][key]['valueIds'][0], item['colour_map'])
            size = self.extract_size(item['variant_json'][key]['valueIds'][1], item['size_map'])
            price = item['variant_json'][key]['variationPrice']

            sku['size'] = size
            sku['colour'] = colour
            sku['price'] = price
            sku['sku_id'] = f'{size}_{colour}'
            sku['currency'] = self.default_currency

            skus.append(sku)

        return skus

    def extract_colour(self, colour_code, colour_json):
        return colour_json[str(colour_code)]['name']

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

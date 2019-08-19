import json
import re

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameters


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class WeItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    requests = Field()


class WeSpider(CrawlSpider):
    name = 'weFashion'
    allowed_domains = ['wefashion.de']
    start_urls = [
        'https://www.wefashion.de/',
    ]

    gender_map = {'Damen': 'women',
                  'Herren': 'men',
                  'Kinder': 'kids'}

    listings_css = ['.level-top-1']
    categories_css = ['.refinement-link']
    products_css = ['.name-link']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=categories_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_pagination(self, response):
        total_products = int(response.css('.plp-progress-bar ::attr(max)').get()) or 30

        for products_count in range(0, total_products, 30):
            range_args = {'sz': 30, 'start': products_count}
            yield response.follow(add_or_replace_parameters(
                response.url, range_args), callback=self.parse)

    def parse_item(self, response):
        css = '#productEcommerceObject ::attr(value)'
        product_json = json.loads(response.css(css).get())

        item = WeItem()
        item['retailer_sku'] = self.retailer_sku(product_json)
        item['gender'] = self.product_gender(product_json)
        item['name'] = self.product_name(product_json)
        item['category'] = self.product_category(product_json)
        item['brand'] = self.product_brand(product_json)
        item['url'] = self.product_url(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def colour_requests(self, response):
        colour_urls = response.css('.color .emptyswatch ::attr(href)').getall()
        return [response.follow(color_url, callback=self.parse_color)
                for color_url in colour_urls]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'] += self.images_url(response)
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        raw_color = response.css('.variant-attribute--color span ::text').get()
        sizes = clean(response.css('#va-size option ::text').getall())

        common_sku = {'color': clean(re.sub('Farbe:|\s+', '', raw_color)),
                      'price': response.css('::attr(data-price)').get(),
                      'previous_price': clean(response.css('.price-standard ::text').get())}
        skus = {}

        for size in sizes or ['OneSize']:
            key = f'{common_sku["color"]}_{size}'
            skus[key] = common_sku.copy()

            if 'Ausverkauft' in size:
                skus[key]['out_of_stock'] = True
            skus[key]['size'] = size.replace('- Ausverkauft', '')

        return skus

    def retailer_sku(self, product_json):
        return product_json['id']

    def product_gender(self, product_json):
        for token, gender in self.gender_map.items():
            if product_json['dimension8'] == token:
                return gender
        return 'uni-Sex'

    def product_name(self, product_json):
        return product_json['name']

    def product_category(self, product_json):
        return product_json['category']

    def product_url(self, response):
        return response.url

    def product_brand(self, product_json):
        return product_json['brand']

    def product_description(self, response):
        return clean(response.css('[itemprop="description"] span ::text').getall())

    def product_care(self, response):
        return [response.css('.washingInstructions ::text').get()]

    def images_url(self, response):
        return response.css('.pdp-figure__image ::attr(data-image-replacement)').getall()

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            return request

        item.pop('requests', None)
        return item


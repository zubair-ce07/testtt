import re
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CeaItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    stock = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class CeaSpider(CrawlSpider):
    name = 'cea'
    allowed_domains = ['cea.com.br']
    start_urls = [
        'https://www.cea.com.br/',
    ]

    gender_dic = {
        'Masculina': 'men',
        'Feminina': 'women',
        'Infantil': 'kids'
    }
    image_url_t = 'https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:' \
                  '{}&sc=1'
    image_t = 'https://cea.vteximg.com.br/arquivos/ids/{}.jpg'
    listing_css = '.header_submenu_item-large'
    product_css = '.product-details_name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_paginantion'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_paginantion(self, response):
        pagination_sel = response.css('script:contains("pagecount")')
        page_count = int(pagination_sel.re_first('pagecount_\d+ = (.+?);'))
        pagination_url = pagination_sel.re_first(".load\(\'(.+?)\' +")

        return [response.follow(url=f'{pagination_url}{page_number}', callback=self.parse)
                for page_number in range(1, page_count)]

    def parse_item(self, response):
        item = CeaItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand()
        item['description'] = self.product_description(response)
        item['care'] = []

        item['skus'] = self.product_skus(response)
        item['image_urls'] = []
        item['requests'] = self.color_requests(response)
        item['requests'].append(self.images_requests(response, item))

        return self.next_request_or_item(item)

    def images_requests(self, response, item):
        return response.follow(self.image_url_t.format(item['retailer_sku']),
                               callback=self.parse_images, meta={'item': item})

    def color_requests(self, response):
        color_queue = response.css('.img-wrapper ::attr(href)').getall()

        return [response.follow(color_url, callback=self.parse_colour)
                for color_url in color_queue]

    def parse_colour(self, response):
        item = response.meta['item']
        item['skus'].update(self.product_skus(response))
        product_id = self.retailer_sku(response)

        return response.follow(self.image_url_t.format(product_id),
                               callback=self.parse_images, meta={'item': item})

    def product_skus(self, response):
        skus = {}
        raw_skus = self.raw_product(response)['skus']

        for sku in raw_skus:
            color = sku.get('dimensions').get('Cor')
            size = sku.get('dimensions').get('Tamanho')
            skus[f'{color}_{size}'] = {
                'out_of_stock': not sku.get('available'),
                'price': sku.get('bestPrice'),
                'previous_price': sku.get('listPrice'),
                'size': size,
                'color': color,
            }

        return skus

    def parse_images(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.get_images_url(response))

        return self.next_request_or_item(item)

    def get_images_url(self, response):
        raw_images_json = json.loads(response.text)[0]['items'][0]

        return [self.image_t.format(i["imageId"])
                for i in raw_images_json['images']]

    def raw_product(self, response):
        raw_css = 'script:contains("var skuJson_0")'
        raw_product = response.css(raw_css).re_first('var skuJson_0 = (.+?);')
        return json.loads(raw_product)

    def retailer_sku(self, response):
        raw_json = self.raw_product(response)
        return raw_json['productId']

    def product_name(self, response):
        return response.css('title::text').get()

    def product_gender(self, response):
        name = self.product_name(response)

        for token, gender in self.gender_dic.items():
            if token in name:
                return gender

        return 'uni-sex'

    def product_category(self, response):
        return response.css('a[property = "v:title"] ::text').getall()

    def product_url(self, response):
        return response.url

    def product_brand(self):
        return 'C&A'

    def product_description(self, response):
        return clean(response.css('.productDescription::text').get())

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request
        item.pop('requests', None)
        return item


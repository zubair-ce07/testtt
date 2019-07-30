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
    parse_product_css = '.product-details_name'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_paginantion'),
        Rule(LinkExtractor(restrict_css=parse_product_css), callback='parse_item'),
    )

    def parse_paginantion(self, response):
        script = response.css('script:contains("pagecount")')
        page_count = int(script.re_first('pagecount_\d+ = (.+?);'))
        page_url_parameters = '{}{{}}'.format(script.re_first(".load\(\'(.+?)\' +"))

        return [response.follow(url=page_url_parameters.format(page_number),
                                callback=self.parse)
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
        item['image_urls'] = []
        item['care'] = []
        item['skus'] = {}
        item['requests'] = self.colour_requests(response)

        return self.next_request_or_item(item)

    def parse_color(self, response):
        return response.follow(url=self.get_image_url(response), callback=self.get_imagesid,
                               meta={'response': response})

    def parse_sku(self, response):
        item = response.meta['item']
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        skus = {}
        raw_json = self.raw_product(response)

        for sku in raw_json.get('skus'):
            color = sku.get('dimensions').get('Cor')
            size = sku.get('dimensions').get('Tamanho')
            skus.update({f'{color}_{size}': {
                'out_of_stock': not sku.get('available'),
                'price': sku.get('bestPrice'),
                'previous_price': sku.get('listPrice'),
                'size': size,
                'color': color,
            }})

        return skus

    def raw_product(self, response):
        return json.loads(response.css('script:contains("var skuJson_0")').re("var skuJson_0 "
                                                                              "= (.+?);")[0])

    def retailer_sku(self, response):
        raw_json = self.raw_product(response)
        if raw_json.get('productId'):
            return raw_json.get('productId')
        raise Exception('Product not available')

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

    def colour_requests(self, response):
        requests = [response.follow(response.url, callback=self.parse_color, dont_filter=True)]
        color_queue = response.css('.img-wrapper ::attr(href)').getall()

        for color_url in color_queue:
            requests.append(response.follow(color_url, callback=self.parse_color))

        return requests

    def get_image_url(self, response):
        product_id = self.retailer_sku(response)
        return self.image_url_t.format(product_id)

    def get_imagesid(self, response):
        item = response.meta['response'].meta['item']
        raw_images_json = json.loads(response.text)

        item['image_urls'].extend([self.image_t.format(i["imageId"])
                                   for i in raw_images_json[0]['items'][0]['images']])

        return self.parse_sku(response.meta['response'])

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            return request
        item.pop('requests', None)
        return item


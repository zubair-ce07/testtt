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
    listing_css = '.header_submenu_item-large'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='paginantion'),
    )
    image_url_t = 'https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:' \
                  '{}&sc=1'
    image_t = 'https://cea.vteximg.com.br/arquivos/ids/{}.jpg'

    def paginantion(self, response):
        page_count = int(
            response.css('script[type="text/javascript"]:contains("pagecount")'
                         '').re('pagecount_\d+ = (.+?);')[0])
        page_url_parameters = response.css('script[type="text/javascript"]:'
                                           'contains(".load")').re("\).load\(\'(.+?)\' +")[0]

        for page_number in range(1, page_count):
            page_url = page_url_parameters + str(page_number)
            yield response.follow(url=page_url, callback=self.parse_products)

    def parse_products(self, response):
        page_products_url = response.css('.product-details_name ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_item)
                    for url in page_products_url]

    def parse_item(self, response):
        raw_json = self.product_json(response)
        item = CeaItem()
        item['retailer_sku'] = self.retailer_sku(raw_json)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand()
        item['description'] = self.product_description(response)
        item['care'] = []
        item['skus'] = {}
        item['requests'] = self.product_requests(response, raw_json)

        yield from self.next_request_or_item(item)

    def parse_sku(self, response):
        raw_json = self.product_json(response)
        item = response.meta['item']
        for sku in raw_json.get('skus'):
            color = sku.get('dimensions').get('Cor')
            size = sku.get('dimensions').get('Tamanho')

            item['skus'].update({f'{color}_{size}': {
                'out_of_stock': not sku.get('available'),
                'price': sku.get('bestPrice'),
                'previous_price': sku.get('listPrice'),
                'size': size,
                'color': color,

            }})

        yield from self.next_request_or_item(item)

    def product_json(self, response):
        return json.loads(response.css('script:contains("var skuJson_0")').re("var skuJson_0 "
                                                                              "= (.+?);")[0])

    def retailer_sku(self, raw_json):
        return raw_json.get('productId')

    def product_name(self, response):
        return response.css('title::text').get()

    def product_gender(self, response):
        name = self.product_name(response)

        for key in self.gender_dic.keys():
            if key in name:
                return self.gender_dic.get(key)

        return 'uni-sex'

    def product_category(self, response):
        return response.css('a[property = "v:title"] ::text').getall()

    def product_url(self, response):
        return response.url

    def product_brand(self):
        return 'C&A'

    def product_description(self, response):
        return clean(response.css('.productDescription::text').get())

    def product_requests(self, response, raw_json):
        requests = [response.follow(response.url + '#', callback=self.parse_sku, meta={'raw_json'
                                                                                       '': raw_json})]
        requests.append(response.follow(url=self.get_image_url(raw_json), callback=self.get_imagesid))
        color_queue = response.css('.img-wrapper ::attr(href)').getall()

        for color_url in color_queue:
            requests.append(response.follow(color_url, callback=self.parse_sku, meta={'raw_json'
                                                                                      '': raw_json}))

        return requests

    def get_image_url(self, raw_json):
        product_id = self.retailer_sku(raw_json)
        return self.image_url_t.format(product_id)

    def get_imagesid(self, response):
        item = response.meta['item']
        raw_images_json = json.loads(response.text)
        images = []

        for i in raw_images_json[0]['items'][0]['images']:
            images.append(self.image_t.format(i["imageId"]))

        item['image_urls'] = images
        yield from self.next_request_or_item(item)

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            yield request
            return
        item.pop('requests', None)
        yield item


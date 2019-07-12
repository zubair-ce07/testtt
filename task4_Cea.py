import re
import json

import scrapy


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


def clean(raw_data):
    raw_info = ''

    if isinstance(raw_data, list):
        for string in raw_data:
            if re.sub('\s+', '', string):
                raw_info += (re.sub('\s+', '', string))

        return raw_info

    if re.sub('\s+', '', raw_data):
        return re.sub('\s+', '', raw_data)


class CeaSpider(scrapy.Spider):
    name = 'cea'
    allowed_domains = ['cea.com.br']
    start_urls = [
        'https://www.cea.com.br/',
    ]

    def parse(self, response):
        major_categories_url = response.css('.header_submenu_item-large ::attr(href)').get()

        yield from [response.follow(url=url, callback=self.extract_pages_link)
                    for url in major_categories_url]

    def extract_pages_link(self, response):

        raw_json_url = 'https://www.cea.com.br/' + \
                       response.css('script[type="text/javascript"]').re("\).load\(\'(.+?)\' +")[0]
        for page_number in range(1, 100):
            page_url = raw_json_url + str(page_number)
            yield response.follow(url=page_url, callback=self.extract_products)

    def extract_products(self, response):

        if not response.text:
            return False

        page_products_url = response.css('.product-details_name ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_item)
                    for url in page_products_url]

    def parse_item(self, response):

        item = CeaItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand()
        item['description'] = self.product_description(response)
        item['color'] = self.product_color(response)
        item['care'] = []
        item['skus'] = {}
        item['requests'] = []
        item['requests'].append(scrapy.Request(url=self.get_image_url(response), callback=self.get_imagesid))
        color_queue = response.css('.img-wrapper ::attr(href)').getall()

        for color_url in color_queue:
            item['requests'].append(response.follow(color_url, callback=self.parse_sku))

        yield from self.request_or_yield(item)

    def get_image_url(self, response):
        raw_json = response.css('script').re("var skuJson_0 = (.+?);")
        product_id = json.loads(raw_json[0]).get('productId')

        return f'https://www.cea.com.br/api/catalog_system/pub/products/search?fq=' \
            f'productId:{product_id}&sc=1'

    def retailer_sku(self, response):
        raw_json = response.css('script').re("var skuJson_0 = (.+?);")
        return json.loads(raw_json[0]).get('productId')

    def product_name(self, response):
        return response.css('title::text').get()

    def product_category(self, response):
        return response.css('a[property = "v:title"] ::text').getall()

    def product_url(self, response):
        return response.url

    def product_brand(self):
        return 'C&A'

    def product_description(self, response):
        return response.css('.productDescription::text').get()

    def product_color(self, response):
        return response.url.split('-')[-1].split('/')[0]

    def get_imagesid(self, response):
        item = response.meta['item']
        raw_images_json = json.loads(response.text)
        images = []

        for i in raw_images_json[0]['items'][0]['images']:
            images.append(f'https://cea.vteximg.com.br/arquivos/ids/{i["imageId"]}.jpg')

        item['image_urls'] = images
        yield from self.request_or_yield(item)

    def parse_sku(self, response):
        item = response.meta['item']
        sizes = self.available_sizes(response)
        color = self.color(response)
        price = self.price(response)
        previous_price = self.prev_price(response)
        raw_sku = item['skus']

        for size in sizes:
            raw_sku.update({f'{color}_{size}': {
                'color': color,
                'price': price,
                'previous_price': previous_price,
                'size': size
            }})

        item['skus'] = raw_sku
        print(item['skus'], "\n\n\n\n\n\n")
        yield from self.request_or_yield(item)

    def available_sizes(self, response):
        raw_json = response.css('script').re('var skuJson_0 = (.+?);')
        color_json = json.loads(raw_json[0])
        return color_json['dimensionsMap']['Tamanho']

    def color(self, response):
        return response.url.split('-')[-1].split('/')[0]

    def price(self, response):
        return response.css('#___rc-p-dv-id ::attr(value)').get()

    def prev_price(self, response):
        raw_json = response.css('script').re('var skuJson_0 = (.+?);')
        price_json = json.loads(raw_json[0])
        return price_json['skus'][0]['listPriceFormated']

    def request_or_yield(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            yield request
        else:
            item.pop('requests', None)
            yield item


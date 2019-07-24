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


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]

    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class CeaSpider(scrapy.Spider):
    name = 'cea'
    allowed_domains = ['cea.com.br']
    start_urls = [
        'https://www.cea.com.br/',
    ]
    raw_json_url_template = 'https://www.cea.com.br/{}'
    image_url_template = 'https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:{}&sc=1'
    image_template = 'https://cea.vteximg.com.br/arquivos/ids/{}.jpg'

    def parse(self, response):
        listing_urls = response.css('.header_submenu_item-large ::attr(href)').get()
        yield from [response.follow(url=url, callback=self.paginantion)
                    for url in listing_urls]

    def paginantion(self, response):
        page_count = int(response.css('script[type="text/javascript"]').re('pagecount_\d+ = (.+?);')[0])
        page_url_parameters = response.css('script[type="text/javascript"]').re("\).load\(\'(.+?)\' +")[0]

        for page_number in range(1, page_count):
            page_url = self.raw_json_url_template.format(page_url_parameters) + str(page_number)
            yield response.follow(url=page_url, callback=self.parse_products)

    def parse_products(self, response):
        page_products_url = response.css('.product-details_name ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_item)
                    for url in page_products_url]

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
        item['skus'] = {}
        item['requests'] = self.product_requests(response)

        yield from self.next_request_or_item(item)

    def retailer_sku(self, response):
        raw_json = response.css('script').re("var skuJson_0 = (.+?);")
        return json.loads(raw_json[0]).get('productId')

    def product_name(self, response):
        return response.css('title::text').get()

    def product_gender(self, response):
        if self.product_name(response).find('Mascu') != -1:
            return 'men'
        if self.product_name(response).find('Femin') != -1:
            return 'women'
        if self.product_name(response).find('Infantil') != -1:
            return 'kids'

        return 'unisex'

    def product_category(self, response):
        return response.css('a[property = "v:title"] ::text').getall()

    def product_url(self, response):
        return response.url

    def product_brand(self):
        return 'C&A'

    def product_description(self, response):
        return clean(response.css('.productDescription::text').get())

    def product_requests(self, response):
        requests = [response.follow(response.url + '/#', callback=self.parse_sku)]
        requests.append(response.follow(url=self.get_image_url(response), callback=self.get_imagesid))
        color_queue = response.css('.img-wrapper ::attr(href)').getall()

        for color_url in color_queue:
            requests.append(response.follow(color_url, callback=self.parse_sku))

        return requests

    def get_image_url(self, response):
        raw_json = response.css('script').re("var skuJson_0 = (.+?);")
        product_id = json.loads(raw_json[0]).get('productId')
        return self.image_url_template.format(product_id)

    def get_imagesid(self, response):
        item = response.meta['item']
        raw_images_json = json.loads(response.text)
        images = []

        for i in raw_images_json[0]['items'][0]['images']:
            images.append(self.image_template.format(i["imageId"]))

        item['image_urls'] = images
        yield from self.next_request_or_item(item)

    def parse_sku(self, response):
        item = response.meta['item']
        sizes = self.sizes(response)
        color = self.color(response)
        price = response.css('#___rc-p-dv-id ::attr(value)').get()
        previous_price = self.prev_price(response)

        for size in sizes:
            item['skus'].update({f'{color}_{size}': {
                'color': color,
                'price': price,
                'previous_price': previous_price,
                'size': size
            }})

        yield from self.next_request_or_item(item)

    def sizes(self, response):
        raw_json = response.css('script').re('var skuJson_0 = (.+?);')
        color_json = json.loads(raw_json[0])
        return color_json.get('dimensionsMap', {}).get('Tamanho', {}) or ['OneSize']

    def color(self, response):
        color = response.url.split('-')[-1].split('/')[0]
        if not color.isdigit():
            return color

        return 'OneColor'

    def prev_price(self, response):
        raw_json = response.css('script').re('var skuJson_0 = (.+?);')
        price_json = json.loads(raw_json[0])
        return price_json.get('skus', {})[0].get('listPriceFormated')

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            yield request
            return
        item.pop('requests', None)
        yield item

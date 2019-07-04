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


class CeaSpider(scrapy.Spider):
    name = 'cea'
    allowed_domains = ['cea.com.br']
    start_urls = [
        'https://www.cea.com.br',
    ]

    def parse(self, response):
        major_categories_url = self.get_home_page_data(response)
        yield from [response.follow(url=url, callback=self.generate_page_links)
                    for url in major_categories_url]

    def generate_page_links(self, response):
        raw_json_url = 'https://www.cea.com.br/' + \
                       re.findall("\).load\(\'(.+?)\' +", response.body.decode('utf-8'), re.S)[0]

        for page_number in range(1, 100):
            if response.folow(url=raw_json_url + str(page_number), callback=self.extract_products):
                break

    def extract_products(self, response):

        if not response.text:
            return 0

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
        item['care'] = []
        item['color'] = self.product_color(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        yield item

    def product_brand(self):
        return 'C&A'

    def retailer_sku(self, response):
        raw_json = re.findall("var skuJson_0 = (.+?);", response.body.decode('utf-8'), re.S)
        return json.loads(raw_json[0]).get('productId')

    def product_skus(self, response):
        return re.findall("var skuJson_0 =(.+?);\n", response.body.decode('utf-8'), re.S)

    def product_color(self, response):
        return response.url.split('-')[-1].split('/')[0]

    def product_description(self, response):
        return response.css('.productDescription::text').get()

    def product_url(self, response):
        return response.url

    def product_category(self, response):
        return response.css('a[property = "v:title"] ::text').getall()

    def product_name(self, response):
        return response.css('title::text').get()

    def get_imagesid(self, response):
        raw_images_json = json.loads(response.text)
        return [raw_images_json[0]['items'][0]['images'][image_number]['imageId']
                for image_number in range(0, 4)]

    def get_home_page_data(self, response):

        yield from [category.css('::attr(href)').get()
                    for category in response.css('.header_submenu_item')
                    if category.css('::text').get()[1:] in 'er tudo']

    def get_last_page(self, response):
        return int(response.css('.navigation-pages_link--last ::text').get()) + 1

    def images_url(self, response):
        raw_json = re.findall("var skuJson_0 = (.+?);", response.body.decode('utf-8'), re.S)
        product_id = json.loads(raw_json[0]).get('productId')
        raw_images_url = f'https://www.cea.com.br/api/catalog_system/pub/products/search?fq=' \
            f'productId:{product_id}&sc=1'
        images_id = yield response.follow(url=raw_images_url, callback=self.get_imagesid)

        images_url = []
        for id in images_id:
            images_url.append(f'https://cea.vteximg.com.br/arquivos/ids/{id}.jpg')

        return images_url


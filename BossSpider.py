import re

import json
import scrapy


class BossItem(scrapy.Item):
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
    price = scrapy.Field()
    skus = scrapy.Field()


class BossSpider(scrapy.Spider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home',
    ]

    def parse(self, response):
        major_categories_url = self.get_home_page_catg(response)

        for url in major_categories_url:
            yield response.follow(url=url, callback=self.extract_products)

    def extract_products(self, response):
        page_products_url = response.css('.product-tile__link ::attr(href)').getall()

        for url in page_products_url:
            yield response.follow(url=url, callback=self.parse_item)

    def parse_item(self, response):

        item = BossItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        yield item

    def get_home_page_catg(self, response):
        return response.css('.font__copy ::attr(href)').getall()

    def retailer_sku(self, response):
        return re.findall("productSku\":\"(.+?)\"", response.body.decode('utf-8'), re.S)[0]

    def product_gender(self, response):
        return re.findall("productGender\":\"(.+?)\"", response.body.decode('utf-8'), re.S)[0]

    def product_name(self, response):
        return response.css('.font__h2 ::text').get()

    def product_category(self, response):
        return response.css('.breadcrumb__title ::text').getall()[1:4]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('meta[itemprop= "brand"] ::attr(content)').get()

    def product_description(self, response):
        return self.clean_text(response.css('.description div ::text').get())

    def product_care(self, response):
        return response.css('.accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

    def product_skus(self, response):
        previous_price = {'prev_price': response.css('s ::text').get()}
        sku_json = json.loads(re.findall("dataLayer.push\((.+?)\);", response.body.decode('utf-8'), re.S)[0])
        sku_json.update(previous_price)

        return sku_json

    def clean_text(self, text):
        clean_text = re.sub('\s+', '', text)

        if clean_text:
            return clean_text

        return 0

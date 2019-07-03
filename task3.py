import re

import scrapy


class AsicsItem(scrapy.Item):
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


class AsicsSpider(scrapy.Spider):
    name = "asics"
    allowed_domains = ['asics.com']
    start_urls = [
        'https://www.asics.com/us/en-us/',
    ]

    def parse(self, response):

        for major_category in response.css('.childlink-wrapper > ::attr(href)').getall():
            category_url = response.urljoin(major_category)
            yield scrapy.Request(url=category_url, callback=self.extract_page_products)

    def extract_page_products(self, response):

        for product in response.css('.prod-wrap  > ::attr(href)').getall():
            product_url = response.urljoin(product)
            yield scrapy.Request(url=product_url, callback=self.extract_product_details)

        next_page = self.next_page_url(response)
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.extract_page_products)

    def extract_product_details(self, response):

        item = AsicsItem()
        item['retailer_sku'] = self.product_sku(response)
        item['name'] = self._name(response)
        item['gender'] = self.gender(response)
        item['category'] = self.category(response)
        item['url'] = self.product_url(response)
        item['description'] = self.description(response)
        item['image_urls'] = self.image_urls(response)
        currency = self.currency(response)
        price = self.price(response)
        color = self.get_color(response)

        item['care'] = []
        item['brand'] = "ASICS"
        item['skus'] = self.sku_record(response, color, currency, price)
        yield item

    def next_page_url(self, response):
        return response.css('rightArrow ::attr(href)').get()

    def size(self, response):
        return response.css('.SizeOption::text').getall()

    def _name(self, response):
        return response.css('title::text').get().split('|')[0].strip()

    def gender(self, response):
        return response.css('title::text').get().split('|')[1].strip()

    def category(self, response):
        return response.css('.breadcrumb > ::text ').getall()

    def product_url(self, response):
        return response.url

    def description(self, response):
        raw_descriptions = response.css('.tabInfoChildContent::text').getall()
        return self.clean_description(raw_descriptions)

    def clean_description(self, raw_descriptions):
        for description in raw_descriptions:
            if re.sub('\s+', '', description):
                return re.sub('\s+', '', description)

    def image_urls(self, response):
        return response.css('.owl-carousel > ::attr(data-big)').getall()

    def currency(self, response):
        return response.css('.inStock > meta[itemprop="priceCurrency"] ::attr(content)').get()

    def price(self, response):
        return response.css('.inStock > meta[itemprop="price"] ::attr(content)').get()

    def product_sku(self, response):
        return response.css('.inStock > meta[itemprop="sku"] ::attr(content)').get()

    def get_color(self, response):
        return response.css('title::text').get().split('|')[2]

    def sku_record(self, response, color, currency, price):
        skus = []

        for sku in response.css('.size-box-select-container .size-select-list'):
            single_sku = {
                sku.css('::attr(data-value)').get():
                    {
                        'color': color,
                        'currency': currency,
                        'price': price,
                        'size': self.size(sku)
                    }
            }
            skus.append(single_sku)

        return skus


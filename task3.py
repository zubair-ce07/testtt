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
        home_page = response.css('.childlink-wrapper > ::attr(href)').getall()

        for category_url in home_page:
            category_url = response.urljoin(category_url)
            yield scrapy.Request(url=category_url, callback=self.extract_page_products)

    def extract_page_products(self, response):
        page_products = response.css('.prod-wrap  > ::attr(href)').getall()

        for product in page_products:
            product_url = response.urljoin(product)
            yield scrapy.Request(url=product_url, callback=self.parse_item)

        next_page = response.css('rightArrow ::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.extract_page_products)

    def parse_item(self, response):
        item = AsicsItem()
        item['retailer_sku'] = self.product_id(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.gender(response)
        item['category'] = self.category(response)
        item['url'] = self.product_url(response)
        item['description'] = self.description(response)
        item['image_urls'] = self.image_urls(response)
        item['care'] = []
        item['brand'] = "ASICS"
        item['skus'] = self.sku_record(response)

        yield item

    def size(self, response):
        return response.css('.SizeOption::text').getall()

    def product_name(self, response):
        return self.clean_text(response.css('title::text').get().split('|')[0])

    def gender(self, response):
        return self.clean_text(response.css('title::text').get().split('|')[1])

    def category(self, response):
        return response.css('.breadcrumb > ::text ').getall()

    def product_url(self, response):
        return response.url

    def description(self, response):
        raw_descriptions = response.css('.tabInfoChildContent::text').getall()

        for description in raw_descriptions:
            if self.clean_text(description):
                return self.clean_text(description)

    def image_urls(self, response):
        return response.css('.owl-carousel > ::attr(data-big)').getall()

    def product_id(self, response):
        return response.css('.inStock > meta[itemprop="sku"] ::attr(content)').get()

    def sku_record(self, response):
        currency = response.css('.inStock > meta[itemprop="priceCurrency"] '
                                '::attr(content)').get()
        price = response.css('.inStock > meta[itemprop="price"] '
                             '::attr(content)').get()
        color = response.css('title::text').get().split('|')[2]
        prev_price = response.css('.pull-right del::text').getall()

        skus = []

        for sku in response.css('.size-box-select-container .size-select-list'):
            single_sku = {
                sku.css('::attr(data-value)').get():
                    {
                        'color': color,
                        'currency': currency,
                        'price': price,
                        'size': self.size(sku),
                        'previous_price' : prev_price
                    }
            }
            skus.append(single_sku)

        return skus

    def clean_text(self,text):
        clean_text = re.sub('\s+', '', text)

        if clean_text:
            return clean_text

        return 0


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
    skus = scrapy.Field()


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


class AsicsSpider(scrapy.Spider):
    name = 'asics'
    allowed_domains = ['asics.com']
    start_urls = [
        'https://www.asics.com/us/en-us/',
    ]

    def parse(self, response):
        listing_urls = response.css('.childlink-wrapper ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_category)
                    for url in listing_urls]

    def parse_category(self, response):
        product_urls = response.css('.prod-wrap ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_item)
                    for url in product_urls]

        next_page = response.css('rightArrow ::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_category)

    def parse_item(self, response):
        item = AsicsItem()
        item['retailer_sku'] = self.product_id(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['description'] = self.product_description(response)
        item['image_urls'] = self.image_urls(response)
        item['care'] = []
        item['brand'] = self.product_brand()
        item['skus'] = self.product_skus(response)

    def product_id(self, response):
        return response.css('.inStock meta[itemprop="sku"] ::attr(content)').get()

    def product_name(self, response):
        return self.clean_text(response.css('title ::text').get().split('|')[0])

    def product_gender(self, response):
        return response.css('script[type="text/javascript"]').re('\"gender\":\"(.+?)\"')[0]

    def product_category(self, response):
        return response.css('.breadcrumb ::text').getall()

    def product_url(self, response):
        return response.url

    def product_description(self, response):
        raw_descriptions = response.css('.tabInfoChildContent ::text').getall()
        return clean(raw_descriptions)

    def image_urls(self, response):
        return response.css('.owl-carousel ::attr(data-big)').getall()

    def product_brand(self):
        return 'ASICS'

    def product_skus(self, response):
        currency = response.css('.inStock meta[itemprop="priceCurrency"]'
                                '::attr(content)').get()
        price = response.css('.inStock meta[itemprop="price"]'
                             '::attr(content)').get()
        color = response.css('title ::text').get().split('|')[2]
        prev_price = response.css('.pull-right del ::text').getall()

        skus = []

        for sku_sel in response.css('.size-box-select-container .size-select-list'):
            single_sku = {
                sku_sel.css('::attr(data-value)').get():
                    {
                        'sku_id': f'{color} _ {self.size(sku_sel)}',
                        'color': color,
                        'currency': currency,
                        'price': price,
                        'size': self.size(sku_sel),
                        'previous_price': prev_price
                    }
            }
            skus.append(single_sku)

        return skus

    def size(self, response):
        if response.css('.SizeOption::text').getall():
            return response.css('.SizeOption::text').getall() or ['One_Size']

    def clean_text(self, text):
        clean_text = re.sub('\s+', '', text)

        if clean_text:
            return clean_text


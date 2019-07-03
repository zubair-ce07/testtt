import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MySpider(CrawlSpider):

    name = 'Derekrose'
    start_urls = ['https://www.derek-rose.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=('.global-nav .global-nav__item[data-nav="mens"]'), \
                           deny=('/men/clothing/accessories') ),follow=True),
        Rule(LinkExtractor(restrict_css=('.category-products'), ), callback='main_function'),
    )

    def main_function(self, response):
        item = DerekRecord()

        item['product_name'] = self.product_name(response)
        item['brand_name'] = self.brand_name(response)
        item['price'] = self.price(response)
        item['details_and_care'] =self.details_and_care(response)
        item['skus'] = self.skus(response)
        item['image_urls'] = self.image_urls(response)
        item['category'] = self.category(response)
        item['gender'] = self.gender(response)
        item['description'] = self.description(response)

        return item

    def price(self, response):
        converted_price = response.css('span.price::text').get()
        converted_price = converted_price[1:]
        converted_price = float(converted_price) * 100

        return converted_price


    def product_name(self, response):
        return response.css('h1.product-details__sub::text').get(),

    def skus(self, response):
          return response.css('.product-details__sku::text').get(),

    def description(self, response):
            return response.css(
                'div.product-details__main-description p::text').getall(),
    def brand_name(self, response):
            return response.css('.store-popup__header::text').get().split()[2] + \
                          response.css('.store-popup__header::text').get().split()[3]

    def image_urls(self, response):
        Links = []

        for link in response.css('.media-extra__item'):
            image_urls = link.css('.media-extra__item img::attr(srcset)').get().split()[18]
            Links.append(image_urls)

        return Links

    def category(self, response):
        return response.css('h1.product-details__sub::text').get().split()[-1]

    def gender(self, response):
        return response.css('h1.product-details__sub::text').get().split()[0]

    def details_and_care(self, response):
        description = {}

        properties = response.css('.product-details__attrs tr th::text').getall()
        values = response.css('.product-details__attrs tr td::text').getall()

        for index in range(0, len(properties) - 1):
            description[properties[index]] = values[index]

        return description,


class DerekRecord(scrapy.Item):

    product_name = scrapy.Field()
    brand_name = scrapy.Field()
    image_urls = scrapy.Field()
    details_and_care = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()



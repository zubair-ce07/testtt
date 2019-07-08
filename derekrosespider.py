import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class DerekRose(CrawlSpider):

    name = 'Derekrose'
    start_urls = ['https://www.derek-rose.com/']
    listing_css_first = '.global-nav .global-nav__item[data-nav="mens"]'
    listing_css_second = '.category-products'

    rules = (
        Rule(LinkExtractor(allow=(), deny=(), restrict_css=listing_css_first)),
        Rule(LinkExtractor(allow=(), deny=(), restrict_css=listing_css_second), callback='parse_item')
    )

    def parse_item(self, response):
        item = DerekRecord()

        item['product_name'] = self.get_product_name(response)
        item['brand_name'] = self.get_brand_name(response)
        item['price'] = self.get_price(response)
        item['details_and_care'] = self.get_details_and_care(response)
        item['skus'] = self.get_skus(response)
        item['image_urls'] = self.get_image_urls(response)
        item['gender'] = self.get_gender(response)
        item['description'] = self.get_description(response)
        item['product_url'] = self.get_product_url(response)

        return item

    def get_price(self, response):
        price = response.css('span.price::text').get()
        raw_prices = price_digits = [str(elem) for elem in price if elem.isdigit()]
        return int(''.join(raw_prices)) * 100

    def get_product_name(self, response):
        return response.css('h1.product-details__sub::text').get()

    def get_skus(self, response):
        return response.css('.product-details__sku::text').get()

    def get_description(self, response):
        return response.css('div.product-details__main-description p::text').getall()

    def get_brand_name(self, response):
        return response.css('.brand--is-large .brand__link::text').get().strip()

    def get_image_urls(self, response):
        image_urls = []

        for link in response.css('.media-extra__item'):
            image_url = link.css('.media-extra__item img::attr(srcset)').get().split()[18]
            image_urls.append(image_url)

        return image_urls

    def get_gender(self, response):
        return response.css('.global-nav .global-nav__item a::attr(data-goto)').get()

    def get_details_and_care(self, response):
        description = {}

        properties = response.css('.product-details__attrs tr th::text').getall()
        values = response.css('.product-details__attrs tr td::text').getall()

        for index in range(0, len(properties) - 1):
            description[properties[index]] = values[index]

        return description,

    def get_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()


class DerekRecord(scrapy.Item):

    product_name = scrapy.Field()
    brand_name = scrapy.Field()
    image_urls = scrapy.Field()
    details_and_care = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    product_url = scrapy.Field()

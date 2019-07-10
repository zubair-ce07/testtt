import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime


class BognerUK(CrawlSpider):

    name = 'Bognerspider'
    start_urls = ['https://www.bogner.com/en-gb/']
    listing_css = '.level0 .level0 a[href*="/en-gb/men"]'
    product_css= '.category-products'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        item = BognerRecord()

        item['name'] = self.get_product_name(response)
        item['retailer_skus'] = self.get_product_skus(response)
        item['size'] = self.get_product_size(response)
        item['description'] = self.get_product_description(response)
        item['market'] = self.get_product_market(response)
        item['care'] = self.get_product_care(response)
        item['image_urls'] = self.get_product_image_urls(response)
        item['crawl_start_time'] = self.get_crawl_start_time(response)
        item['currency'] = self.get_product_currency(response)
        item['url'] = self.get_product_url(response)
        item['category'] = self.get_product_category(response)
        item['brand'] = self.get_product_brand_name(response)

        return item

    def get_product_name(self,response):
        return response.css('.product-name-text::text').get()

    def get_product_skus(self,response):
        return response.css('.sku::text').get()

    def get_product_price(self, response):
        price = response.css('.product-sizes .size-box::attr(data-size-label)').get()
        raw_prices = [str(elem) for elem in price if elem.isdigit()]

        return int(''.join(raw_prices)) * 100

    def get_product_size(self, response):
        return response.css('.product-sizes .size-box::attr(data-size-label)').get()

    def get_product_description(self, response):
        return response.css('.std p::text').get()

    def get_product_details(self, response):
        return response.css('.tab-target .product-features ul li::text').getall()

    def get_product_market(self,response):
        return response.css('.country-icon .header-label::text').get()

    def get_product_care(self, response):
        return response.css('.material-care-tip .carelabel-list li p::text').getall()

    def get_product_image_urls(self, response):
        return response.css('.product-view .view-gallery-item img::attr(data-src)').getall()

    def get_crawl_start_time(self, response):
        return datetime.utcnow()

    def get_product_currency(self, response):
        return response.css('.sizebox-wrapper::attr(data-currency)').get()

    def get_product_url(self, response):
        return response.css("link[rel='canonical']::attr(href)").get()

    def get_product_category(self, response):
        return response.css('.main .breadcrumbs li a::attr(title)').getall()

    def get_product_brand_name(self, response):
        return response.css('.collection-name::text').get()


class BognerRecord(scrapy.Item):

    name = scrapy.Field()
    retailer_skus = scrapy.Field()
    size = scrapy.Field()
    description = scrapy.Field()
    market = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    crawl_start_time = scrapy.Field()
    currency = scrapy.Field()
    url =scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()


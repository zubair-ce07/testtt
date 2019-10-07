import re
import scrapy

from ..items import Task2BeyondlimitsItem

def get_retailor_sku(response):
    return response.css('[itemprop="productID"]::text').get()

def get_url(response):
    return response.url

def get_gender(response):
    return re.search(r'(?<=/)(Wo|wo)?(M|m)en?(?=/)', response.url).group()

def get_category(response):
    return re.search(r'(?<=.com/).+(?=/)', response.url).group()

def get_brand(response):
    return response.css('[property="og:site_name"]::attr(content)').get()

def get_name(response):
    return response.css(".bb_art--title::text").get()

def get_description(response):
    return response.css('#description p::text').get()

def get_care(response):
    return response.css('#description ul li::text')[1].get()

def get_img_urls(response):
    return response.css(".bb_pic--nav li a::attr(href)").getall()

def get_skus(response):
    colour = response.css('#description ul li::text')[0].get().split(': ', 1)[1]
    price = response.css('[itemprop="price"]::attr(content)').get()
    currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
    previous_prices = response.css('.oldPrice del::text').get()
    sizes = response.css('#bb-variants--0 option')
    return [{'colour': colour, 'price': price, 'currency': currency, 'previous_prices': previous_prices,
      'size': size.css("option::text").get(), 'sku_id': colour + "_" + size.css("option::text").get()}
     for size in sizes if size.css("option::attr(value)").get()]

class BeyondLimitsSpider(scrapy.Spider):
    name = "beyondlimits"
    start_urls = [
        'https://www.beyondlimits.com/',
    ]

    def parse(self, response):
        for category in response.css('.bb_mega--link.bb_catnav--link::attr(href)'):
            yield response.follow(category.get(), callback=self.category_page_parse)

    def category_page_parse(self, response):
        for detail_url in response.css('.bb_product--link.bb_product--imgsizer::attr(href)'):
            yield response.follow(detail_url.get(), callback=self.details_page_parse)

    def details_page_parse(self, response):
        product_details = Task2BeyondlimitsItem()
        product_details['retailer_sku'] = get_retailor_sku(response)
        product_details['url'] = get_url(response)
        product_details['gender'] = get_gender(response)
        product_details['category'] = get_category(response)
        product_details['brand'] = get_brand(response)
        product_details['name'] = get_name(response)
        product_details['description'] = get_description(response)
        product_details['care'] = get_care(response)
        product_details['img_urls'] = get_img_urls(response)
        product_details['skus'] = get_skus(response)

        yield product_details



import scrapy


class Task2BeyondlimitsItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    img_urls = scrapy.Field()
    skus = scrapy.Field()

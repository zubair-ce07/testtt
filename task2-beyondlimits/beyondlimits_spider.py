import re
import scrapy

from ..items import Task2BeyondlimitsItem

class QuotesSpider(scrapy.Spider):
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
        product_details['retailer_sku'] = response.css('[itemprop="productID"]::text').get()
        product_details['url'] = response.url
        product_details['gender'] = re.search(r'(?<=/)(Wo|wo)?(M|m)en?(?=/)', response.url).group()
        product_details['category'] = re.search(r'(?<=.com/).+(?=/)', response.url).group()
        product_details['brand'] = response.css('[property="og:site_name"]::attr(content)').get()
        product_details['name'] = response.css(".bb_art--title::text").get()
        product_details['description'] = response.css('#description p::text').get()
        product_details['care'] = response.css('#description ul li::text')[1].get()
        product_details['img_urls'] = response.css(".bb_pic--nav li a::attr(href)").getall()
        colour = response.css('#description ul li::text')[0].get().split(': ', 1)[1]
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_prices = response.css('.oldPrice del::text').get()
        sizes = response.css('#bb-variants--0 option')
        product_details['skus'] = \
            [{'colour': colour, 'price': price, 'currency': currency, 'previous_prices': previous_prices,
              'size': size.css("option::text").get(), 'sku_id': colour + "_" + size.css("option::text").get()}
             for size in sizes if size.css("option::attr(value)").get()]
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

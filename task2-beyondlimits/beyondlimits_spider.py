import re
import scrapy

from ..items import DetailsItems


class BeyondLimitsExtractor:
    def extract_retailor_sku(self, response):
        return response.css('[itemprop="productID"]::text').get()

    def extract_url(self, response):
        return response.url

    def extract_gender(self, response):
        return re.search(r'(?<=/)(Wo|wo)?(M|m)en?(?=/)', response.url).group()

    def extract_category(self, response):
        return re.search(r'(?<=.com/).+(?=/)', response.url).group()

    def extract_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def extract_name(self, response):
        return response.css(".bb_art--title::text").get()

    def extract_description(self, response):
        return response.css('#description p::text').get()

    def extract_care(self, response):
        return response.css('#description ul li::text')[1].get()

    def extract_img_urls(self, response):
        return response.css(".bb_pic--nav li a::attr(href)").getall()

    def extract_skus(self, response):
        colour = response.css('#description ul li::text')[0].get().split(': ', 1)[1]
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_prices = response.css('.oldPrice del::text').get()
        sizes = response.css('#bb-variants--0 option')
        return [{'colour': colour, 'price': price, 'currency': currency, 'previous_prices': previous_prices,
                 'size': size.css("option::text").get(), 'sku_id': colour + "_" + size.css("option::text").get()} 
                for size in sizes if size.css("option::attr(value)").get()]


class CrawlSpider(scrapy.Spider):
    name = "beyondlimits"
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/',
    ]

    def parse(self, response):
        for category in response.css('.bb_mega--link.bb_catnav--link::attr(href)'):
            yield response.follow(category.get(), callback=self.parse_category)

    def parse_category(self, response):
        for detail_url in response.css('.bb_product--link.bb_product--imgsizer::attr(href)'):
            yield response.follow(detail_url.get(), callback=self.parse_details)

    def parse_details(self, response):
        product_details = DetailsItems()
        details_extractor = BeyondLimitsExtractor()
        product_details['retailer_sku'] = details_extractor.extract_retailor_sku(response)
        product_details['url'] = details_extractor.extract_url(response)
        product_details['gender'] = details_extractor.extract_gender(response)
        product_details['category'] = details_extractor.extract_category(response)
        product_details['brand'] = details_extractor.extract_brand(response)
        product_details['name'] = details_extractor.extract_name(response)
        product_details['description'] = details_extractor.extract_description(response)
        product_details['care'] = details_extractor.extract_care(response)
        product_details['img_urls'] = details_extractor.extract_img_urls(response)
        product_details['skus'] = details_extractor.extract_skus(response)

        yield product_details


class DetailsItems(scrapy.Item):
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



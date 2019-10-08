import re
import unicodedata

from scrapy.spiders import CrawlSpider

from ..items import BeyondLimitItem


class BeyondLimitsExtractor:
    def parse_details(self, response):
        product_details = BeyondLimitItem()

        product_details['retailer_sku'] = self.extract_retailor_sku(response)
        product_details['url'] = self.extract_url(response)
        product_details['gender'] = self.extract_gender(response)
        product_details['category'] = self.extract_category(response)
        product_details['brand'] = self.extract_brand(response)
        product_details['name'] = self.extract_name(response)
        product_details['description'] = self.extract_description(response)
        product_details['care'] = self.extract_care(response)
        product_details['img_urls'] = self.extract_img_urls(response)
        product_details['skus'] = self.extract_skus(response)

        yield product_details

    def extract_retailor_sku(self, response):
        return response.css('[itemprop="productID"]::text').get()

    def extract_url(self, response):
        return response.url

    def extract_gender(self, response):
        return re.search(r'(?<=/)(Wo|wo)?(M|m)en?(?=/)', response.url).group()

    def extract_category(self, response):
        categories = response.css('.bb_breadcrumb--inner span a ::text').getall()
        return [category.strip() for category in categories if category.strip() != 'Home' and category.strip()]

    def extract_brand(self, response):
        return response.css('[property="og:site_name"]::attr(content)').get()

    def extract_name(self, response):
        return response.css(".bb_art--title::text").get()

    def extract_description(self, response):
        return response.css('#description p::text').getall()

    def extract_care(self, response):
        return response.css('#description ul li::text')[1].getall()

    def extract_img_urls(self, response):
        return response.css(".bb_pic--nav li a::attr(href)").getall()

    def extract_skus(self, response):
        colour = response.css('#description ul li::text')[0].get().split(': ', 1)[1]
        price = response.css('[itemprop="price"]::attr(content)').get()
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        previous_prices = response.css('.oldPrice del::text').get()
        if previous_prices:
            previous_prices = unicodedata.normalize('NFKD', previous_prices).encode('ascii', 'ignore').split()
        sizes = response.css('#bb-variants--0 option')
        skus = []
        for size in sizes:
            if size.css("option::attr(value)").get():
                skus.append({'colour': colour, 'price': price, 'currency': currency, 'previous_prices': previous_prices,
                             'size': size.css("option::text").get(),
                             'sku_id': colour + "_" + size.css("option::text").get()})
        return skus


class BeyondLimitsSpider(CrawlSpider):
    name = "beyondlimits"
    allowed_domains = ['beyondlimits.com']
    start_urls = [
        'https://www.beyondlimits.com/',
    ]

    def parse(self, response):
        for category in response.css('.bb_mega--link.bb_catnav--link::attr(href)'):
            yield response.follow(category.get(), callback=self.parse_category)

    def parse_category(self, response):
        details_extractor = BeyondLimitsExtractor()
        for detail_url in response.css('.bb_product--link.bb_product--imgsizer::attr(href)'):
            yield response.follow(detail_url.get(), callback=details_extractor.parse_details)



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



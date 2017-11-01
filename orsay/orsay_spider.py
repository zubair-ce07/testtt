import scrapy
import re
from tutorial.items import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class OrseySpider(CrawlSpider):
    # name of spider
    name = 'orsay'

    # list of allowed domains
    allowed_domains = ['orsay.com']
    # starting url
    start_urls = ['http://www.orsay.com/de-de/']
    # location of csv file
    custom_settings = {'FEED_URI': 'tmp/orsay.json'}

    rules = [Rule(LinkExtractor(restrict_css=".nav-container"), follow=True),
             Rule(LinkExtractor(restrict_css="li.next"), follow=True),
             Rule(LinkExtractor(restrict_css=".product-image-wrapper"), callback="parse_product_page")]

    def parse_product_page(self, response):
        # Extract product information

        product = Item()
        product['brand'] = 'Orsay'
        product['description'] = self.get_product_description(response)
        product['url'] = response.url
        product['gender'] = 'girls'
        product['name'] = self.get_product_name(response)
        product['category'] = self.get_product_category(response)
        product['skus'] = self.get_skus(response)
        product['image_urls'] = self.get_product_images(response)
        product['care'] = self.get_product_care(response)
        product['id'] = self.get_product_id(response)

        yield product

    def get_skus(self, response):
        skus = {}
        sizes = self.get_product_sizes(response)
        colors = self.get_product_colors(response)
        availability = self.get_product_availabilty(response)

        for item in zip(sizes, availability):
            for color in colors:
                key = color + '_' + item[0]
                skus[key] = {}
                skus[key]['color'] = color
                skus[key]['price'] = self.get_product_price(response)
                skus[key]['size'] = item[0]
                skus[key]['currency'] = 'EUR'
                skus[key]['availability'] = item[1]

        return skus

    def get_product_name(self, response):
        name = response.css('.product-name::text').extract_first().strip()
        return name

    def get_product_description(self, response):
        description = response.css('.description::text').extract_first().strip().split(sep='.')
        return description

    def get_product_category(self, response):
        breadcrumbs = response.css('ul.breadcrumbs')
        category = breadcrumbs.css('a::text').extract()
        return category

    def get_product_id(self, response):
        # id = response.css('.sku::text').extract()
        id_url = re.search(".*(\d{8}).html", response.url)
        id = id_url.group(1)
        return id

    def get_product_images(self, response):
        images = response.css('[data-zoom-id=mainZoom]::attr(href)').extract()
        return images

    def get_product_care(self, response):
        care = response.css('.material::text').extract()
        return care

    def get_product_price(self, response):
        price = response.css('.price::text').extract_first()
        return price

    def get_product_sizes(self, response):
        ul = response.css('.sizebox-wrapper > ul')
        sizes = ul.css('li::text').extract()
        size = []
        for s in sizes:
            if s.strip() == "":
                pass
            else:
                size.append(s.strip())

        return size

    def get_product_availabilty(self, response):
        ul = response.css('.sizebox-wrapper > ul')
        availability = ul.css('li::attr(class)').extract()
        avail = []
        for a in availability:
            boolean_value = 'unavailable' in a
            avail.append(not boolean_value)

        return avail

    def get_product_colors(self, response):
        color_info = response.css('.product-colors')
        colors = response.css('ul.product-colors > li > a > img::attr(title)').extract()
        color_urls = color_info.css('a::attr(href)').extract()
        # colors = color_info.css('img::attr(title)').extract()
        return colors

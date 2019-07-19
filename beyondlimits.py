import scrapy

from scrapy import Spider
from scrapy_spider.items import BeyondLimitItem
from datetime import datetime


class CrawlSpider(Spider):
    name = 'beyondlimitspider'
    allowed_domains = ['beyondlimits.com']
    start_urls = ['https://www.beyondlimits.com/Sales/Men/#bb_artlist',
                  'https://www.beyondlimits.com/Sales/Women/']

    def get_product_name(self, response):
        return response.css('header > h1::text').extract_first()

    def get_product_gender(self, response):
        return response.css('a > strong::text').extract_first()

    def get_product_description(self, response):
        return response.css(' header > p::text').extract_first()

    def get_retailer_sku(self, response):
        return response.css('header > small > span::text').extract_first()

    def get_image_urls(self, response):
        product_images = response.css('ul a::attr(href)').extract()
        return [image for image in product_images if 'jpg' in image]

    def get_product_care(self, response):
        product_care = response.css('#description > ul > li::text').extract()
        if product_care:
            del[product_care[0]]
        return product_care

    def get_product_color(self, response):
        product_color = response.css('#description > ul > li::text').extract_first()
        if product_color:
            filtered_color = product_color.split()
            return filtered_color[1]

    def get_product_url(self, response):
        return response.css('div > a.flag.en.selected::attr(href)').extract_first()

    def get_language(self, response):
        return response.css('a.flag.en.selected::attr(title)').extract_first()

    def get_product_brand(self, response):
        return response.css('a > img::attr(title)').extract_first()

    def get_product_category(self, response):
        return response.css('a > strong::text').extract_first()

    def get_crawl_start_time(self):
        return datetime.now()

    def get_unix_time(self):
        return datetime.timestamp(datetime.now())

    def get_product_sku(self, response):
        size_id = {'S': 1, 'M': 2, 'L': 3, 'XL': 4, 'XXL': 5}
        sku = []
        product_size = response.css('option::text').getall()
        if product_size:
            del[product_size[0]]
            product_price_currency = response.css('.price span::text').get()
            price_currency = product_price_currency.split(" ")
            product_sku = response.css('small > span::text').get()
            for sizes in product_size:
                sku_num = int(product_sku[3:]) + size_id[sizes]
                current_sku = {"price": price_currency[0], "currency": price_currency[1],
                               "sku": sizes, "skuid": str(product_sku[:3]) + str(sku_num)}
                sku.append(current_sku)
        return sku

    def get_crawl_id(self, response):
        return f"{self.name}-{self.get_language(response)}-{datetime.now().replace(second=0, microsecond=0)}" \
               f"-{datetime.timestamp(datetime.now().replace(second=0, microsecond=0))}"

    def parse(self, response):
        links = response.css('div.pictureBox.gridPicture.bb_product--imgwrap > a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_of_clothing_item)
        next_page = response.css('a.bb_pagination--item::attr(href)').getall()

        for link in next_page:
            yield scrapy.Request(link, callback=self.parse)

    def parse_of_clothing_item(self, response):
        complete_product = BeyondLimitItem()
        complete_product["name"] = self.get_product_name(response)
        complete_product["sku"] = self.get_product_sku(response)
        complete_product["gender"] = self.get_product_gender(response)
        complete_product["description"] = self.get_product_description(response)
        complete_product["retailer_sku"] = self.get_retailer_sku(response)
        complete_product["image_urls"] = self.get_image_urls(response)
        complete_product["care"] = self.get_product_care(response)
        complete_product["lang"] = self.get_language(response)
        complete_product["brand"] = self.get_product_brand(response)
        complete_product["category"] = self.get_product_category(response)
        complete_product["url"] = self.get_product_url(response)
        complete_product["color"] = self.get_product_color(response)
        complete_product["crawl_start_time"] = self.get_crawl_start_time()
        complete_product["time"] = self.get_unix_time()
        complete_product["crawl_id"] = self.get_crawl_id(response)
        yield complete_product

from logging import debug
import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.selector import Selector


class Product(scrapy.Item):
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    body_type = scrapy.Field()
    engine_size = scrapy.Field()
    odometer = scrapy.Field()
    exterior_colour = scrapy.Field()
    transmission = scrapy.Field()
    fuel_type = scrapy.Field()
    asking_price = scrapy.Field()
    advert_text = scrapy.Field()
    image_urls = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    financing_options = scrapy.Field()
    description = scrapy.Field()
    fuel_economy = scrapy.Field()
    stock_number = scrapy.Field()
    contact_number = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    image_urls_out = Identity()


class DrivenSpider(scrapy.Spider):
    name = "driven"

    allowed_domains = [
        'driven.co.nz'
    ]

    start_urls = [
        'https://www.driven.co.nz'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'DUPEFILTER_DEBUG': True
    }

    def parse(self, response):
        total_results = 36535
        page_size = 24
        page_count = int(total_results / page_size)

        form_data = {
            "pageSize": 24,
            "totalResults": 36535,
            "currentview": "",
            "listingType": "u",
            "regionId": 0,
            "districtId": 0,
            "bodytype": "",
            "model": "",
            "pricefrom": 0,
            "priceto": 0,
            "yearfrom": 0,
            "yearto": 0,
            "odometerfrom": 0,
            "odometerto": 0,
            "enginefrom": 0,
            "engineto": 0,
            "categoryId": 30010,
            "colour": "",
            "fuel": "",
            "transmission": "",
            "keywords": "",
            "startIndex": 25,
            "endIndex": 48,
            "reachedEnd": False,
            "sortOrder": "latest"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.driven.co.nz/used-cars-for-sale/?budgetfrequency=totalPrice',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        }

        for i in range(0, page_count):
            form_data['startIndex'] = 1 + (page_size * i)
            form_data['endIndex'] = 24 + (page_size * i)

            yield scrapy.Request(
                'https://www.driven.co.nz/umbraco/surface/ListingResults/ListingSearchResults',
                callback=self.parse_listing, body=json.dumps(form_data), method='POST',
                headers=headers, dont_filter=True)

    def parse_listing(self, response):
        selector = Selector(text=json.loads(response.text)['d']['resultsHtml'])
        product_urls = selector.css('.listing-title::attr(href)').extract()

        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    @staticmethod
    def parse_product(response):
        product_loader = ProductLoader(item=Product(), response=response)

        product_loader.add_css('image_urls', '.rsImg img::attr(src)')

        return product_loader.load_item()

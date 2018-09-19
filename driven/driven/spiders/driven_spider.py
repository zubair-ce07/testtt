import json
import re

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
    # advert_text = scrapy.Field()
    image_urls = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    financing_options = scrapy.Field()
    description = scrapy.Field()
    fuel_economy = scrapy.Field()
    stock_number = scrapy.Field()
    contact_number = scrapy.Field()
    url = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def clean_text(value):
        return ' '.join([v.strip().replace('\r', ' ') for v in value if v.strip()])

    @staticmethod
    def fetch_images(value):
        return [v for v in value if 'driven_no-image' not in v]

    image_urls_out = Identity()

    description_in = clean_text
    financing_options_in = clean_text
    image_urls_in = fetch_images


class DrivenSpider(scrapy.Spider):
    name = "driven"

    allowed_domains = [
        'driven.co.nz'
    ]

    start_urls = [
        'https://www.driven.co.nz/used-cars-for-sale/?budgetfrequency=totalPrice'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'DUPEFILTER_DEBUG': True
    }

    def parse(self, response):
        raw_form = response.xpath('//script[contains(text(), "currentSearch")]').extract_first()
        page_size = int(re.findall(r'pageSize\s*=\s*(\d+);', raw_form)[0])
        total_results = int(re.findall(r'totalResults\s*=\s*(\d+);', raw_form)[0])
        category_id = int(re.findall(r'categoryId\s*=\s*(\d+);', raw_form)[0])

        form_data = {
            "pageSize": page_size,
            "totalResults": total_results,
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
            "categoryId": category_id,
            "colour": "",
            "fuel": "",
            "transmission": "",
            "keywords": "",
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

        page_count = int(total_results / page_size)

        for i in range(0, page_count):
            form_data['startIndex'] = 1 + (page_size * i)
            form_data['endIndex'] = page_size + (page_size * i)

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
        product_loader.add_css('asking_price', 'span.price::text')
        product_loader.add_css('description', '.listing-text-info p::text, '
                                              '.listing-text-info p b::text')
        product_loader.add_css('title', '.listing-header h1::text')
        product_loader.add_css('contact_number', '.seller-cta .mobile-hide::attr(data-phonenumber)')
        product_loader.add_css('financing_options', '.financing-options strong::text, '
                                                    '.financing-options::text')
        product_loader.add_xpath('make', '//*[@class="listing-table-info"]//td[text()="Make"]'
                                         '//following::td[1]/text()')
        product_loader.add_xpath('model', '//*[@class="listing-table-info"]//td[text()="Model"]'
                                          '//following::td[1]/text()')
        product_loader.add_xpath('year', '//*[@class="listing-table-info"]//td[text()="Year"]'
                                         '//following::td[1]/text()')
        product_loader.add_xpath('body_type', '//*[@class="listing-table-info"]//td[contains('
                                              'text(), "Body type")]//following::td[1]/text()')
        product_loader.add_xpath('engine_size', '//*[@class="listing-table-info"]//td[contains('
                                                'text(), "Engine size")]//following::td[1]/text()')
        product_loader.add_xpath('odometer', '//*[@class="listing-table-info"]//td'
                                             '[text()="Odometer"]//following::td[1]/text()')
        product_loader.add_xpath('exterior_colour', '//*[@class="listing-table-info"]//td[text()='
                                                    '"Exterior colour"]//following::td[1]/text()')
        product_loader.add_xpath('transmission', '//*[@class="listing-table-info"]//td[text()='
                                                 '"Transmission"]//following::td[1]/text()')
        product_loader.add_xpath('fuel_type', '//*[@class="listing-table-info"]//td[text()='
                                              '"Fuel Type"]//following::td[1]/text()')
        product_loader.add_xpath('location', '//*[@class="icon-location"]//following::p[1]/text()')
        product_loader.add_xpath('fuel_economy', '//*[@class="listing-table-info"]//td[text()='
                                                 '"Fuel economy"]//following::td[1]/text()')
        product_loader.add_xpath('stock_number', '//*[@class="listing-table-info"]//td[text()='
                                                 '"Stock number"]//following::td[1]/text()')
        product_loader.add_value('url', response.url)

        return product_loader.load_item()

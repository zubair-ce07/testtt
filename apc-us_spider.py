import scrapy
import json
import requests


class ApcProductsSpider(scrapy.Spider):
    name = 'apc-us'
    start_urls = [
        'https://www.apc-us.com',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
    }

    def parse(self, response):
        navigation_links = response.css('nav ul.nav-sublevel li a::attr(href)').getall()
        for headers_url in navigation_links:
            if not '#' in headers_url:
                listing_url = response.urljoin(headers_url)
                yield scrapy.Request(listing_url, callback=self.parse_products_url)

    def parse_products_url(self, response):
        products_link = response.css('main a::attr(href)').getall()
        for product_url in products_link:
            listing_url = response.urljoin(product_url)
            yield scrapy.Request(listing_url, callback=self.parse_detail_page_info)

    def parse_detail_page_info(self, response):
        if '?' in response.url:
            url_split = response.url.split('?')
            url = url_split[0]+'.js'
        else:
            url = response.url+'.js'
        response = requests.request("GET", url)

        json_data = json.loads(response.text)
        product_name = json_data['title']
        product_id = str(json_data['id'])
        product_images_link = json_data['images']
        product_description = json_data['description']
        brand = 'A.P.C'
        currency = 'USD'
# -*- coding: utf-8 -*-
import base64

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from universal.items import UniversalItem


class EnamoraSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.enamora.com`
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }

    name = 'uni'
    allowed_domains = ['www.universal.at']
    start_urls = ['https://www.universal.at']

    rules = (
        Rule(LinkExtractor(
            restrict_css='div#nav-main-list span',
        ), callback='parse_me'),
    )

    def parse_me(self, response):
        print(response.url)

    def parse_urls(self, encoded_url):
        def rot47(url):
            decoded_url = []
            for ch in url:
                ordered_ch = ord(ch)
                if ordered_ch in range(33, 127):
                    decoded_url.append(chr(33 + ((ordered_ch + 14) % 94)))
                else:
                    decoded_url.append(ch)
            return ''.join(decoded_url)
        return rot47(base64.b64decode(encoded_url))

    def parse_item(self, response):
        item = UniversalItem()
        item['url'] = response.url
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        sizes_request = scrapy.Request(url=self.extract_sizes_url(response), callback=self.parse_sizes)
        sizes_request.meta['item'] = item
        sizes_request.meta['color'] = self.extract_color(response)
        sizes_request.meta['price'] = self.extract_price(response)
        yield sizes_request

    def parse_sizes(self, response):
        item = response.meta['item']
        color = response.meta['color']
        price = response.meta['price']
        skus = list()
        sizes_info = response.css("li")
        for size_info in sizes_info:
            size = size_info.css("span::text").extract_first()
            sku = {
                'color': color,
                'size': size,
                'sku_id': "{}_{}".format(color.replace(' ', '_'), size)
            }
            if size_info.css("a[disabled*='disabled']"):
                sku['out_of_stock'] = True
            sku.update(price)
            skus.append(sku)
        item['skus'] = skus
        yield item

    @staticmethod
    def extract_sizes_url(response):
        url = response.css("ul[id='product-sizeselect'] include::attr(src)").extract_first()
        return url.replace('mi.', 'www.')

    @staticmethod
    def extract_name(response):
        return response.url.split('/')[-1].replace('.html', '').replace('-', ' ')

    @staticmethod
    def extract_brand(response):
        return response.css("a.brand::text").extract_first()

    @staticmethod
    def extract_image_urls(response):
        return response.css("ol.carousel-indicators li img::attr(src)").extract()

    @staticmethod
    def extract_care(response):
        return response.css("ul[id='pflegehinweise'] img::attr(alt)").extract()

    @staticmethod
    def extract_color(response):
        return response.css("p.product-color strong::text").extract_first()

    @staticmethod
    def extract_price(response):
        regular_price = response.css("p.regular strong::text").extract_first()
        previous_prices = []
        if not regular_price:
            regular_price = response.css("p.special strong::text").extract_first()
            previous_prices = previous_prices.append(
                response.css("p.old small::text").extract_first(default='').strip()[:-1]
            )
        return {
            'currnency': regular_price.strip()[-1],
            'price': regular_price.strip()[:-1],
            'previous_price': previous_prices
        }

    @staticmethod
    def extract_description(response):
        response = response.replace(
            body=response.body.replace(b'<br />', b'\n').replace(b'<br>', b'\n')
        )
        headings = response.css("div[id='produkt-details'] span.control-label::text").extract()
        descriptions = response.css("div[id='produkt-details'] span.information-value::text").extract()
        return ["{} {}".format(headings[index], description)
                for index, description in enumerate(descriptions)]

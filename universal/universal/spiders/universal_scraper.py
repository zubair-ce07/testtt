# -*- coding: utf-8 -*-
from base64 import b64decode
import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from universal.items import UniversalItem


def clean_url(encoded_url):
    domain = 'https://www.universal.at'
    encoded_url = encoded_url[encoded_url.index('/X') + 1:]

    def rot47(url):
        decoded_url = []
        for ch in url:
            ordered_ch = ord(ch)
            if ordered_ch in range(33, 127):
                decoded_url.append(chr(33 + ((ordered_ch + 14) % 94)))
            else:
                decoded_url.append(ch)
        return ''.join(decoded_url)

    return '{}{}'.format(domain, rot47(b64decode(encoded_url).decode()))


def clean_price(price):
    return price.strip().replace(',', '')


class UniversalSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.universal.at`
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    name = 'universal'
    allowed_domains = ['www.universal.at']
    start_urls = ['https://www.universal.at']
    product_data_url = ('https://www.universal.at/INTERSHOP/rest/WFS/EmpirieCom-UniversalAT-Site/-;loc=de_AT;cur=EUR'
                        '/inventories/{}/master?_=')
    rules = (
        Rule(LinkExtractor(
            restrict_css='div#nav-main-list span',
            process_value=clean_url, attrs=('data-src',), tags=('span',)
        ), callback='parse'),
        Rule(LinkExtractor(
            restrict_css="div.productlist-product a"
        ), callback='parse_item')
    )

    def parse_item(self, response):
        item = UniversalItem()
        retailer_sku = response.url.split('/')[-1]
        item['url'] = response.url
        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        skus_request = self.prepare_skus_request(retailer_sku)
        item['image_urls'] = self.extract_image_urls(response)
        skus_request.meta['item'] = item
        skus_request.meta['price'] = self.extract_price(response)
        yield skus_request

    def prepare_skus_request(self, retailer_sku):
        return scrapy.Request(
            url=self.product_data_url.format(retailer_sku), callback=self.parse_skus
        )

    def parse_skus(self, response):
        item = response.meta['item']
        price = response.meta['price']
        response = json.loads(response.text)
        skus = list()
        for sku in response['variants']:
            sku_dict = {
                self.map_sku_key(sku_info['id']): sku_info['value'] for sku_info in sku['axisData']
            }
            sku_dict['sku_id'] = sku['sku']
            sku_dict.update(price)
            if sku['deliveryStatus'] == 'NOT_AVAILABLE':
                sku_dict['out_of_stock'] = True
            skus.append(sku_dict)
        item['skus'] = skus
        yield item

    @staticmethod
    def map_sku_key(key):
        skus_map = {
            'Var_Article': 'color',
            'Var_Size': 'size',
            'Var_Dimension3': 'size_variant'
        }
        return skus_map.get(key)

    @staticmethod
    def extract_name(response):
        return response.css("h1.headline::text").extract_first()

    @staticmethod
    def extract_brand(response):
        return response.css("div.product-manufacturer-logo img::attr(alt)").extract_first()

    @staticmethod
    def extract_image_urls(response):
        return response.css("img.product-gallery-image::attr(src)").extract()

    @staticmethod
    def extract_care(response):
        care_details = response.css('table.tmpArticleDetailTable tr')
        return [": ".join(care_detail.css('::text').extract()) for care_detail in care_details]

    @staticmethod
    def extract_price(response):
        regular_price = response.css("div.price::text").extract()[1].strip()
        previous_prices = []
        if not regular_price:
            regular_price = clean_price(response.css("div.price.new::text").extract_first().strip())
            previous_prices = previous_prices.append(
                response.css("div.price-strike::text").extract_first(default='').strip()
            )
        price_dict = {
            'currency': regular_price[-1],
            'price': clean_price(regular_price[:-1]),
        }
        if previous_prices:
            price_dict['previous_prices'] = previous_prices
        return price_dict

    @staticmethod
    def extract_description(response):
        return "".join(response.css('div span.long-description *::text').extract()).strip().split('.')

# -*- coding: utf-8 -*-
import json
import operator
from functools import reduce
from base64 import b64decode

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from universal.items import UniversalItem


def clean_url(encoded_url):
    """
    Decode rot47-base64 encoded url
    :param encoded_url: rot47-base64 encoded url with domain as prefix
    :return: Clean decoded url with domain as prefix
    """
    domain = 'https://www.universal.at'
    encoded_url = encoded_url[encoded_url.index('/X') + 1:]

    def rot47(url):
        decoded_url = []
        for ch in url:
            ordered_ch = ord(ch)
            if ordered_ch in range(33, 127):
                decoded_url.append(
                    chr(33 + ((ordered_ch + 14) % 94))
                )
            else:
                decoded_url.append(ch)
        return ''.join(decoded_url)

    return '{}{}'.format(
        domain, rot47(b64decode(encoded_url).decode())
    )


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
    product_img_url = 'https://media.universal.at/i/empiriecom/{}'

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
        item['category'] = self.extract_category(response)
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

        for sku_info in response['variants']:
            sku = {
                self.map_sku_key(sku_info['id']): sku_info['value']
                for sku_info in sku_info['axisData']
            }
            sku['sku_id'] = sku_info['sku']
            sku.update(price)

            if sku_info['deliveryStatus'] == 'NOT_AVAILABLE':
                sku['out_of_stock'] = True
            skus.append(sku)
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

    def extract_image_urls(self, response):
        images_details = json.loads(
            response.css("script.data-product-detail::text").extract_first()
        )
        images = images_details['imageList'].values()

        return [
            self.product_img_url.format(image['image'])
            for image in reduce(operator.add, images)
        ]

    @staticmethod
    def extract_care(response):
        care_details_s = response.css('table.tmpArticleDetailTable tr')
        care_details = care_details_s.css('::text').extract()
        return [
            ": ".join(care_detail)
            for care_detail in care_details
        ]

    @staticmethod
    def extract_price(response):
        pricing = {}
        price = response.css("div.price::text").extract()[-2].strip()
        pricing['price'] = clean_price(price[:-1])
        pricing['currency'] = price[-1]
        previous_prices = response.css("div.price-strike::text").extract_first(default='')
        previous_prices = clean_price(previous_prices.strip()[:-1])

        if previous_prices:
            pricing['previous_prices'] = [previous_prices]

        return pricing

    @staticmethod
    def extract_description(response):
        description = response.css('div span.long-description *::text').extract()
        return "".join(description).strip().split('. ')

    @staticmethod
    def extract_category(response):
        return response.css("div.nav-breadcrumb span::text").extract()

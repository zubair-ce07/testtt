# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from kith.items import KithItem
import json
import re


class KithSpider(CrawlSpider):
    name = 'kith'
    allowed_domains = ['kith.com']
    start_urls = ['https://kith.com/']

    rules = (
        Rule(LinkExtractor(allow=('/collections/.*/products/',)),
                           callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/collections/',)), follow=True),
    )

    def parse_item(self, response):
        product = KithItem()

        product['brand'] = response.css('h1.product-header-title span::text').extract()
        product['url'] = response.url
        main_class = response.css('nav.breadcrumb.text-center')
        product['category'] = main_class.css('a[href^="/c"]::text').extract()
        product['gender'] = self.get_gender(product['category'])
        product['description'] = response.css('div.product-single-details-rte '
                                              'p::text').extract()
        product['care'] = [item for item in product['description']
                           if item.startswith('Material:')]
        product['image_urls'] = response.css('img.full-width::attr(src)').extract()
        product['industry'] = ''
        product['market'] = 'US'
        product['merch_info'] = []

        pattern = re.compile(r"product:(.*?)}]", re.MULTILINE | re.DOTALL)
        script = response.xpath("//script[contains(.,'product:')]/text()").re(pattern)[0]
        script = script.split('variants', 1)
        product['retailer_sku'] = self.get_retailer_sku(script[0])
        product['skus'] = self.get_skus(script[1])

        product['name'] = product['brand'][0].split(' ')[-1]
        product['retailer'] = 'kith-us'

        return product

    def get_gender(self, category):
        if "Women" in category:
            return "women"

    def get_retailer_sku(self, response):
        return response.split(',')[0][1:]

    def get_skus(self, response):
        response = (response + '}]')[2:]
        json_obj = json.loads(response)

        skus = []

        for each in json_obj:
            sku = {}
            sku['ID'] = each['id']
            sku['price'] = each['price']
            sku['currency'] = 'USD'
            sku['out_of_stock'] = each['available']
            sku['previous_price'] = each['compare_at_price']
            sku['size'] = each['title']

            skus.append(sku)

        return skus

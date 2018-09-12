"""
This module extracts products data from puket website
"""
import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PuketSpider(CrawlSpider):

    json_storage = {}
    name = 'puket'
    allowed_domains = ['puket.com.br']
    start_urls = ['http://www.puket.com.br/']
    rules = (

        Rule(LinkExtractor(restrict_css=['.dropLink'])),
        Rule(LinkExtractor(restrict_css=['.shelf-url']), callback='parse_product'),

    )

    def parse_product(self, response):
        product = {}
        self.json_storage = self.retrieve_data(response)
        product['name'] = response.css('.nameProduct::text').extract_first()
        product['price'] = response.css('.val::attr(content)').extract_first()
        product['currency'] = response.css('.priceProduct::attr(data-currency-symbol)')\
            .extract_first()
        product['composition'] = response.css('p.product-attribute-body::text')\
            .extract_first().strip()
        product['description'] = response.css('div.descProduct::text').extract_first().strip()
        product['image_url'] = response.css('.thumb-img::attr(src)').extract()
        product['bread-crumb'] = '>'.join(response.css('.product-breadcrumb a::text').extract())
        product['product_url'] = self.json_storage['product_url']
        product['gender'] = self.json_storage['udasProd']['google_gender']
        product['brand'] = self.json_storage['udasProd']['marca']
        product['category'] = self.json_storage['udasProd']['categoria']
        product['skus'] = self.skus_formation()
        return product


    def retrieve_data(self, response):
        """
        This method extracts data in raw json format from script tag. Data is then to be
        purified by regex and hence load it into pure json format
        :param response:
        :return:
        """
        script = response.css('script[type="text/javascript"]::text').extract_first()
        raw_json = re.findall(r"var\s+skuJson\s*=\s*(\{.*\})", script, re.S)
        pure_json = json.loads(raw_json[0])
        return pure_json


    def skus_formation(self):
        sku = {}
        for item in self.json_storage['skus']:
            sku_id = item['sku']
            sku[sku_id] = {
                'currency': item['currency'],
                'bestPrice': item['bestPrice'],
                'Tamanho': item['udas']['TAMANHO'],
                'color': item['udas']['CORES']
            }
        return sku


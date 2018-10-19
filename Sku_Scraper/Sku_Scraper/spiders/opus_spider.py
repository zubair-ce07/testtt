import json
import requests
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from w3lib.url import add_or_replace_parameter

from ..items import Product


class OpusSpider(CrawlSpider):
    name = "opus_spider"
    session_url = "https://ident.casual-fashion.com/"
    start_urls = ["https://de.opus-fashion.com/de/mode-online"]

    listings_css = '.c-pagination__nav--next'
    product_css = '.c-product-box > .c-product-box__visual'
    
    rules = (
        Rule(LinkExtractor(restrict_css=(listings_css))),
        Rule(LinkExtractor(restrict_css=(product_css)),
             callback="parse_item"),)

    def start_requests(self):
        yield scrapy.Request(self.session_url, callback=self.parse_session)

    def parse_session(self, response):
        session = response.text
        return [scrapy.Request(add_or_replace_parameter(url, "idto", session), callback=self.parse) \
                for url in self.start_urls]

    def parse_item(self, response):
        raw_product = self.raw_product(response)
        product_loader = ItemLoader(item=Product(), response=response)

        product_id = self.product_pid(raw_product)
        product_loader.add_value('pid', product_id)

        gender = self.product_gender(response)
        product_loader.add_value('gender', gender)

        category = self.product_category(raw_product)
        product_loader.add_value('category', category)
        
        url = self.response_url(response)
        product_loader.add_value('url', url)

        name = self.product_name(response)
        product_loader.add_value('name', name)

        description = self.product_description(response)
        product_loader.add_value('description', description)

        image_urls = self.product_image_urls(response)
        product_loader.add_value('image_urls', image_urls)

        skus = self.skus(raw_product, response)
        product_loader.add_value('skus', skus)

        yield product_loader.load_item()

    def raw_product(self, response):
        xpath_raw_product = '//sim-page-tracker//@*[name()=":page-data"]'
        raw_product = response.xpath(xpath_raw_product).extract_first()
        return json.loads(raw_product)

    def product_pid(self, product_detail):
        return product_detail['productId']

    def product_gender(self, response):
        return 'women'

    def product_category(self, product_detail):
        return product_detail['productCategory'].split('>')

    def response_url(self, response):
        return response.url

    def product_name(self, response):
        css = '.c-product-detail__title > span::text'
        return response.css(css).extract_first()

    def product_description(self, response):
        css = '.c-tabs__pane--description li::text, .c-tabs__pane--material-care li::text'
        return response.css(css).extract()
        
    def product_image_urls(self, response):
        css = '.c-product-gallery__thumb-img::attr(src)'
        return response.css(css).extract()

    def skus(self, raw_product, response):
        skus = []
        skus_css = '.c-band--product-detail .c-ipt__input--hidden > option'
        skus_s = response.css(skus_css)

        colour_css = '.c-product-detail__color > span::text'
        colour = response.css(colour_css).extract_first()

        for sku_s in skus_s:
            size_css = 'option::attr(data-size)'
            size = sku_s.css(size_css).extract_first()

            if not size:
                continue

            available_css = 'option::attr(data-available)'
            availability = sku_s.css(available_css).extract_first()

            sku_id = raw_product["productId"] + '_' + size

            sku_item = {"price": raw_product["productPrice"],
                        "currency": raw_product["currencyCode"],
                        "colour": colour,
                        "size": size,
                        "out_of_stock": availability != '1',
                        "sku_id": sku_id}
            skus.append(sku_item)
        return skus


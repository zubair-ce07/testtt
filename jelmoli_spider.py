# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from JelmoliShop.items import JelmoliItem

import urllib.parse as urlparse
import json


class JelmoliSpider(CrawlSpider):
    name = "jelmoli_spider"
    allowed_domains = ["jelmoli-shop.ch"]
    start_urls = ["https://www.jelmoli-shop.ch"]
    deny_expressions = ['geräte', 'multimedia', 'ausrüstung', 'werkzeug', 'maschinen', 'heizen', 'klima', 'spielzeug',
                        'küche', 'elektronik']

    rules = [
        Rule(LinkExtractor(restrict_xpaths="//a[@class='link-product']", deny=deny_expressions),
             callback="parse_product_details"),

        Rule(LinkExtractor(restrict_xpaths="//div[@class='nav-content']//a", deny=deny_expressions),
             callback="parse_subcategory_details"),

        Rule(LinkExtractor(restrict_xpaths="//div[@id='nav-main-list']//a", deny=deny_expressions)),
    ]

    @staticmethod
    def get_subcategory_pagination_url(category_url, page):
        url_parts = list(urlparse.urlparse(category_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'Page': page})
        url_parts[4] = urlparse.urlencode(query)
        return urlparse.urlunparse(url_parts)

    def parse_subcategory_details(self, product_subcategory_response):
        number_of_pages = product_subcategory_response.xpath("(//div/@data-page)[last()]").extract_first() or '1'
        for page in range(int(number_of_pages)):
            subcategory_pagination_url = self.get_subcategory_pagination_url(product_subcategory_response.url,
                                                                             "P{page_no}".format(page_no=page))
            yield scrapy.Request(url=subcategory_pagination_url, dont_filter=True)

    def parse_product_details(self, product_response):
        product_details = product_response.xpath("//script[@class='data-product-detail']/text()").extract_first()
        product_details_json = json.loads(product_details)

        product = JelmoliItem()

        product["brand"] = self.get_brand_from_json(product_details_json)
        product["care"] = self.get_care_from_json(product_details_json)
        product["category"] = self.get_category_from_response(product_response)
        product["description"] = self.get_description_from_json(product_details_json)
        product["gender"] = self.get_gender_from_response(product_response)
        product["image_urls"] = self.get_image_urls_from_json(product_details_json)
        product["industry"] = self.get_industry_from_response(product_response)
        product["market"] = self.get_market()
        product["name"] = self.get_name_from_json(product_details_json)
        product["lang"] = self.get_lang_from_response(product_response)
        product["retailer"] = self.get_retailer()
        product["retailer_sku"] = self.get_retailer_sku_from_json(product_details_json)
        product["skus"] = self.get_skus_from_json(product_details_json)
        product["url"] = self.get_url_from_response(product_response)

        yield product

    @staticmethod
    def get_brand_from_json(product_json):
        product_variations = product_json["variations"]
        for sku in product_variations.keys():
            return product_variations[sku]["manufacturerName"]

    @staticmethod
    def get_care_from_json(product_json):
        care = [Selector(text=product_json["tags"]["T0"]).xpath("//text()").extract_first()]

        product_details = Selector(text=product_json["tags"]["T2"])
        care.extend(product_details.xpath("//td//text()[contains(.,'Materialzusammensetzung')]"
                                          "//ancestor::td//following-sibling::td//text()"
                                          "| //td//text()[contains(.,'Applikationen')]"
                                          "//ancestor::td//following-sibling::td//text()").extract())

        return care

    @staticmethod
    def get_category_from_response(product_response):
        return product_response.xpath("//li[contains(@typeof,'Breadcrumb')]//text()[normalize-space()]").extract()

    @staticmethod
    def get_description_from_json(product_json):
        description = Selector(text=product_json["tags"]["T0"]).xpath("//text()").extract()

        product_details = Selector(text=product_json["tags"]["T2"])
        description.extend(product_details.xpath("//td//following-sibling::td//text()").extract())

        return description

    def get_gender_from_response(self, product_response):
        if self.get_industry_from_response(product_response):
            return

        categories = self.get_category_from_response(product_response)
        genders = {'Damen': 'women', 'Herren': 'men', 'Kinder': 'unisex-kids'}
        for category in categories:
            if category in genders:
                return genders.get(category)

        return 'unisex-adult'

    def get_industry_from_response(self, product_response):
        categories = self.get_category_from_response(product_response)
        if any(category in ['Wohnen', 'Baumarket'] for category in categories):
            return 'homeware'

    @staticmethod
    def get_image_urls_from_json(product_json):
        image_url = "https://images.jelmoli-shop.ch/asset/mmo/formatz/{image_name}"
        product_images = product_json["galleryImages"]
        return [image_url.format(image_name=image["image"]) for image in product_images]

    @staticmethod
    def get_lang_from_response(product_response):
        return product_response.xpath("//html/@lang").extract_first()

    @staticmethod
    def get_name_from_json(product_json):
        return product_json["nameWithoutManufacturer"]

    @staticmethod
    def get_market():
        return "CH"

    @staticmethod
    def get_retailer():
        return "jelmoli-ch"

    @staticmethod
    def get_retailer_sku_from_json(product_json):
        return product_json["sku"]

    @staticmethod
    def get_skus_from_json(product_json):
        skus = {}
        product_variations = product_json["variations"]
        product_skus = product_variations.keys()
        for sku in product_skus:
            sku_details = product_variations[sku]
            skus[sku] = {"colour": sku_details["variationValues"]["Var_Article"],
                         "currency": sku_details["currentPrice"]["currency"],
                         "price": sku_details["currentPrice"]["value"],
                         "size": sku_details["size"]}
        return skus

    @staticmethod
    def get_url_from_response(product_response):
        return product_response.url

# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import FormRequest

from Immobilienscout24.items import Immobilienscout24Item
from .Base import BaseClass


class Immobilienscout24CrawlSpider(scrapy.Spider, BaseClass):
    name = "Immobilienscout24-crawl"
    allowed_domains = ["immobilienscout24.de"]
    start_urls = ['https://www.immobilienscout24.de/']
    items_url = "https://www.immobilienscout24.de/Suche/controller/oneStepSearch/form.html"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, response):
        for city in self.cities:
            for rent_type in self.rent_types:
                item = Immobilienscout24Item()
                body = {
                    'world': 'LIVING',
                    'location': city,
                    'region': city,
                    'realEstateType': rent_type,
                    'gacId': '1276003001',
                    'geoCodeId': '1276003001',
                    'geographicalEntityType': 'city'
                }

                item["type"] = "Rent"
                item["city"] = city
                item["subtype"] = rent_type
                yield FormRequest(url=self.items_url, callback=self.parse_items_listing,
                            formdata=body, headers=self.headers, meta={'item': item})

    def parse_items_listing(self, response):
        item = response.meta["item"]
        print(item)
        listing_res = json.loads(response.text)

        print(listing_res)

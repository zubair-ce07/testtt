# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import FormRequest, Request

from Immobilienscout24.items import Immobilienscout24Item
from .Base import BaseClass


class Immobilienscout24CrawlSpider(scrapy.Spider, BaseClass):
    name = "Immobilienscout24-crawl"
    allowed_domains = ["immobilienscout24.de"]
    start_urls = ['https://www.immobilienscout24.de/']
    property_listing_url = "https://www.immobilienscout24.de/Suche/controller/oneStepSearch/form.html"
    result_count_url = "https://www.immobilienscout24.de/Suche/controller/oneStepSearch/resultCount.json"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, response):
        for city in self.cities_mini:
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

                item["property_type"] = "Rent"
                item["city"] = city
                item["property_subtype"] = rent_type
                yield FormRequest(url=self.result_count_url, callback=self.parse_property_count,
                                  formdata=body, headers=self.headers, meta={'item': item, 'body': body})

    def parse_property_count(self, response):
        item = response.meta["item"]
        body = response.meta["body"]
        result_count_res = json.loads(response.text)
        if not result_count_res["error"]:
            item["property_count"] = result_count_res["count"]

            yield FormRequest(url=self.property_listing_url, method="POST", callback=self.parse_property,
                              headers=self.headers, meta={'item': item}, formdata=body)

    def parse_property(self, response):
        print(response.body)

        property_res = json.loads(response.text)
        if not property_res["errors"]:
            url = response.urljoin(property_res["redirectUrl"])
            yield Request(url=url, meta={'item': response.meta['item']},
                          callback=self.parse_property_listing, headers=self.headers)

    def parse_property_listing(self, response):
        print("response url", response.url)

        yield response.meta["item"]

# -*- coding: utf-8 -*-
import copy
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
    location_url_t = "https://www.immobilienscout24.de/geoautocomplete/v3/locations.json?i={}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def parse(self, response):
        for city in self.cities:
            item = Immobilienscout24Item()
            body = {
                'world': 'LIVING',
                'location': city,
                'region': city,
                'city': city,
                'geographicalEntityType': 'city'
            }
            item["property_type"] = "Rent"
            item["city"] = city
            url = self.location_url_t.format(city)
            yield Request(url=url, callback=self.parse_location, meta={'item': item, 'body': body})

    def parse_location(self, response):
        item = copy.deepcopy(response.meta["item"])
        body = copy.deepcopy(response.meta["body"])

        location = json.loads(response.text)
        location_id = [l["entity"]["id"] for l in location if l["entity"]["type"] == "city"]
        location_id = location_id[0] or None
        if not location_id:
            return

        body["gacId"] = location_id
        body["geoCodeId"] = location_id

        for rent_type in self.rent_types:
            item["property_subtype"] = rent_type
            body['realEstateType'] = rent_type
            yield FormRequest(method="POST", url=self.result_count_url, callback=self.parse_property_count,
                              formdata=body, headers=self.headers,
                              meta={'item': copy.deepcopy(item), 'body': body})

    def parse_property_count(self, response):
        item = copy.deepcopy(response.meta["item"])
        body = copy.deepcopy(response.meta["body"])
        result_count_res = json.loads(response.text)
        if not result_count_res["error"]:
            item["property_count"] = result_count_res["count"]

            yield FormRequest(url=self.property_listing_url, method="POST", callback=self.parse_property_redirect_url,
                              headers=self.headers, meta={'item': item}, formdata=body)

    def parse_property_redirect_url(self, response):
        property_res = json.loads(response.text)
        item = copy.deepcopy(response.meta['item'])
        if not property_res["errors"]:
            url = response.urljoin(property_res["redirectUrl"])
            yield Request(url=url, meta={'item': item},
                          callback=self.parse_property_listing, headers=self.headers)

    def parse_property_listing(self, response):
        item = response.meta["item"]
        item["url"] = response.url
        yield item

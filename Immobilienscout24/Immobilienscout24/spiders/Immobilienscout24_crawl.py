# -*- coding: utf-8 -*-
import copy
import datetime
import json
import re
import string

import scrapy
from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor

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
    agent_info_re = re.compile(r'contactData: *(\{.*\}),')
    agent_ingo_typ2_re = re.compile(r'JSON\.parse\(\'(\{.*\}?)\'\)')

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

            item["city"] = city
            url = self.location_url_t.format(city)
            yield Request(url=url, callback=self.parse_location, meta={'item': copy.deepcopy(item), 'body': body})

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

        # Rent
        for rent_type in self.rent_types:
            item["property_type"] = "Rent"
            item["property_subtype"] = rent_type
            body['realEstateType'] = rent_type
            yield FormRequest(method="POST", url=self.result_count_url, callback=self.parse_property_count,
                              formdata=body, headers=self.headers,
                              meta={'item': copy.deepcopy(item), 'body': copy.deepcopy(body)})
        # Sale
        for sale_type in self.sale_types:
            item["property_type"] = "Sale"
            item["property_subtype"] = sale_type
            body['realEstateType'] = sale_type
            yield FormRequest(method="POST", url=self.result_count_url, callback=self.parse_property_count,
                              formdata=body, headers=self.headers,
                              meta={'item': copy.deepcopy(item), 'body': copy.deepcopy(body)})

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
        items_extractor = LinkExtractor(restrict_css=".result-list__listing", deny="Suche")

        for link in items_extractor.extract_links(response):
            yield Request(url=link.url, callback=self.parse_property, meta={'item': item})

        css = '[data-is24-qa="paging_bottom_next"] ::attr(href)'
        next_page_url = response.css(css).extract_first()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_property_listing,
                                  meta={'item': item}, headers=self.headers)

    def parse_property(self, response):
        # item = response.meta["item"]
        item = Immobilienscout24Item()
        item["url"] = response.url
        item['crawl_datetime'] = datetime.datetime.utcnow()

        css = 'script:contains("contactData")::text'
        product = response.css(css).re_first(self.agent_info_re)

        if product:
            product = json.loads(product)
            del product['contactButton']
            item['agent'] = product
        else:
            item['agent'] = self.item_agent(response)

        yield item

    def item_agent(self, response):
        agent = dict()
        css = 'script:contains("projectData")::text'
        agent_info_json = response.css(css).re_first(self.agent_ingo_typ2_re)
        if agent_info_json:
            agent_info_json = agent_info_json.replace('\\"', '\"')

            agent_info_json = json.loads(agent_info_json)

        agent["phoneNumbers"] = self.agent_contact_number(response, agent_info_json)
        agent['realtorInformation'] = self.agent_company_info(response, agent_info_json)

        return agent

    def agent_contact_number(self, response, agent_info):
        phone = dict()
        if agent_info:
            phone_number = agent_info['realtorPhoneNumber']
        else:
            phone_number = response.css('.phone-link ::text').extract_first()

        phone['phoneNumber'] = {
            'contactNumber': phone_number
        }
        return phone

    def agent_company_info(self, response, agent_info):
        company_info = dict()
        if agent_info:
            company_info['companyName'] = response.css('h2.grid-item ::text').extract_first()
        else:
            company_info['companyName'] = response.css('.homepage-url ::text').extract_first()
            company_info['realtorHomepage'] = response.css('.homepage-url ::attr(href)').extract_first()

        return company_info

    def remove_non_ascii_characters(self, to_remove):
        to_remove = [c for c in to_remove if c in string.printable]
        return "".join(to_remove)

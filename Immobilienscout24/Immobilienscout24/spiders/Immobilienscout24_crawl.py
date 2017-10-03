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
    cities_url_t = "https://www.immobilienscout24.de/geoautocomplete/v3/locations.json?i={}&t=city"
    location_url_t = "https://www.immobilienscout24.de/geoautocomplete/v3/locations.json?i={}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    agent_info_re = re.compile(r'contactData: *(\{.*\}),')
    agent_info_typ2_re = re.compile(r'JSON\.parse\(\'(\{.*\}?)\'\)')
    listing_re = re.compile(r'onTopProduct\s*:\s*\'(\w+)\',')

    listing_map = {
        'XL': 'XL',
        'L': 'L',
        'M': 'M',
        '': 'Basic'
    }

    def parse(self, response):
        for alphabet in string.ascii_lowercase:
            url = self.cities_url_t.format(alphabet)
            yield Request(url=url, callback=self.parse_cities, headers=self.headers)

    def parse_cities(self, response):
        cities = json.loads(response.text)
        common_body = dict()
        common_body['world'] = 'LIVING'
        common_body['geographicalEntityType'] = 'city'
        for city in cities:
            item = Immobilienscout24Item()
            body = common_body.copy()
            current_city = city['entity']['label']
            item['city'] = current_city
            print("city name ", current_city)
            body['location'] = current_city
            body['region'] = current_city
            body['city'] = current_city
            body["gacId"] = city['entity']['id']
            body["geoCodeId"] = body["gacId"]

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
            item["property_count_in_city"] = result_count_res["count"]

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
        item = response.meta["item"]
        item["url"] = response.url
        if 'expose' in response.url:
            item['id'] = response.url.split('expose/')[-1]
        else:
            item['id'] = response.url.split('/')[-1].split('.')[0]
        item['crawl_datetime'] = datetime.datetime.utcnow()
        item['property_name'] = self.property_name(response)
        item['property_address'] = self.property_address(response)
        item['category'] = self.item_category(response)
        item['type_of_listing'] = self.item_property_listing_type(response)

        css = 'script:contains("contactData")::text'
        product = response.css(css).re_first(self.agent_info_re)

        if product:
            product = json.loads(product)
            if product.get('realtorInformation').get('realtorHomepage'):
                product['realtorInformation']['Homepage'] = product['realtorInformation']['realtorHomepage']

            del product['realtorInformation']['privateOffer']

            if product.get('realtorInformation').get('realtorLogo'):
                del product['realtorInformation']['realtorLogo']

            if product.get('realtorInformation').get('realtorHomepage'):
                del product['realtorInformation']['realtorHomepage']

            del product['contactButton']

            product['companyInformation'] = product['realtorInformation']

            del product['realtorInformation']
            item['agent'] = product
        else:
            item['agent'] = self.item_agent(response)

        yield item

    def item_agent(self, response):
        agent = dict()
        css = 'script:contains("projectData")::text'
        agent_info_json = response.css(css).re_first(self.agent_info_typ2_re)
        if agent_info_json:
            agent_info_json = agent_info_json.replace('\\"', '\"')
            if '\\' in agent_info_json:
                agent_info_json = agent_info_json.replace('\\', '')

            agent_info_json = json.loads(agent_info_json)

        agent["phoneNumbers"] = self.agent_contact_number(response, agent_info_json)
        agent['companyInformation'] = self.agent_company_info(response, agent_info_json)

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
            company_info['Homepage'] = response.css('.homepage-url ::attr(href)').extract_first()

        return company_info

    def property_name(self, response):
        css = '[property="og:title"] ::attr(content)'
        return response.css(css).extract_first()

    def property_address(self, response):
        address = dict()
        address['address'] = "".join(response.css('.address-block :first-child ::text').extract())
        address['zipcode'] = response.css('.zip-region-and-country ::text').extract_first()

        return address

    def item_category(self, response):
        category = response.css('.flex-item--center > ::text').extract()
        return self.clean(category)

    def item_property_listing_type(self, response):
        css = 'script:contains("onTopProduct")::text'
        listing_type = response.css(css).re_first(self.listing_re)
        if not listing_type:
            listing_type = ''

        return self.listing_map[listing_type]

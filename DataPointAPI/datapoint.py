# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request


class DatapointSpider(scrapy.Spider):
    name = 'datapoint'
    allowed_domains = ['datapoint.com']

    def start_requests(self):
        urls = ['https://io.datapointapi.com/token']
        payload = '''grant_type=password&username=DpsNtxUser
                     &password=!!4WriteTesting'''
        data_headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
            }
        for url in urls:
            yield Request(url=url, callback=self.parse, method='POST',
                          headers=data_headers,
                          body=payload)

    def parse(self, response):
        json_response = json.loads(response.text)
        access_token = json_response['access_token']

        url = "https://io.datapointapi.com/api/Sites/20288/RealTimeToken"
        headers = {
            'Authorization': "Bearer {}".format(access_token),
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        yield Request(url=url, callback=self.request_data, method='GET',
                      headers=headers, dont_filter=True,
                      meta={"RT": access_token})

    def request_data(self, response):
        urls = [
                "https://io.datapointapi.com/odata/Patients",
                "https://io.datapointapi.com/odata/Clients",
                "https://io.datapointapi.com/odata/Appointments",
                "https://io.datapointapi.com/odata/Codes",
                "https://io.datapointapi.com/odata/Resources"
                ]
        api_urls = [
                    '''https://io.datapointapi.com/api/lookups/
                        20288/InvoiceItems''',
                    '''https://io.datapointapi.com/api/lookups/
                        20288/InventoryClasses''',
                    '''https://io.datapointapi.com/api/lookups/
                        20288/Documents''',
                    '''https://io.datapointapi.com/api/lookups/
                        20288/UnitsOfMeasure''',
                    '''https://io.datapointapi.com/api/lookups/
                        20288/RevenueCenters'''
                    ]
        headers = {
            'Authorization': "Bearer {}".format(response.meta["RT"]),
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
            }

        for url in urls:
            url = url+"?$filter=SiteId eq 20288"
            yield Request(url=url,
                          callback=self.parse_all_data, method='GET',
                          headers=headers, dont_filter=True,
                          meta={"RT": response.meta["RT"],
                                "OldRT": response.text})

        for url in api_urls:
            yield Request(url=url, callback=self.parse_all_data, method='GET',
                          headers=headers, dont_filter=True,
                          meta={"RT": response.meta["RT"],
                                "OldRT": response.text})

    def parse_all_data(self, response):
        yield json.loads(response.text)
        headers = {
            'Authorization': "Bearer {}".format(response.meta["RT"]),
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
            }
        if "Patients" in response.url:
            json_response = json.loads(response.text)
            url = "https://io.datapointapi.com/api/20288/patients"
            for patient_data in json_response["value"]:
                yield Request(
                    url=url+"?id="+patient_data["pimsPatientIdentifier"],
                    callback=self.parse_details_data,
                    method='GET', headers=headers, dont_filter=True,
                    meta={"RT": response.meta["RT"],
                            "OldRT": response.meta["OldRT"]})

        if "Clients" in response.url:
            url = "https://io.datapointapi.com/api/20288/clients/"
            for client_data in json_response["value"]:
                yield Request(url=url+client_data["pimsClientIdentifier"],
                              callback=self.parse_details_data,
                              method='GET', headers=headers, dont_filter=True)

    def parse_details_data(self, response):

        if response.meta.get("OldRT", None):
            headers = {
                'Authorization': "Bearer {}".format(response.meta["OldRT"]),
                'Accept': "application/json",
                'Content-Type': "application/json",
                'Cache-Control': "no-cache"
            }
            if "patients" in response.url:
                patient_id = json.loads(response.text)
                patient_id = patient_id["response"][0]["patient"]["pimsIdentifier"]
                url = '''https://datapointrelay-dev.servicebus.windows.net/
                            20288/api/patient-prescriptions/'''
                yield Request(url=url+patient_id,
                              callback=self.parse_details_data,
                              method='GET', headers=headers, dont_filter=True,
                              meta={"OldRT": response.meta["OldRT"]})
            else:
                urls = [
                        '''https://datapointrelay-dev.servicebus.windows.net/20288
                        /api/census?censusType=OutPatient''',
                        '''https://datapointrelay-dev.servicebus.windows.net/20288
                        /api/census?censusType=InPatient'''
                        ]
                for url in urls:
                    yield Request(url=url,
                                  callback=self.parse_details_data,
                                  method='GET', headers=headers,
                                  dont_filter=True)
                yield {
                    "Patient-Prescription": eval(response.text.replace(
                        'null', '"null"').replace('true', '"True"'))
                }

        else:
            yield {
                "Census-Out": eval(response.text.replace('null', '"null"'))
            }

# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from urllib.parse import urlencode

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

import pdb
import pprint


class DocketSpider(scrapy.Spider):
    name = 'docket'
    base_url = "http://documents.dps.ny.gov/public/"
    allowed_domains = [base_url]
    start_urls = [base_url]

    search_result_endpoint = "Common/SearchResults.aspx"
    dockets_endpoint = "CaseMaster/MatterExternal"


    def start_requests(self):

        if not (self.from_date and self.to_date):
            logging.error("Pass from_date and to_date in options")

        from_date = "10/2/2016"
        to_date = "02/01/2017"

        param_dict = {
            "MC": 1,
            "SDT": to_date,
            "SDF": from_date,
            "CO": 0
        }
        search_url = f"{self.base_url}{self.search_result_endpoint}?{urlencode(param_dict)}"
        yield scrapy.Request(url=search_url, callback=self.parse_dockets_url,
                             errback=self.errback_docket, dont_filter=True)


    def parse_dockets_url(self, response):
        matter_sq_re = r"\bvar\s+MatterSeq\s*=\s*'(.*?)\?'\s*\+\s*\$\('(#.*?)'\)\[0\]\.value;\s*\n"

        matter_seq, hidden_params =  response.css('script::text').re(matter_sq_re)
        querrry_params = response.css(hidden_params).attrib['value']
        final_url = f"{self.base_url}{self.dockets_endpoint}/{matter_seq}?{querrry_params}"
        yield scrapy.Request(url=final_url, callback=self.parse_docket,
                             errback=self.errback_docket, dont_filter=True)


    def parse_docket(self, response):
        dockets_data = json.loads(response.body)

        for obj in dockets_data:
            pprint.pprint(obj)
            yield obj

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)


    def errback_docket(self, failure):
        # log all errback failures
        logging.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            logging.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            logging.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            logging.error('TimeoutError on %s', request.url)

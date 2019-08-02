# -*- coding: utf-8 -*-
"""
    This module implements a spider that crawls proceedings for a
    given time period from the following website
    http://docs.cpuc.ca.gov/
"""

import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from pprint import pprint
import re

from ..items import CaPucItem


class ProceedingsSpider(scrapy.Spider):
    name = 'proceedings'
    search_form_url = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx/'
    proceeding_details_base_url = 'https://apps.cpuc.ca.gov/apex/f?p=401:{}:'\
        '666746862207::NO:RP,57,RIR:P5_PROCEEDING_SELECT:'
    proceeding_details_url = proceeding_details_base_url.format('56')
    filings_url = proceeding_details_base_url.format('57')
    start_urls = [search_form_url]
    # download_delay = 5

    def parse(self, response):
        """
            Get the search form and send a form request with
            given time period
        """
        # creating a form data for request
        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'FilingDateFrom': '02/21/19',
            'FilingDateTo': '02/26/19',
            'IndustryID': '-1',
            'ddlCpuc01Types': '-1',
            'SearchButton': 'Search'
        }
        # yielding a Form Request
        yield scrapy.FormRequest.from_response(
            response,
            url=self.search_form_url,
            formdata=form_data,
            callback=self.parse_proceedings,
            formid="frmSearchform",
            meta={'do_pagination': True}
        )

    def do_proceedings_pagination(self, response):
        """
            Get all of the remaining pages target and
            yield a form request to them.
        """
        view_state, \
            view_state_generator, \
            event_validation = self.get_form_states(response)
        # Getting pages
        pages_selector = '//a[contains(@href, "rptPages")]/@href'
        # Sending request for paginations
        print(len(response.xpath(pages_selector).getall()))
        for p in response.xpath(pages_selector).getall():
            event_target = p.split("'")[1]
            # creating a form data for request
            form_data = {
                '__EVENTTARGET': event_target,
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_state_generator,
                '__EVENTVALIDATION': event_validation
            }
            # yielding a Form Request
            yield scrapy.FormRequest(
                url='http://docs.cpuc.ca.gov/SearchRes.aspx',
                formdata=form_data,
                callback=self.parse_proceedings,
                dont_filter=True
            )

    def parse_proceedings(self, response):
        """
            Get the search results and send an
            individual request for each proceeding id
        """
        proceeding_ids = self.get_proceeding_ids(response)
        print(list(set(proceeding_ids)))
        for p_id in proceeding_ids:
            yield scrapy.Request(
                url='{}{}'.format(self.proceeding_details_url, p_id),
                callback=self.parse_proceedings_details,
                meta={'proceeding_id': p_id},
            )

        if "do_pagination" in response.meta and response.meta["do_pagination"]:
            for next_proceeding in self.do_proceedings_pagination(response):
                yield next_proceeding

    def parse_proceedings_details(self, response):
        """
            Load the item with given data on this proceeding
            detail page and send a request to parse filings for
            a given proceeding

            meta_data: loader:ItemLoader
        """
        # print('parse_proceedings_details headers', response.headers)
        proceeding_id = response.meta['proceeding_id']

        loader = ItemLoader(item=CaPucItem(), response=response)
        loader.add_css('_id', 'div.rounded-corner-region::attr("id")')
        loader.add_css('filed_on', '#P56_FILING_DATE::text')
        loader.add_css('assignees', '#P56_STAFF::text')
        loader.add_css('industries', '#P56_INDUSTRY::text')
        loader.add_css('filed_by', '#P56_FILED_BY::text')
        loader.add_css('proceeding_type', '#P56_CATEGORY::text')
        loader.add_css('title', '#P56_DESCRIPTION::text')
        loader.add_css('status', '#P56_STATUS::text')
        loader.add_css('state_id', 'h1::text')

        yield scrapy.Request(
            url='{}{}'.format(self.filings_url, proceeding_id),
            callback=self.parse_filings,
            meta={'loader': loader}
        )

    def parse_filings(self, response):
        """
            Iterate through filing rows on the given filing page
            and send request to parse documents for a given filing

            meta_data: loader:ItemLoader, filing:dict
        """
        loader = response.meta['loader']
        # getting filing details
        filings_rows = response.xpath(
            '//*[@class="apexir_WORKSHEET_DATA"]/tr[preceding-sibling::*]')
        # update loaders with meta data of filing count and total filings
        loader.add_value('total_filing_count', len(filings_rows))
        loader.add_value('filing_count', 0)

        for row in filings_rows:
            filing = {
                "description": row.xpath('td[4]/text()').get(),
                "documents": [],
                "filed_on": row.xpath('td[1]/text()').get(),
                "filing_parties": row.xpath('td[3]/text()').get(),
                "types": row.css('u::text').get().split(' ')
            }
            # Getting doucments for each filing
            documents_link = row.css('td a::attr("href")').get()

            yield SplashRequest(
                url=documents_link,
                callback=self.parse_documents,
                meta={'loader': loader, 'filing': filing},
                dont_filter=True,
                dont_process_response=True
            )

    def parse_documents(self, response):
        """
            Iterate through document rows on the given document page
            and update the filing with the respective documents.
            Finally, return the completely populated item if all filings
            are processed.

            return required item
        """
        print(response.headers)
        loader, filing = response.meta["loader"], \
            response.meta["filing"]

        # populating filing with respective documents
        filing = self.get_filing_with_documents(response, filing)
        # updating filings
        filings = loader.load_item()['filings'].append(filing) \
            if 'filings' in loader.load_item() else [filing]

        loader.replace_value('filings', filings)

        loader.replace_value(
            'filing_count',
            loader.load_item()['filing_count'] + 1
        )

        # Check if its last request so we can yield the item
        if self.is_last_request(loader):
            return loader.load_item()

    def is_last_request(self, loader):
        """ Check if its last request of filing """
        return loader.load_item()['total_filing_count'] == \
            loader.load_item()['filing_count']

    def get_filing_with_documents(self, response, filing):
        """
            Fetch the documents from response and
            return the updated filing with documents
        """
        rows = response.css('#ResultTable tr:not([style])')
        print(len(rows), " Documents Fetched ")
        for row in rows:
            source_url = row.css('.ResultLinkTD a::attr("href")').get()
            document = {
                "name": source_url.split('.')[0].split('/')[-1],
                "extension": source_url.split('.')[1],
                "source_url": row.css('.ResultLinkTD a::attr("href")').get(),
                "title": row.css('.ResultTitleTD::text').get()
            }

            filing["documents"].append(document)

        return filing

    def get_proceeding_ids(self, response):
        """Returning a list proceeding ids from the response"""
        ids = []
        proceedings_selector = '//*[@class="ResultTitleTD"]/text()[2]'
        for proceeding in response.xpath(proceedings_selector).getall():
            print(proceeding)
            ids += re.findall(r'\w\d{7}', proceeding)

        return ids

    def get_form_states(self, response):
        """ Getting VIEWSTATE from asp pages"""
        view_state = response.xpath(
            '//input[contains(@id, "__VIEWSTATE")]/@value').get()
        view_state_generator = response.xpath(
            '//input[contains(@id, "__VIEWSTATEGENERATOR")]/@value').get()
        event_validation = response.xpath(
            '//input[contains(@id, "__EVENTVALIDATION")]/@value').get()

        return view_state, view_state_generator, event_validation

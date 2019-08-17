# -*- coding: utf-8 -*-
"""
    This module implements a spider that crawls proceedings for a
    given time period from the following website
    http://docs.cpuc.ca.gov/
"""

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
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

    def __init__(self):
        self.p_instance = None
        self.p_flow_id = None
        self.p_flow_step_id = None

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
        proceeding_id = response.meta['proceeding_id']

        loader = ItemLoader(item=CaPucItem(), response=response)
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
            meta={'loader': loader, 'first_page': True, 'filing_list': []}
        )

    def parse_filings(self, response):
        """
            Iterate through filing rows on the given filing page
            and send request to parse documents for a given filing

            meta_data: loader:ItemLoader, filing:dict
        """
        # getting filing details
        filings_rows = response.xpath(
            '//*[@class="apexir_WORKSHEET_DATA"]/tr[preceding-sibling::*]')

        for row in filings_rows:
            filing = {
                "description": row.xpath('td[4]/text()').get(),
                "documents": [],
                "filed_on": row.xpath('td[1]/text()').get(),
                "filing_parties": row.xpath('td[3]/text()').get(),
                "types": row.css('u::text').get().split(' '),
                "documents_link": row.css('td a::attr("href")').get()
            }
            # Getting doucments for each filing
            if re.search('orderadocument', filing['documents_link']):
                continue

            response.meta['filing_list'].append(filing)

        # Doing pagination for filings
        for filing_next_page in self.do_filings_pagination(response):
            yield filing_next_page

    def do_filings_pagination(self, response):
        """
            Doing pagination for filings
            1. check if anchor exists for next page.
            2. create appropriate form data
            3. send form request to navigate
        """
        next_page_anchor = self.get_filing_next_page_anchor(response)
        # Sending request for paginations
        if not next_page_anchor:
            # Here we have all filings in a list we will fill them with
            # respective documents
            for request in self.scrap_filing_for_documents(response):
                yield request

        else:
            widget_action_mod = next_page_anchor.split("'")[1]
            x01 = response.xpath(
                '//input[@id="apexir_WORKSHEET_ID"]/@value').get()
            x02 = response.xpath(
                '//input[@id="apexir_REPORT_ID"]/@value').get()

            # update member variables to hold data across multiple requests
            if not self.p_instance:
                self.p_instance = response.xpath(
                    '//input[contains(@name,"p_instance")]/@value').get()
            if not self.p_flow_id:
                self.p_flow_id = response.xpath(
                    '//input[@id="pFlowId"]/@value').get()
            if not self.p_flow_step_id:
                self.p_flow_step_id = response.xpath(
                    '//input[@id="pFlowStepId"]/@value').get()

            form_data = {
                'p_request': 'APXWGT',
                'p_instance': self.p_instance,
                'p_flow_id': self.p_flow_id,
                'p_flow_step_id': self.p_flow_step_id,
                'p_widget_num_return': '100',
                'p_widget_name': 'worksheet',
                'p_widget_mod': 'ACTION',
                'p_widget_action': 'PAGE',
                'p_widget_action_mod': widget_action_mod,
                'x01': x01,
                'x02': x02
            }
            response.meta["first_page"] = False
            # yielding a Form Request
            yield scrapy.FormRequest(
                url="https://apps.cpuc.ca.gov/apex/wwv_flow.show",
                formdata=form_data,
                callback=self.parse_filings,
                dont_filter=True,
                headers={
                    'Referer': response.url
                },
                meta=response.meta,
            )

    def scrap_filing_for_documents(self, response):
        if len(response.meta['filing_list']) == 0:
            yield response.meta['loader'].load_item()
        else:
            filing = response.meta['filing_list'].pop()
            response.meta['filing'] = filing

            yield scrapy.Request(
                url=filing['documents_link'],
                callback=self.parse_documents,
                meta=response.meta,
                dont_filter=True
            )

    def parse_documents(self, response):
        """
            Simulating an event click on a link.

            at first the response does not contain the required data.
            This method sends a Form Request with necessary data to
            the same url and send the response to appropriat callback
            for futher processing.
        """
        # Getting pages
        pages_selector = '//a[contains(@href, "rptPages")]/@href'
        # Sending request for paginations
        for p in response.xpath(pages_selector).getall():
            event_target = p.split("'")[1]
            # creating a form data for request
            form_data = {
                '__EVENTTARGET': event_target,
                '__EVENTARGUMENT': ''
            }
            # yielding a Form Request
            yield scrapy.FormRequest.from_response(
                response,
                url=response.url,
                dont_click=True,
                formdata=form_data,
                callback=self.get_all_documents,
                dont_filter=True,
                meta=response.meta
            )

    def get_all_documents(self, response):
        """
            Iterate through document rows on the given document page
            and update the filing with the respective documents.
            Finally, return the completely populated item if all filings
            are processed.

            return required item
        """
        loader, filing = response.meta["loader"], \
            response.meta["filing"]

        filing = self.get_filing_with_documents(response, filing)

        filings = loader.load_item()['filings'].append(filing) \
            if 'filings' in loader.load_item() else [filing]

        loader.replace_value('filings', filings)

        # scraping next filing for documents
        for request in self.scrap_filing_for_documents(response):
            yield request

    def get_filing_with_documents(self, response, filing):
        """
            Fetch the documents from response and
            return the updated filing with documents
        """
        document_rows = response.xpath(
            '//table[contains(@id, "ResultTable")]//tr[not(@style)]'
        )
        for row in document_rows:
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

    def get_filing_next_page_anchor(self, response):
        """
            Return href of the next page anchor
            in pagination
        """
        first_page_anchor_selector = '//*[contains(@class, "pagination")]/*/a/@href'
        anchor_selector = '//*[contains(@class,"pagination")]/*/a/following-sibling::a/@href'
        return response.xpath(first_page_anchor_selector).get()\
            if response.meta["first_page"] \
            else response.xpath(anchor_selector).get()

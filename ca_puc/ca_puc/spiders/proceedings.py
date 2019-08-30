# -*- coding: utf-8 -*-
"""
    This module implements a spider that crawls proceedings for a
    given time period from the following website
    http://docs.cpuc.ca.gov/
"""
import re
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.exceptions import CloseSpider

from ..items import CaPucItem


class ProceedingsSpider(scrapy.Spider):
    name = 'proceedings'
    search_form_url = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx/'
    proceeding_details_base_url = 'https://apps.cpuc.ca.gov/apex/f?p=401:{}:'\
        '666746862207::NO:RP,57,RIR:P5_PROCEEDING_SELECT:'
    proceeding_details_url = proceeding_details_base_url.format('56')
    filings_url = proceeding_details_base_url.format('57')
    start_urls = [search_form_url]

    def __init__(self, start_date, end_date):
        self.validate_date_arguments(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date
        self.p_instance = None
        self.p_flow_id = None
        self.p_flow_step_id = None
        self.proceeding_set = set()
        self.cookiejar_count = 0

    def parse(self, response):
        """
            Get the search form and send a form request with
            given time period
        """
        # creating a form data for request
        form_data = {
            'FilingDateFrom': self.start_date,
            'FilingDateTo': self.end_date,
        }
        # returning a Form Request
        return scrapy.FormRequest.from_response(
            response,
            url=self.search_form_url,
            formdata=form_data,
            callback=self.parse_proceedings
        )

    def parse_proceedings(self, response):
        """
            Get the search results and collect id from the page
            and send request to next page for pagination
        """
        view_state, \
            view_state_generator, \
            event_validation = self.get_form_states(response)
        proceeding_ids = self.get_proceeding_ids(response)
        response.meta.setdefault('proceeding_ids', []).extend(proceeding_ids)

        lnkNextPage = response.xpath('//a[@id="lnkNextPage"]')
        if not lnkNextPage:
            self.proceeding_set = set(response.meta.get('proceeding_ids'))
            self.cookiejar_count += 1
            return scrapy.Request(
                url='{}{}'.format(
                    self.proceeding_details_url,
                    self.proceeding_set.pop()
                ),
                callback=self.parse_proceedings_details,
                meta={'cookiejar': self.cookiejar_count},
            )
        # else:
        form_data = {
            '__EVENTTARGET': 'lnkNextPage',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': view_state_generator,
            '__EVENTVALIDATION': event_validation
        }

        return scrapy.FormRequest(
            url='http://docs.cpuc.ca.gov/SearchRes.aspx',
            formdata=form_data,
            callback=self.parse_proceedings,
            meta=response.meta
        )

    def parse_proceedings_details(self, response):
        """
            Load the item with given data on this proceeding
            detail page and send a request to parse filings for
            a given proceeding

            meta_data: loader:ItemLoader
        """
        loader = ItemLoader(item=CaPucItem(), response=response)
        loader.add_css('filed_on', '#P56_FILING_DATE::text')
        loader.add_css('assignees', '#P56_STAFF::text')
        loader.add_css('industries', '#P56_INDUSTRY::text')
        loader.add_css('filed_by', '#P56_FILED_BY::text')
        loader.add_css('proceeding_type', '#P56_CATEGORY::text')
        loader.add_css('title', '#P56_DESCRIPTION::text')
        loader.add_css('status', '#P56_STATUS::text')
        loader.add_css('state_id', 'h1::text')

        self.cookiejar_count += 1
        return scrapy.Request(
            url='{}{}'.format(
                self.filings_url,
                loader.load_item()['state_id']
            ),
            callback=self.parse_filings,
            meta={
                'loader': loader,
                'cookiejar': self.cookiejar_count
            }
        )

    def parse_filings(self, response):
        """
            maintains a list of filings by iterating
            through filing rows on the given filing page
            and do pagination for filings

            meta_data: loader:ItemLoader
        """
        # getting filing details
        filings_rows = response.xpath(
            '//*[@class="apexir_WORKSHEET_DATA"]/tr[preceding-sibling::*]')
        for row in filings_rows:
            document_types = row.css('u::text').get()
            document_types = document_types.split(' ') \
                if document_types else []

            documents_link = row.css('td a::attr("href")').get()
            if not documents_link or \
                    re.search('orderadocument', documents_link):
                continue

            filing = {
                "description": row.xpath('td[4]/text()').get(),
                "documents": [],
                "filed_on": row.xpath('td[1]/text()').get(),
                "filing_parties": row.xpath('td[3]/text()').get(),
                "types": document_types,
                "documents_link": documents_link
            }

            response.meta.setdefault('filing_list', []).append(filing)
        # Doing pagination for filings
        return self.do_filings_pagination(response)

    def do_filings_pagination(self, response):
        """
            Doing pagination for filings
            1. check if anchor exists for next page.
            2. create appropriate form data
            3. send form request to navigate
            when completed:
            1. sends the collected list of filings to collect
            documents for respective filings.
        """
        next_page_anchor = self.get_filing_next_page_anchor(response)
        # Sending request for paginations
        if not next_page_anchor:
            # Here we have all filings in a list we will fill them with
            # respective documents
            return self.scrap_filing_for_documents(response)

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
        # returning a Form Request
        return scrapy.FormRequest(
            url="https://apps.cpuc.ca.gov/apex/wwv_flow.show",
            formdata=form_data,
            callback=self.parse_filings,
            dont_filter=True,
            meta=response.meta,
        )

    def scrap_filing_for_documents(self, response):
        """
            Check if all filings are processed
            then
                return proceeding item
                Check if proceeding_set is empty
                then
                    return None
                else
                    send request to next proceeding in the list
            else
                Collect documents for individual filings

        """
        self.cookiejar_count += 1
        if not response.meta.get('filing_list'):
            if not self.proceeding_set:
                return response.meta['loader'].load_item()

            return (
                response.meta['loader'].load_item(),
                scrapy.Request(
                    url='{}{}'.format(
                        self.proceeding_details_url,
                        self.proceeding_set.pop()
                    ),
                    callback=self.parse_proceedings_details,
                    meta={'cookiejar': self.cookiejar_count},
                )
            )

        return scrapy.Request(
            url=filing.get('documents_link'),
            callback=self.parse_documents,
            meta={
                'cookiejar': self.cookiejar_count,
                'filing': response.meta.get('filing_list').pop(),
                'filing_list': response.meta.get('filing_list'),
                'loader': response.meta.get('loader')
            },
            dont_filter=True
        )

    def parse_documents(self, response):
        """
            Iterate through document rows on the given document page
            and update the filing with the respective documents.
            Finally, send request to process next filing in the list.
        """
        loader, filing = response.meta.get("loader"), \
            response.meta.get("filing")

        filing = self.get_filing_with_documents(response, filing)
        filings = loader.load_item().setdefault('filings', []).append(filing)
        loader.replace_value('filings', filings)
        # scraping next filing for documents
        return self.scrap_filing_for_documents(response)

    def get_filing_with_documents(self, response, filing):
        """
            Fetch the documents from response and
            return the updated filing with documents
        """
        document_rows = response.xpath(
            '//table[contains(@id, "ResultTable")]//tr[not(@style)]'
        )
        print("Documents Fetched", len(document_rows))
        for row in document_rows:
            source_url = row.css('.ResultLinkTD a::attr("href")').get()
            document = {
                "name": source_url.split('.')[0].split('/')[-1],
                "extension": source_url.split('.')[1],
                "source_url": row.css('.ResultLinkTD a::attr("href")').get(),
                "title": row.css('.ResultTitleTD::text').get()
            }

            filing.get("documents").append(document)

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
        pagination_text = response.xpath(
            '//*[@class="fielddata"]/text()').get()
        if not pagination_text:
            return

        current_limit = pagination_text.split('-')[-1].split('of')[0].strip()
        total_filings = pagination_text.split('of')[-1].strip()
        anchors = response.xpath(
            '//*[@class="fielddata"]/a/@href').getall()

        return anchors[-1] if int(current_limit) < int(total_filings) else None

    def validate_date_arguments(self, start_date, end_date):
        date_format = "%m/%d/%Y"
        try:
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)
        except ValueError as err:
            raise CloseSpider("Invalid date format. Use mm/dd/yyyy")

        if start_date > end_date:
            raise CloseSpider("start date should be lower than end date")

        return True

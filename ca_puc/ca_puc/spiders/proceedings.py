# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from pprint import pprint
import re

from ..items import CaPucItem


class ProceedingsSpider(scrapy.Spider):
    """Spider that crawls proceedings for a given time period"""
    name = 'proceedings'
    search_form_url = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx/'
    proceeding_details_base_url = 'https://apps.cpuc.ca.gov/apex/f?p=401:{}:'\
        '666746862207::NO:RP,57,RIR:P5_PROCEEDING_SELECT:'
    proceeding_details_url = proceeding_details_base_url.format('56')
    filings_url = proceeding_details_base_url.format('57')
    start_urls = [search_form_url]
    # download_delay = 5

    def start_requests(self):
        """
            Fetch the JS rendered Search Form and
            send the response to parse method
        """
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='render.html',
                args={
                    'wait': 0.5
                }
            )

    def parse(self, response):
        """
            Get the search form and send a form request with
            given time period
        """
        # getting the view state
        view_state, \
            view_state_generator,   \
            event_validation = self.get_form_states(response)

        # creating a form data for request
        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'FilingDateFrom': '02/21/19',
            'FilingDateTo': '02/26/19',
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': view_state_generator,
            '__EVENTVALIDATION': event_validation,
            'IndustryID': '-1',
            'ddlCpuc01Types': '-1',
            'SearchButton': 'Search'
        }
        # yielding a Form Request
        yield SplashFormRequest(
            url=self.search_form_url,
            formdata=form_data,
            callback=self.parse_proceedings
        )

    def parse_proceedings(self, response):
        """
            Get the search results and send an
            individual request for each proceeding id
        """
        proceeding_ids = self.get_proceeding_ids(response)
        for p_id in proceeding_ids:
            yield SplashRequest(
                url='{}{}'.format(self.proceeding_details_url, p_id),
                callback=self.parse_proceedings_details,
                meta={'proceeding_id': p_id},
                endpoint='render.html',
                args={
                    'wait': 0.5
                }
            )

    def parse_proceedings_details(self, response):
        """
            Load the item with given data on this proceeding
            detail page and send a request to parse filings for
            a given proceeding

            meta_data: loader:ItemLoader
        """
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
        filings_rows = response.xpath('//*[@class="apexir_WORKSHEET_DATA"]/tr')
        # update loaders with meta data of filing count and total filings
        # len - 2 because we are ignoring the header row
        loader.add_value('total_filing_count', len(filings_rows) - 2)
        loader.add_value('filing_count', 0)

        for row in filings_rows[1:]:
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
                meta={'loader': loader, 'filing': filing}
            )

    def parse_documents(self, response):
        """
            Iterate through document rows on the given document page
            and update the filing with the respective documents.
            Finally, return the completely populated item if all filings
            are processed.

            return required item
        """
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
            item = loader.load_item()
            del item['total_filing_count']
            del item['filing_count']
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
        for row in rows:
            source_url = row.css('.ResultLinkTD a::attr("href")').get()
            title = row.css('.ResultTitleTD::text').get()
            name = source_url.split('.')[0].split('/')[-1]
            extenion = source_url.split('.')[1]

            document = {
                "name": name,
                "extension": extenion,
                "source_url": source_url,
                "title": title
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
        view_state = response.css(
            'input[name="__VIEWSTATE"]::attr(value)').get()
        view_state_generator = response.css(
            'input[name="__VIEWSTATEGENERATOR"]::attr(value)').get()
        event_validation = response.css(
            'input[name="__EVENTVALIDATION"]::attr(value)').get()

        return view_state, view_state_generator, event_validation

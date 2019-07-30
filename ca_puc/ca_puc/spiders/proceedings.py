# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from pprint import pprint
import re

from ..items import CaPucItem


class ProceedingsSpider(scrapy.Spider):
    name = 'proceedings'
    search_form_url = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx/'
    proceeding_details_url = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:666746862207::NO:RP,57,RIR:P5_PROCEEDING_SELECT:'
    filings_url = 'https://apps.cpuc.ca.gov/apex/f?p=401:57:666746862207::NO:RP,57,RIR:P5_PROCEEDING_SELECT:'
    start_urls = [search_form_url]
    # download_delay = 3

    def start_requests(self):
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
        # getting the view state
        view_state = response.css(
            'input[name="__VIEWSTATE"]::attr(value)').get()
        view_state_generator = response.css(
            'input[name="__VIEWSTATEGENERATOR"]::attr(value)').get()
        event_validation = response.css(
            'input[name="__EVENTVALIDATION"]::attr(value)').get()

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
        proceeding_id = response.meta['proceeding_id']

        item = CaPucItem()
        item["_id"] = response.css(
            'div.rounded-corner-region::attr("id")').get()
        item["filed_on"] = response.css('#P56_FILING_DATE::text').get()
        item["assignees"] = response.css('#P56_STAFF::text').get()
        item["industries"] = response.css('#P56_INDUSTRY::text').get()
        item["filed_by"] = response.css('#P56_FILED_BY::text').get()
        item["proceeding_type"] = response.css('#P56_CATEGORY::text').get()
        item["title"] = response.css('#P56_DESCRIPTION::text').get()
        item["status"] = response.css('#P56_STATUS::text').get()
        item["state_id"] = response.css('h1::text').get().split('-')[0].strip()
        item["filings"] = []

        yield scrapy.Request(
            url='{}{}'.format(self.filings_url, proceeding_id),
            callback=self.parse_filings,
            meta={'item': item}
        )

    def parse_filings(self, response):
        item = response.meta['item']
        # getting filing details
        filings_rows = response.xpath('//*[@class="apexir_WORKSHEET_DATA"]/tr')
        for row in filings_rows[1:]:
            filing_date = row.xpath('td[1]/text()').get()
            filed_by = row.xpath('td[3]/text()').get()
            description = row.xpath('td[4]/text()').get()
            document_type = row.css('u::text').get()

            filing = {
                "description": description,
                "documents": [],
                "filed_on": filing_date,
                "filing_parties": filed_by,
                "types": document_type
            }

            # Getting doucments for each filing
            # documents_link = 'http://docs.cpuc.ca.gov/SearchRes.aspx?DocFormat=ALL&DocID=309875317'
            documents_link = row.css('td a::attr("href")').get()

            yield SplashRequest(
                url=documents_link,
                callback=self.parse_documents,
                meta={'item': item, 'filing': filing}
            )
# TODO: PARSING DOCUMENTS and storing them in respective filings

    def parse_documents(self, response):
        item, filing = response.meta['item'], response.meta["filing"]
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

        item["filings"] = filing

        return item

    def get_proceeding_ids(self, response):
        ids = []
        proceedings_selector = '//*[@class="ResultTitleTD"]/text()[2]'
        for proceeding in response.xpath(proceedings_selector).getall():
            ids += re.findall('\w\d{7}', proceeding)

        return ids

import re

import scrapy
from CAPUC.items import Item
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags


class CapucParseSpider(scrapy.Spider):
    name = 'capuc-parser'

    proceeding_filings_url_t = 'https://apps.cpuc.ca.gov/apex/f?p=401:57:0::NO'

    def parse(self, response):

        item = Item()
        item['_id'] = self.extract_id(response)
        item['filed_on'] = self.extract_proceeding_filing_date(response)
        item['source_title'] = self.extract_title(response)
        item['source_url'] = self.extract_proceeding_url(response)
        item['state_id'] = self.extract_state_id(response)
        item['status'] = self.extract_proceeding_status(response)
        item['assignees'] = self.extract_proceeding_assignees(response)
        item['industries'] = self.extract_proceeding_industries(response)
        item['major_parties'] = self.extract_major_parties(response)
        item['proceeding_type'] = self.extract_proceeding_type(response)
        item['uploaded'] = 'true'
        item['state'] = 'CA'
        item['filings'] = []
        item['meta'] = []

        yield Request(self.proceeding_filings_url_t, meta={'item': item}, callback=self.parse_proceeding_filings)

    def parse_proceeding_filings(self, response):
        filings = {}
        item = response.meta['item']

        proceeding_filings = response.css('.apexir_WORKSHEET_DATA')
        for raw_filing in proceeding_filings.css('tr'):
            filings['filed_on'] = self.extract_filing_date(raw_filing)
            filings['source_filing_parties'] = self.extract_filing_parties(raw_filing)
            filings['description'] = self.extract_filing_description(raw_filing)
            filings['meta'] = {'docs_request': self.extract_docs_requests(raw_filing)}

            item['meta'].append(filings)

        return self.next_filing_or_item(item)

    def next_filing_or_item(self, item):
        if item['meta']:
            filing = item['meta'].pop(0)
            if filing['meta']:
                request = filing['meta'].get('docs_request')
                request.meta['item'] = item
                request.meta['filing'] = filing
                yield request

        else:
            yield item

    def extract_filing_docs(self, response):

        item = response.meta['item']
        filing = response.meta['filing']
        filings_titles = self.extract_filings_titles(response)
        filings_docs_links = self.extract_filings_docs_links(response)

        for raw_filing in zip(filings_titles, filings_docs_links):
            filing['source_url'] = '{}{}'.format('http://docs.cpuc.ca.gov', self.extract_filing_source_url(raw_filing))
            filing['title'] = raw_filing[0]
            filing['blob_name'] = "{}-{}-{}".format(item['state'], item['state_id'],
                                                    filing['source_url'].split('/')[-1])
            filing['extension'] = filing['source_url'].split('.')[-1]
            filing['name'] = filing['source_url'].split('/')[-1]


        item['filings'].append(filing)

        return self.next_filing_or_item(item)

    def extract_id(self, response):
        return response.css('.rounded-corner-region::attr(id)').extract_first()

    def extract_proceeding_filing_date(self, response):
        return response.css('#P56_FILING_DATE::text').extract_first()

    def extract_title(self, response):
        return response.css('#P56_DESCRIPTION::text').extract_first()

    def extract_proceeding_url(self, response):
        return response.url

    def extract_state_id(self, response):
        return response.css('div.rc-content-main h1::text').extract_first().split('-')[0]

    def extract_proceeding_status(self, response):
        return response.css('#P56_STATUS::text').extract_first()

    def extract_proceeding_assignees(self, response):
        return response.css('#P56_STAFF::text').extract_first()

    def extract_proceeding_industries(self, response):
        return response.css('#P56_INDUSTRY::text').extract_first()

    def extract_major_parties(self, response):
        return response.css('#P56_FILED_BY::text').extract_first()

    def extract_proceeding_type(self, response):
        return response.css('#P56_CATEGORY::text').extract_first()

    def extract_filing_date(self, raw_filing):
        return raw_filing.css('td[headers="FILING_DATE"]::text').extract_first()

    def extract_filing_parties(self, raw_filing):
        return raw_filing.css('td[headers="FILED_BY"]::text').extract_first()

    def extract_filing_description(self, raw_filing):
        return raw_filing.css('td[headers="DESCRIPTION"]::text').extract_first()

    def extract_docs_requests(self, raw_filing):
        if raw_filing.css('td[headers="DOCUMENT_TYPE"] a::attr(href)').extract_first():
            return Request(raw_filing.css('td[headers="DOCUMENT_TYPE"] a::attr(href)').extract_first(),
                           dont_filter=True, callback=self.extract_filing_docs)

    def extract_filings_titles(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        raw_titles = soup.find_all("td", class_="ResultTitleTD")

        return [remove_tags(title.contents[0]) for title in raw_titles]

    def extract_filings_docs_links(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        raw_links = soup.find_all("td", class_="ResultLinkTD")

        return [link.contents[0] for link in raw_links]

    def extract_filing_source_url(self, raw_filing):
        return re.findall(r'(\/PublishedDocs.*?")', str(raw_filing[1]))[0].strip('"')


class SavageCrawlSpider(CrawlSpider):
    name = 'capuc-crawler'

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36" \
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    base_url_t = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx'
    proceeding_url_t = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:12117329809176::NO:RP,57,RIR:P5_PROCEEDING_SELECT'

    capuc_parser = CapucParseSpider()

    def start_requests(self):

        formdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUKLTk2MTY0MzkwOQ9kFgICBQ9kFgYCCQ8QDxYGHg5EYXRhVmFsdWVGaWVsZAUJRG9jVHlwZUlEHg1EYXRhVGV4dEZpZWxkBQtEb2NUeXBlRGVzYx4LXyFEYXRhQm91bmRnZBAVEA4tLVNlbGVjdCBPbmUtLQZBZ2VuZGEORGFpbHkgQ2FsZW5kYXIPQWdlbmRhIERlY2lzaW9uEENvbW1lbnQgRGVjaXNpb24ORmluYWwgRGVjaXNpb24NR2VuZXJhbCBPcmRlciZJdGVtIGZvciBsZWdpc2xhdGl2ZSBzZWN0aW9uIG9mIGFnZW5kYQxOZXdzIFJlbGVhc2UGUmVwb3J0EUFnZW5kYSBSZXNvbHV0aW9uEkNvbW1lbnQgUmVzb2x1dGlvbhBGaW5hbCBSZXNvbHV0aW9uH1J1bGVzIG9mIFByYWN0aWNlIGFuZCBQcm9jZWR1cmUGUnVsaW5nFUUtRmlsZWQgRG9jdW1lbnQgVHlwZRUQAi0xATEBOQIxNwIxOAIxOQIyOQIzMgI0MAI1MAI1MwI1NAI1NQI1NwI1OAItNRQrAxBnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCCw8QDxYGHwAFCURvY1R5cGVJRB8BBQtEb2NUeXBlRGVzYx8CZ2QPFk0CAQICAgMCBAIFAgYCBwIIAgkCCgILAgwCDQIOAg8CEAIRAhICEwIUAhUCFgIXAhgCGQIaAhsCHAIdAh4CHwIgAiECIgIjAiQCJQImAicCKAIpAioCKwIsAi0CLgIvAjACMQIyAjMCNAI1AjYCNwI4AjkCOgI7AjwCPQI+Aj8CQAJBAkICQwJEAkUCRgJHAkgCSQJKAksCTAJNFk0QBQ5BTEogUmVzb2x1dGlvbgUDMTMwZxAFCUFsdGVybmF0ZQUCNjlnEAUTQW1lbmRlZCBBcHBsaWNhdGlvbgUCNjdnEAURQW1lbmRlZCBDb21wbGFpbnQFAjY4ZxAFCUFtZW5kbWVudAUCNzBnEAUGQW5zd2VyBQI3MWcQBQZBcHBlYWwFAjcyZxAFFUFwcGVhbCBDYXRlZ29yaXphdGlvbgUCNzNnEAULQXBwbGljYXRpb24FAjY2ZxAFFUFyYml0cmF0aW9uIEFncmVlbWVudAUCNzVnEAURQXJiaXRyYXRvciBSZXBvcnQFAjc0ZxAFCEFzc2lnbmVkBQI3NmcQBQVCcmllZgUCNzdnEAUIQ2FsZW5kYXIFAjgwZxAFFkNlcnRpZmljYXRlIG9mIFNlcnZpY2UFAjg1ZxAFCENvbW1lbnRzBQI4MmcQBRVDb21tZW50cyBvbiBBbHRlcm5hdGUFAjgzZxAFGENvbW1pc3Npb24gSW52ZXN0aWdhdGlvbgUCOTlnEAUVQ29tbWlzc2lvbiBSdWxlbWFraW5nBQMxMTJnEAUJQ29tcGxhaW50BQI3OGcQBRBDb21wbGFpbnQgQW5zd2VyBQI3OWcQBRFDb21wbGlhbmNlIEZpbGluZwUCODFnEAUYQ29uc29saWRhdGVkIFByb2NlZWRpbmdzBQI4NGcQBQlEZWZlbmRhbnQFAjg2ZxAFEURlbmlhbCBvZiBFeHBhcnRlBQI5MmcQBQ5EcmFmdCBEZWNpc2lvbgUCODdnEAUKRXhjZXB0aW9ucwUCOTRnEAUHRXhoaWJpdAUCOTNnEAUHRXhwYXJ0ZQUCOTVnEAUORmVlIC0gUnVsZSAyLjUFAjk4ZxAFBEZlZXMFAjk2ZxAFDklkZW50aWZpY2F0aW9uBQMxMDBnEAUHSW1wb3VuZAUDMTAxZxAFFUluc3RydWN0aW9uIHRvIEFuc3dlcgUDMTAyZxAFG0luc3RydWN0aW9uIHRvIEFuc3dlciBTQjk2MAUDMTAzZxAFDExhdyAmIE1vdGlvbgUDMTA0ZxAFCk1lbW9yYW5kdW0FAzEwNWcQBRRNaXNjZWxsYW5lb3VzIEZpbGluZwUDMTA2ZxAFBk1vdGlvbgUDMTA3ZxAFF01vdGlvbiBmb3IgUmVhc3NpZ25tZW50BQMxMjNnEAUJTk9JIEZpbGVkBQMxMDhnEAUMTk9JIFRlbmRlcmVkBQMxNDRnEAUGTm90aWNlBQMxMDlnEAUQTm90aWNlIG9mIERlbmlhbAUCOTFnEAUJT2JqZWN0aW9uBQMxMTFnEAUKT3Bwb3NpdGlvbgUDMTEzZxAFBU9yZGVyBQMxMTBnEAUIUGV0aXRpb24FAzExOGcQBRlQZXRpdGlvbiBmb3IgTW9kaWZpY2F0aW9uBQMxMjBnEAUoUGV0aXRpb24gVG8gQWRvcHQgQW1lbmQgT3IgUmVwZWFsIFJlZ3VsLgUDMTIyZxAFH1ByZWhlYXJpbmcgQ29uZmVyZW5jZSBTdGF0ZW1lbnQFAzExOWcQBRtQcmVzaWRpbmcgT2ZmaWNlcnMgRGVjaXNpb24FAzEyMWcQBRNQcmltYXJ5IFBhcnRpY2lwYW50BQMxMTVnEAUjUHJvcG9uZW50cyBFbnZpcm9ubWVudGFsIEFzc2Vzc21lbnQFAzExN2cQBRFQcm9wb3NlZCBEZWNpc2lvbgUDMTE2ZxAFB1Byb3Rlc3QFAzExNGcQBQpSZWFzc2lnbmVkBQMxMjZnEAUMUmVjYWxlbmRhcmVkBQMxMjVnEAURUmVoZWFyaW5nIFJlcXVlc3QFAzEyNGcQBRBSZWplY3Rpb24gTGV0dGVyBQMxMzNnEAUFUmVwbHkFAzEyN2cQBQZSZXBvcnQFAzEyOGcQBQdSZXF1ZXN0BQMxMjlnEAUhUmVzb2x1dGlvbiBBTEotMTc2IENhdGVnb3JpemF0aW9uBQMxMzFnEAUIUmVzcG9uc2UFAzEzMmcQBQZSdWxpbmcFAzEzNmcQBQ5TY29waW5nIFJ1bGluZwUDMTM1ZxAFCVN0YXRlbWVudAUDMTM4ZxAFC1N0aXB1bGF0aW9uBQMxMzlnEAUIU3VicG9lbmEFAzE0MGcQBQpTdXBwbGVtZW50BQMxNDFnEAUMU3VwcGxlbWVudGFsBQMxMzdnEAUlU3VwcGxlbWVudGFsIENvbnNvbGlkYXRlZCBQcm9jZWVkaW5ncwUDMTQyZxAFE1N1cHBvcnRpbmcgRG9jdW1lbnQFAzE0N2cQBQlUZXN0aW1vbnkFAzE0M2cQBQpUcmFuc2NyaXB0BQMxNDVnEAUKV2l0aGRyYXdhbAUDMTQ2Z2RkAg8PEA8WBh8ABQpJbmR1c3RyeUlEHwEFDEluZHVzdHJ5TmFtZR8CZ2QPFgcCAQICAgMCBAIFAgYCBxYHEAUGRW5lcmd5BQExZxAFDlRyYW5zcG9ydGF0aW9uBQEyZxAFC1dhdGVyL1Nld2VyBQEzZxAFDkNvbW11bmljYXRpb25zBQE0ZxAFBU90aGVyBQE1ZxBlBQIxNGcQBQ5NdWx0aXBsZSBUeXBlcwUCMTVnZGRk17UOPgZaN43R4YOU/jocHfbUjzvVGWNhRTMGlEL9MsM=',
            '__EVENTVALIDATION': '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',
            ' __VIEWSTATEGENERATOR': '6DB12421',
            'DocTitle': '',
            'ddlCpuc01Types': '-1',
            'IndustryID': '-1',
            'ProcNum': '',
            'MeetDate': '',
            'PubDateFrom': '',
            'PubDateTo': '',
            'EfileConfirmNum': '',
            'FilingDateFrom': '10/01/17',
            'FilingDateTo': '10/16/18',
            'SearchButton': 'Search',
        }

        yield FormRequest(self.base_url_t, formdata=formdata, callback=self.parse_proceeding)

    def parse_proceeding(self, response):
        proceeding_ids = self.extract_proceeding_ids(response)

        for proceeding in proceeding_ids:
            yield Request('{}:{}'.format(self.proceeding_url_t, proceeding), callback=self.capuc_parser.parse)

    def extract_proceeding_ids(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        raw_proceedings = soup.find_all("td", class_="ResultTitleTD")
        for rp in raw_proceedings:
            proceeding = str(rp.contents[-1])
            clean_proceeding = remove_tags(proceeding)
            raw_proceeding_ids = re.findall((r": [A-Z].*[0-9]"), clean_proceeding)
            proceeding_ids = raw_proceeding_ids[0].split(';')

            return [proceeding.strip(': ') for proceeding in proceeding_ids]

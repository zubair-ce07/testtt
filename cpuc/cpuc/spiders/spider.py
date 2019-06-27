
import scrapy
from scrapy import FormRequest
from cpuc.RequestManager import RequestManager
from cpuc.items import Document, ProceedingDetail, Filing


class CpucSpider(scrapy.Spider):
    name = "cpuc"
    pbar = ""
    allowed_domains = ['cpuc.ca.gov']
    request_manager = RequestManager()
    start_urls = ['http://docs.cpuc.ca.gov/advancedsearchform.aspx']

    def parse(self, response):
        formdata = {
                    '__EVENTARGUMENT': '',
                    '__EVENTTARGET': '',
                    'FilingDateFrom': '06/20/19',
                    'FilingDateTo': '06/21/19',
                    '__VIEWSTATEGENERATOR': '6DB12421',
                    'DocTitle': '',
                    'ddlCpuc01Types': '-1',
                    'IndustryID': '-1',
                    'ProcNum': '',
                    'MeetDate': '',
                    'PubDateFrom': '',
                    'PubDateTo': '',
                    'EfileConfirmNum': '',
                    'SearchButton': 'Search',
                    '__VIEWSTATE': '/wEPDwUKLTk2MTY0MzkwOQ9kFgICBQ9kFgYCCQ8QDxYGHg5EYXRhVmFsdWVGaWVsZAUJRG9jVHlwZUlEHg1EYXRhVGV4dEZpZWxkBQtEb2NUeXBlRGVzYx4LXyFEYXRhQm91bmRnZBAVEA4tLVNlbGVjdCBPbmUtLQZBZ2VuZGEORGFpbHkgQ2FsZW5kYXIPQWdlbmRhIERlY2lzaW9uEENvbW1lbnQgRGVjaXNpb24ORmluYWwgRGVjaXNpb24NR2VuZXJhbCBPcmRlciZJdGVtIGZvciBsZWdpc2xhdGl2ZSBzZWN0aW9uIG9mIGFnZW5kYQxOZXdzIFJlbGVhc2UGUmVwb3J0EUFnZW5kYSBSZXNvbHV0aW9uEkNvbW1lbnQgUmVzb2x1dGlvbhBGaW5hbCBSZXNvbHV0aW9uH1J1bGVzIG9mIFByYWN0aWNlIGFuZCBQcm9jZWR1cmUGUnVsaW5nFUUtRmlsZWQgRG9jdW1lbnQgVHlwZRUQAi0xATEBOQIxNwIxOAIxOQIyOQIzMgI0MAI1MAI1MwI1NAI1NQI1NwI1OAItNRQrAxBnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCCw8QDxYGHwAFCURvY1R5cGVJRB8BBQtEb2NUeXBlRGVzYx8CZ2QPFk4CAQICAgMCBAIFAgYCBwIIAgkCCgILAgwCDQIOAg8CEAIRAhICEwIUAhUCFgIXAhgCGQIaAhsCHAIdAh4CHwIgAiECIgIjAiQCJQImAicCKAIpAioCKwIsAi0CLgIvAjACMQIyAjMCNAI1AjYCNwI4AjkCOgI7AjwCPQI+Aj8CQAJBAkICQwJEAkUCRgJHAkgCSQJKAksCTAJNAk4WThAFDkFMSiBSZXNvbHV0aW9uBQMxMzBnEAUJQWx0ZXJuYXRlBQI2OWcQBRNBbWVuZGVkIEFwcGxpY2F0aW9uBQI2N2cQBRFBbWVuZGVkIENvbXBsYWludAUCNjhnEAUJQW1lbmRtZW50BQI3MGcQBQZBbnN3ZXIFAjcxZxAFBkFwcGVhbAUCNzJnEAUVQXBwZWFsIENhdGVnb3JpemF0aW9uBQI3M2cQBQtBcHBsaWNhdGlvbgUCNjZnEAUVQXJiaXRyYXRpb24gQWdyZWVtZW50BQI3NWcQBRFBcmJpdHJhdG9yIFJlcG9ydAUCNzRnEAUIQXNzaWduZWQFAjc2ZxAFBUJyaWVmBQI3N2cQBQhDYWxlbmRhcgUCODBnEAUWQ2VydGlmaWNhdGUgb2YgU2VydmljZQUCODVnEAUPQ2l0YXRpb24gQXBwZWFsBQMxNDhnEAUIQ29tbWVudHMFAjgyZxAFFUNvbW1lbnRzIG9uIEFsdGVybmF0ZQUCODNnEAUYQ29tbWlzc2lvbiBJbnZlc3RpZ2F0aW9uBQI5OWcQBRVDb21taXNzaW9uIFJ1bGVtYWtpbmcFAzExMmcQBQlDb21wbGFpbnQFAjc4ZxAFEENvbXBsYWludCBBbnN3ZXIFAjc5ZxAFEUNvbXBsaWFuY2UgRmlsaW5nBQI4MWcQBRhDb25zb2xpZGF0ZWQgUHJvY2VlZGluZ3MFAjg0ZxAFCURlZmVuZGFudAUCODZnEAURRGVuaWFsIG9mIEV4cGFydGUFAjkyZxAFDkRyYWZ0IERlY2lzaW9uBQI4N2cQBQpFeGNlcHRpb25zBQI5NGcQBQdFeGhpYml0BQI5M2cQBQdFeHBhcnRlBQI5NWcQBQ5GZWUgLSBSdWxlIDIuNQUCOThnEAUERmVlcwUCOTZnEAUOSWRlbnRpZmljYXRpb24FAzEwMGcQBQdJbXBvdW5kBQMxMDFnEAUVSW5zdHJ1Y3Rpb24gdG8gQW5zd2VyBQMxMDJnEAUbSW5zdHJ1Y3Rpb24gdG8gQW5zd2VyIFNCOTYwBQMxMDNnEAUMTGF3ICYgTW90aW9uBQMxMDRnEAUKTWVtb3JhbmR1bQUDMTA1ZxAFFE1pc2NlbGxhbmVvdXMgRmlsaW5nBQMxMDZnEAUGTW90aW9uBQMxMDdnEAUXTW90aW9uIGZvciBSZWFzc2lnbm1lbnQFAzEyM2cQBQlOT0kgRmlsZWQFAzEwOGcQBQxOT0kgVGVuZGVyZWQFAzE0NGcQBQZOb3RpY2UFAzEwOWcQBRBOb3RpY2Ugb2YgRGVuaWFsBQI5MWcQBQlPYmplY3Rpb24FAzExMWcQBQpPcHBvc2l0aW9uBQMxMTNnEAUFT3JkZXIFAzExMGcQBQhQZXRpdGlvbgUDMTE4ZxAFGVBldGl0aW9uIGZvciBNb2RpZmljYXRpb24FAzEyMGcQBShQZXRpdGlvbiBUbyBBZG9wdCBBbWVuZCBPciBSZXBlYWwgUmVndWwuBQMxMjJnEAUfUHJlaGVhcmluZyBDb25mZXJlbmNlIFN0YXRlbWVudAUDMTE5ZxAFG1ByZXNpZGluZyBPZmZpY2VycyBEZWNpc2lvbgUDMTIxZxAFE1ByaW1hcnkgUGFydGljaXBhbnQFAzExNWcQBSNQcm9wb25lbnRzIEVudmlyb25tZW50YWwgQXNzZXNzbWVudAUDMTE3ZxAFEVByb3Bvc2VkIERlY2lzaW9uBQMxMTZnEAUHUHJvdGVzdAUDMTE0ZxAFClJlYXNzaWduZWQFAzEyNmcQBQxSZWNhbGVuZGFyZWQFAzEyNWcQBRFSZWhlYXJpbmcgUmVxdWVzdAUDMTI0ZxAFEFJlamVjdGlvbiBMZXR0ZXIFAzEzM2cQBQVSZXBseQUDMTI3ZxAFBlJlcG9ydAUDMTI4ZxAFB1JlcXVlc3QFAzEyOWcQBSFSZXNvbHV0aW9uIEFMSi0xNzYgQ2F0ZWdvcml6YXRpb24FAzEzMWcQBQhSZXNwb25zZQUDMTMyZxAFBlJ1bGluZwUDMTM2ZxAFDlNjb3BpbmcgUnVsaW5nBQMxMzVnEAUJU3RhdGVtZW50BQMxMzhnEAULU3RpcHVsYXRpb24FAzEzOWcQBQhTdWJwb2VuYQUDMTQwZxAFClN1cHBsZW1lbnQFAzE0MWcQBQxTdXBwbGVtZW50YWwFAzEzN2cQBSVTdXBwbGVtZW50YWwgQ29uc29saWRhdGVkIFByb2NlZWRpbmdzBQMxNDJnEAUTU3VwcG9ydGluZyBEb2N1bWVudAUDMTQ3ZxAFCVRlc3RpbW9ueQUDMTQzZxAFClRyYW5zY3JpcHQFAzE0NWcQBQpXaXRoZHJhd2FsBQMxNDZnZGQCDw8QDxYGHwAFCkluZHVzdHJ5SUQfAQUMSW5kdXN0cnlOYW1lHwJnZA8WBwIBAgICAwIEAgUCBgIHFgcQBQZFbmVyZ3kFATFnEAUOVHJhbnNwb3J0YXRpb24FATJnEAULV2F0ZXIvU2V3ZXIFATNnEAUOQ29tbXVuaWNhdGlvbnMFATRnEAUFT3RoZXIFATVnEGUFAjE0ZxAFDk11bHRpcGxlIFR5cGVzBQIxNWdkZGQrMOijrhj2nAD696/Nqu10v92XtvVvSDLWV5SpZjUXRw==',
                    '__EVENTVALIDATION': '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'
                    }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        method='POST',
                                        callback=self.parse_all_proceeding_number,
                                        meta={'proceeding_num': set(), 'page_no': 0})

    def parse_all_proceeding_number(self, response):
        current_page = int(response.meta['page_no'])
        __EVENT_TARGET = ""
        if current_page < 10:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format("0"+str(current_page+1))
        elif current_page > 9:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format(str(current_page+1))

        total_pages = int(response.xpath("//table[@id='Pages']//tr/td[position()=2]/a[last()]/text()").get())

        if current_page < total_pages:
            proceeding_num = response.meta['proceeding_num']
            table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr")
            skip = False
            for row in table_rows:
                if not skip:
                    proceeding_number = row.xpath("td[@class='ResultTitleTD']/text()")[1].get()
                    len_str = len(proceeding_number)
                    proceeding_number = proceeding_number[12: len_str]
                    if len(proceeding_number) > 8:
                        proceeding_number = proceeding_number[0:8]
                    proceeding_num.add(proceeding_number)
                    skip = True
                else:
                    skip = False
            formdata = {
                '__EVENTTARGET': __EVENT_TARGET,
                '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            }
            yield FormRequest(
                url='http://docs.cpuc.ca.gov/SearchRes.aspx',
                formdata=formdata,
                callback=self.parse_all_proceeding_number,
                meta={'page_no': current_page+1, 'proceeding_num': response.meta['proceeding_num']}
            )

        else:
            proceeding_num = response.meta['proceeding_num']
            print("PROCEEDING # {}".format(proceeding_num))
            while proceeding_num:
                num = proceeding_num.pop()
                next_page = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:6062906969229::NO:RP,57,RIR' \
                            ':P5_PROCEEDING_SELECT:{}'.format(num)
                yield response.follow(next_page,
                                      callback=self.parse_proceeding_number)

    def parse_proceeding_number(self, response):
        proceeding_details = ProceedingDetail()
        table_rows = response.xpath("//table[@id='apex_layout_1757486743389754952']/tr")
        filling_parties = list()
        for filled_party in table_rows.xpath("td[position()=2]//span[@id='P56_FILED_BY']/text()"):
            filling_parties.append(filled_party.get())

        proceeding_details['filing_parties'] = filling_parties

        industries = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_INDUSTRY']/text()"):
            industries.append(industry.get())
        proceeding_details['industries'] = industries

        proceeding_details['filled_on'] = table_rows.xpath("td[position()=2]//span[@id='P56_FILING_DATE']/text()").get()
        proceeding_details['status'] = table_rows.xpath("td[position()=2]//span[@id='P56_STATUS']/text()").get()
        proceeding_details['proceeding_type'] = table_rows.xpath("td[position()=2]//span[@id='P56_CATEGORY']/text()").get()
        proceeding_details['title'] = table_rows.xpath("td[position()=2]//span[@id='P56_DESCRIPTION']/text()").get()
        proceeding_details['source_url'] = response.url

        assignees = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_STAFF']/text()"):
            assignees.append(industry.get())
        proceeding_details['assignees'] = assignees
        cookie = response.request.headers.getlist("Cookie")
        proceeding_details['filings'] = list()

        yield scrapy.Request(
            url='https://apps.cpuc.ca.gov/apex/f?p=401:57:0::NO',
            callback=self.save_document,
            errback=self.error_back,
            headers={'Cookie': cookie},
            dont_filter=True,
            meta={'item': proceeding_details, 'dont_merge_cookies': True}
        )

    def error_back(self, failure):
        print(failure)

    def save_document(self, response):
        item = response.meta['item']
        filings = Filing()
        table = response.xpath("//div[@id='apexir_DATA_PANEL']//table[@class='apexir_WORKSHEET_DATA']")
        table_rows = table.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for row in table_rows:
            filings['description'] = row.xpath("td[@headers='DESCRIPTION']/text()").get()
            filings['filled_on'] = row.xpath("td[@headers='FILING_DATE']/text()").get()
            filings['types'] = list()
            filings['types'].append(row.xpath("td[@headers='DOCUMENT_TYPE']//u/text()").get())
            filings['filing_parties'] = list()
            filings['filing_parties'].append(row.xpath("td[@headers='FILED_BY']/text()").get())

            document_link = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()
            item = response.meta['item']
            item['filings'].append(filings)
            request = response.follow(document_link,
                                      callback=self.parse_document_page,
                                      meta={'item': response.meta['item'],
                                            'dont_merge_cookies': True})
            self.request_manager.Filing_request.append(request)

        next_btn = response.xpath("//div[@id='apexir_DATA_PANEL']//span[@class='fielddata']/a/@href").get()
        if next_btn:
            formdata = {
                '__EVENTTARGET': 'lnkNextPage',
                '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            }

            next_page_request_parameters = {
                'formdata': formdata,
                'method': 'POST',
                'url': response,
                'callback': self.save_document
            }
            self.request_manager.next_page = next_page_request_parameters
        else:
            self.request_manager.next_page = None

        if len(self.request_manager.Filing_request) > 0:
            yield self.request_manager.Filing_request.pop()
        else:
            yield {'docket': item}

    def parse_document_page(self, response):
        item = response.meta['item']
        table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr")
        skip = False
        document_list = list()
        for row in table_rows:
            if not skip:
                document = Document()
                document['title'] = row.xpath("td[@class='ResultTitleTD']/text()").get()
                document['source_url'] = "http://docs.cpuc.ca.gov{}".format(row.xpath("td[@class="
                                                                                      "'ResultLinkTD']/a/@href").get())
                document['extension'] = row.xpath("td[@class='ResultLinkTD']/a/text()").get()
                document_list.append(document)
                skip = True
            else:
                skip = False

        item['filings'][len(item['filings'])-1]['documents'] = document_list

        if len(self.request_manager.Filing_request) > 0:
            yield self.request_manager.Filing_request.pop()

        elif len(self.request_manager.Filing_request) == 0:
            yield FormRequest.from_response(self.request_manager.next_page['url'],
                                            formdata=self.request_manager.next_page['formdata'],
                                            method=self.request_manager.next_page['method'],
                                            callback=self.request_manager.next_page['callback'],
                                            meta={'item': item, 'dont_merge_cookies': True})


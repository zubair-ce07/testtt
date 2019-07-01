import logging
import re

import scrapy
from scrapy import FormRequest
from cpuc.RequestManager import RequestManager
from cpuc.items import Document, ProceedingDetail, Filing


class CpucSpider(scrapy.Spider):
    name = "cpuc"
    allowed_domains = ['cpuc.ca.gov']
    request_manager = RequestManager()
    start_urls = ['http://docs.cpuc.ca.gov/advancedsearchform.aspx']

    def parse(self, response):
        formdata = {
                    'FilingDateFrom': '06/20/19',
                    'FilingDateTo': '06/21/19',
                    '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                    'SearchButton': 'Search',
                    '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                    '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get(),
                    }
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        method='POST',
                                        callback=self.parse_all_proceeding_number,
                                        meta={'proceeding_set': set(), 'page_no': 0})

    @staticmethod
    def get_filling_parties(table_rows, proceeding_details):
        filling_parties = list()
        for filled_party in table_rows.xpath("td[position()=2]//span[@id='P56_FILED_BY']/text()"):
            filling_parties.append(filled_party.get())
        proceeding_details['filing_parties'] = filling_parties

    @staticmethod
    def get_industries(table_rows, proceeding_details):
        industries = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_INDUSTRY']/text()"):
            industries.append(industry.get())
        proceeding_details['industries'] = industries

    @staticmethod
    def get_assignees(table_rows, proceeding_details):
        assignees = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_STAFF']/text()"):
            assignees.append(industry.get())
        proceeding_details['assignees'] = assignees

    def parse_all_proceeding_number(self, response):
        page_no = int(response.meta['page_no'])
        __EVENT_TARGET = ""
        if page_no < 10:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format("0"+str(page_no+1))
        elif page_no > 9:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format(str(page_no+1))

        total_pages = int(response.xpath("//table[@id='Pages']//tr/td[position()=2]/a[last()]/text()").get())

        if page_no < total_pages:
            proceeding_set = response.meta['proceeding_set']
            table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
            for row in table_rows:
                proceeding_numbers = row.xpath("td[@class='ResultTitleTD']/text()")[1].get()
                proceeding_numbers = re.findall(r'[A-Z][0-9]{7}', proceeding_numbers)

                for proceeding_number in proceeding_numbers:
                    proceeding_set.add(proceeding_number)
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
                meta={'page_no': page_no+1, 'proceeding_set': proceeding_set}
            )

        else:
            proceeding_num = response.meta['proceeding_set']
            while proceeding_num:
                num = proceeding_num.pop()
                next_page = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:6062906969229::NO:RP,57,RIR' \
                            ':P5_PROCEEDING_SELECT:{}'.format(num)
                yield response.follow(next_page,
                                      callback=self.parse_proceeding_number, meta={'dont_merge_cookies': True})

    def parse_proceeding_number(self, response):
        proceeding_details = ProceedingDetail()
        table_rows = response.xpath("//table[@id='apex_layout_1757486743389754952']/tr")

        self.get_filling_parties(table_rows, proceeding_details)

        self.get_industries(table_rows, proceeding_details)

        proceeding_details['filled_on'] = table_rows.xpath("td[position()=2]//span[@id='P56_FILING_DATE']/text()").get()
        proceeding_details['status'] = table_rows.xpath("td[position()=2]//span[@id='P56_STATUS']/text()").get()
        proceeding_details['proceeding_type'] = table_rows.xpath("td[position()=2]//span[@id='P56_CATEGORY']/text()").get()
        proceeding_details['title'] = table_rows.xpath("td[position()=2]//span[@id='P56_DESCRIPTION']/text()").get()
        proceeding_details['source_url'] = response.url

        self.get_assignees(table_rows, proceeding_details)

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

    @staticmethod
    def error_back(failure):
        logging.exception(failure)

    def save_document(self, response):
        table_rows = response.xpath("//div[@id='apexir_DATA_PANEL']//table[@class='apexir_WORKSHEET_DATA']//"
                                    "tr[@class='even'] | //tr[@class='odd']")
        for row in table_rows:
            filings = Filing()
            filings['description'] = row.xpath("td[@headers='DESCRIPTION']/text()").get()
            filings['filled_on'] = row.xpath("td[@headers='FILING_DATE']/text()").get()
            filings['types'] = row.xpath("td[@headers='DOCUMENT_TYPE']//u/text()").get()

            filings['filing_parties'] = row.xpath("td[@headers='FILED_BY']/text()").get()

            document_link = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()
            item = response.meta['item']
            item['filings'].append(filings)
            request = response.follow(document_link,
                                      callback=self.parse_document_page,
                                      errback=self.error_back,
                                      meta={'item': item, 'dont_merge_cookies': True})
            self.request_manager.filing_requests.append(request)

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

        if self.request_manager.filing_requests:
            yield self.request_manager.filing_requests.pop()

    def parse_document_page(self, response):
        item = response.meta['item']

        table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
        document_list = list()
        for row in table_rows:
            document = Document()
            document['title'] = row.xpath("td[@class='ResultTitleTD']/text()").get()
            document['source_url'] = "http://docs.cpuc.ca.gov{}".format(row.xpath("td[@class="
                                                                                  "'ResultLinkTD']/a/@href").get())
            document['extension'] = row.xpath("td[@class='ResultLinkTD']/a/text()").get()
            document_list.append(document)

        item['filings'][len(item['filings'])-1]['documents'] = document_list
        if len(self.request_manager.filing_requests) > 88:
            yield self.request_manager.filing_requests.pop()
        else:
            if self.request_manager.next_page:
                yield FormRequest.from_response(self.request_manager.next_page['url'],
                                                formdata=self.request_manager.next_page['formdata'],
                                                method=self.request_manager.next_page['method'],
                                                dont_filter=True,
                                                errback=self.error_back,
                                                callback=self.request_manager.next_page['callback'],
                                                meta={'item': item, 'dont_merge_cookies': True})
            else:
                yield {'docket': item}


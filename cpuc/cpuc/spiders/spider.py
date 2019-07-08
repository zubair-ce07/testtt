import logging
import re
from scrapy.loader import ItemLoader
import scrapy
from scrapy import FormRequest

from cpuc.RequestManager import RequestManager
from cpuc.items import Document, ProceedingDetail, Filing


class CpucSpider(scrapy.Spider):
    name = "cpuc"
    allowed_domains = ['cpuc.ca.gov']
    request_manager = RequestManager()
    start_urls = ['http://docs.cpuc.ca.gov/advancedsearchform.aspx']

    @staticmethod
    def get__search_form_data_loaded(response):
        formdata = {
            'FilingDateFrom': '06/20/19',
            'FilingDateTo': '06/21/19',
            '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
            'SearchButton': 'Search',
            '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
            '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get(),
        }
        return formdata

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formdata=self.get__search_form_data_loaded(response),
                                        method='POST',
                                        callback=self.extract_proceeding_docket,
                                        meta={'proceeding_set': set(), 'page_no': 0})

    @staticmethod
    def get_filling_parties(table_rows, docket_loader):
        filling_parties = list()
        for filled_party in table_rows.xpath("td[position()=2]//span[@id='P56_FILED_BY']/text()"):
            filling_parties.append(filled_party.get())
        docket_loader.add_value('filing_parties', filling_parties)

    @staticmethod
    def get_industries(table_rows, docket_loader):
        industries = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_INDUSTRY']/text()"):
            industries.append(industry.get())
        docket_loader.add_value('industries', industries)

    @staticmethod
    def get_assignees(table_rows, docket_loader):
        assignees = list()
        for industry in table_rows.xpath("td[position()=2]//span[@id='P56_STAFF']/text()"):
            assignees.append(industry.get())
        docket_loader.add_value('assignees', assignees)

    @staticmethod
    def get_proceeding_numers(response):
        proceeding_set = response.meta['proceeding_set']
        table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
        for row in table_rows:
            proceeding_numbers = row.xpath("td[@class='ResultTitleTD']/text()")[1].get()
            proceeding_numbers = re.findall(r'[A-Z][0-9]{7}', proceeding_numbers)

            for proceeding_number in proceeding_numbers:
                proceeding_set.add(proceeding_number)
        return proceeding_set

    @staticmethod
    def get_event_target(page_no):
        __EVENT_TARGET = ""
        if page_no < 10:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format("0"+str(page_no+1))
        elif page_no > 9:
            __EVENT_TARGET = 'rptPages$ctl{}$btnPage'.format(str(page_no+1))

        return __EVENT_TARGET

    def extract_proceeding_docket(self, response):
        page_no = int(response.meta['page_no'])
        __EVENT_TARGET = self.get_event_target(page_no)
        total_pages = int(response.xpath("//table[@id='Pages']//tr/td[position()=2]/a[last()]/text()").get())

        if page_no < total_pages:
            proceeding_set = self.get_proceeding_numers(response)
            formdata = {
                '__EVENTTARGET': __EVENT_TARGET,
                '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            }
            yield FormRequest(
                url='http://docs.cpuc.ca.gov/SearchRes.aspx',
                formdata=formdata,
                callback=self.extract_proceeding_docket,
                meta={'page_no': page_no+1, 'proceeding_set': proceeding_set}
            )

        else:
            proceeding_num = response.meta['proceeding_set']
            proceeding_num = {'A1904010'}
            while proceeding_num:
                num = proceeding_num.pop()
                next_page = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:6062906969229::NO:RP,57,RIR' \
                            ':P5_PROCEEDING_SELECT:{}'.format(num)
                yield response.follow(next_page,
                                      callback=self.parse_proceeding_number,
                                      meta={'dont_merge_cookie': True}
                                      )

    def parse_proceeding_number(self, response):
        proceeding_details = ProceedingDetail()

        table_rows = response.xpath("//table[@id='apex_layout_1757486743389754952']/tr")
        docket_loader = ItemLoader(item=ProceedingDetail(), response=response, selector=table_rows)

        self.get_filling_parties(table_rows, docket_loader)

        self.get_industries(table_rows, docket_loader)

        docket_loader.add_xpath('filled_on', "td[position()=2]//span[@id='P56_FILING_DATE']/text()")
        docket_loader.add_xpath('status', "td[position()=2]//span[@id='P56_STATUS']/text()")
        docket_loader.add_xpath('proceeding_type', "td[position()=2]//span[@id='P56_CATEGORY']/text()")
        docket_loader.add_xpath('title', "td[position()=2]//span[@id='P56_DESCRIPTION']/text()")
        docket_loader.add_value('source_url', response.url)

        self.get_assignees(table_rows, docket_loader)

        cookie = response.request.headers.getlist("Cookie")
        filings = list()
        docket_loader.add_value('filings', filings)
        yield response.follow('https://apps.cpuc.ca.gov/apex/f?p=401:57:0::NO',
                              callback=self.parse_filing_documents,
                              errback=self.error_back,
                              headers={'Cookie': cookie},
                              dont_filter=True,
                              meta={'item': proceeding_details, 'dont_merge_cookies': True,
                                    'docket_loader': docket_loader}
                              )

    @staticmethod
    def error_back(failure):
        logging.exception(failure)

    @staticmethod
    def get_link_status(document_link):
        pattern = re.compile("http:\/\/docs.cpuc.ca.gov\/SearchRes.aspx\?DocFormat=ALL&DocID=[0-9]{9}")
        if pattern.match(document_link):
            return True
        else:
            return False

    def parse_filing_documents(self, response):
        docket_loader = response.meta['docket_loader']
        table_rows = response.xpath("//div[@id='apexir_DATA_PANEL']//table[@class='apexir_WORKSHEET_DATA']//"
                                    "tr[@class='even'] | //tr[@class='odd']")
        for row in table_rows:
            filing_loader = ItemLoader(item=Filing(), response=response, selector=row)

            filing_loader.add_xpath('description', 'td[@headers="DESCRIPTION"]/text()')
            filing_loader.add_xpath('filled_on', 'td[@headers="FILING_DATE"]/text()')
            filing_loader.add_xpath('types', 'td[@headers="DOCUMENT_TYPE"]//u/text()')
            filing_loader.add_xpath('filing_parties', "td[@headers='FILED_BY']/text()")

            document_link = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()

            if self.get_link_status(document_link):
                request = response.follow(document_link,
                                          callback=self.parse_document_page,
                                          errback=self.error_back,
                                          meta={'dont_merge_cookies': True, 'docket_loader': docket_loader,
                                                'filing_loader': filing_loader})
                self.request_manager.filing_requests.append(request)

        if self.request_manager.filing_requests:
            yield self.request_manager.filing_requests.pop()

    @staticmethod
    def get_documents_of_filing(response):
        document_list = list()
        table_rows = response.xpath('//*[@id="ResultTable"]//tr[not(@style)]')
        for row in table_rows:
            document = Document()
            document['title'] = row.xpath("td[@class='ResultTitleTD']/text()").get()
            if document['title']:
                document['source_url'] = "http://docs.cpuc.ca.gov{}".format(
                    row.xpath("td[@class='ResultLinkTD']/a/@href").get())
                document['extension'] = row.xpath("//td[@class='ResultLinkTD']/a/text()").get()
                document_list.append(document)
        return document_list

    def get_next_request(self, docket_loader):
        if self.request_manager.filing_requests:
            return self.request_manager.filing_requests.pop()
        else:
            return docket_loader.load_item()

    def parse_document_page(self, response):
        docket_loader = response.meta['docket_loader']
        filing_loader = response.meta['filing_loader']
        document_list = self.get_documents_of_filing(response)

        filing_loader.add_value('documents', document_list)
        filings_list = docket_loader.get_output_value('filings')
        filings_list.append(filing_loader.load_item())

        yield self.get_next_request(docket_loader)

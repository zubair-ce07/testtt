import re

from scrapy.loader import ItemLoader
import scrapy
from scrapy import FormRequest

from cpuc.RequestManager import RequestManager
from cpuc.items import Document, ProceedingDetail, Filing


class CpucSpider(scrapy.Spider):
    name = "cpuc"
    allowed_domains = ['cpuc.ca.gov']
    start_urls = ['http://docs.cpuc.ca.gov/advancedsearchform.aspx']

    def parse(self, response):
        formdata = {
            'FilingDateFrom': '07/01/19',
            'FilingDateTo': '07/12/19',
            '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
            'SearchButton': 'Search',
            '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
            '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get(),
        }

        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        method='POST',
                                        callback=self.extract_proceeding_docket,
                                        meta={'proceeding_set': set(), 'page_no': 0})

    def extract_proceeding_docket(self, response):
        next_page = response.xpath("//a[@id='lnkNextPage']")
        proceeding_set = self.get_proceeding_numbers(response)
        if next_page:
            formdata = {
                '__EVENTTARGET': 'lnkNextPage',
                '__VIEWSTATEGENERATOR': response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                '__VIEWSTATE': response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                '__EVENTVALIDATION': response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            }

            yield FormRequest(
                url='http://docs.cpuc.ca.gov/SearchRes.aspx',
                formdata=formdata,
                callback=self.extract_proceeding_docket,
                meta={'proceeding_set': proceeding_set}
            )

        else:
            while proceeding_set:
                num = proceeding_set.pop()
                next_page = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:::NO:RP,57,RIR' \
                            ':P5_PROCEEDING_SELECT:{}'.format(num)

                yield scrapy.Request(
                    next_page,
                    callback=self.parse_proceeding_number,
                    meta={'cookiejar': num}
                )

    def parse_proceeding_number(self, response):
        table_rows = response.xpath("//table[@id='apex_layout_1757486743389754952']/tr")
        docket_loader = ItemLoader(item=ProceedingDetail(), response=response, selector=table_rows)

        self.get_filling_parties(table_rows, docket_loader)

        self.get_industries(table_rows, docket_loader)

        docket_loader.add_xpath('filled_on', "td[2]//span[@id='P56_FILING_DATE']/text()")
        docket_loader.add_xpath('status', "td[2]//span[@id='P56_STATUS']/text()")
        docket_loader.add_xpath('proceeding_type', "td[2]//span[@id='P56_CATEGORY']/text()")
        docket_loader.add_xpath('title', "td[2]//span[@id='P56_DESCRIPTION']/text()")
        docket_loader.add_value('source_url', response.url)

        self.get_assignees(table_rows, docket_loader)

        docket_loader.add_value('filings', list())

        return scrapy.Request('https://apps.cpuc.ca.gov/apex/f?p=401:57:0::NO',
                              callback=self.parse_filing_documents,
                              dont_filter=True,
                              meta={
                                    'cookiejar': response.meta['cookiejar'],
                                    'docket_loader': docket_loader,
                                    'request_manager': RequestManager()
                              })

    def parse_filing_documents(self, response):
        request_manager = response.meta['request_manager']
        docket_loader = response.meta['docket_loader']

        table_rows = response.xpath("//div[@id='apexir_DATA_PANEL']//table[@class='apexir_WORKSHEET_DATA']//"
                                    "tr[@class='even'] | //tr[@class='odd']")

        if table_rows:
            for row in table_rows:
                filing_loader = ItemLoader(item=Filing(), response=response, selector=row)
                filing_loader.add_xpath('description', 'td[@headers="DESCRIPTION"]/text()')
                filing_loader.add_xpath('filled_on', 'td[@headers="FILING_DATE"]/text()')
                filing_loader.add_xpath('types', 'td[@headers="DOCUMENT_TYPE"]//u/text()')
                filing_loader.add_xpath('filing_parties', "td[@headers='FILED_BY']/text()")
                document_link = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()

                if document_link != 'http://www.cpuc.ca.gov/orderadocument/':
                    if self.is_exists(document_link, request_manager.filing_requests) is not True:
                        request_parameters = {
                            'document_link': document_link,
                            'docket_loader': docket_loader,
                            'filing_loader': filing_loader
                        }
                        request_manager.filing_requests.append(request_parameters)

            next_btn = response.xpath('//*[@id="apexir_DATA_PANEL"]/table/tr[1]/td/span/a[last()]/@href').get()
            total_doc = response.xpath('//*[@id="apexir_DATA_PANEL"]/table/tr[1]/td/span/text()').get().strip()
            max_range = total_doc.split(" ")[4]
            current_range = total_doc.split(" ")[2]
            if int(current_range) < int(max_range):

                if next_btn:
                    next_btn = next_btn.split("'")[1]

                    if response.xpath("//*[@name='p_instance']/@value").get() is None:
                        p_instance = response.meta['p_instance']
                    else:
                        p_instance = response.xpath("//*[@name='p_instance']/@value").get(),
                    formdata = {
                        'p_request': 'APXWGT',
                        'p_instance': p_instance,
                        'p_flow_id': '401',
                        'p_flow_step_id': '57',
                        'p_widget_num_return': '100',
                        'p_widget_name': 'worksheet',
                        'p_widget_mod': 'ACTION',
                        'p_widget_action': 'PAGE',
                        'p_widget_action_mod': next_btn,
                        'x01': response.xpath('//input[@id="apexir_WORKSHEET_ID"]/@value').get(),
                        'x02': response.xpath('//input[@id="apexir_REPORT_ID"]/@value').get(),
                    }

                    yield scrapy.FormRequest('https://apps.cpuc.ca.gov/apex/wwv_flow.show',
                                             formdata=formdata,
                                             method="POST",
                                             callback=self.parse_filing_documents,
                                             meta={'docket_loader': docket_loader,
                                                    'cookiejar': response.meta['cookiejar'],
                                                    'request_manager': request_manager,
                                                    'p_instance': p_instance})

            else:

                if request_manager.filing_requests:
                    request_parameters = request_manager.filing_requests.pop()

                    yield response.follow(request_parameters['document_link'],
                                          meta={
                                              'dont_merge_cookies': True,
                                              'docket_loader': request_parameters['docket_loader'],
                                              'filing_loader': request_parameters['filing_loader'],
                                              'request_manager': request_manager},
                                          callback=self.parse_document_page
                                          )

        else:
            return docket_loader.load_item()

    def parse_document_page(self, response):
        docket_loader = response.meta['docket_loader']
        filing_loader = response.meta['filing_loader']
        document_list = self.get_documents_of_filing(response)

        filing_loader.add_value('documents', document_list)
        filings_list = docket_loader.get_output_value('filings')
        filings_list.append(filing_loader.load_item())

        yield self.get_next_request(docket_loader, response)

    def get_next_request(self, docket_loader, response):
        request_manager = response.meta['request_manager']
        request_parameters = None

        if request_manager.filing_requests:
            request_parameters = request_manager.filing_requests.pop()

        if request_parameters:
            request = response.follow(request_parameters['document_link'],
                                      meta={
                                            'dont_merge_cookies': True,
                                            'docket_loader': request_parameters['docket_loader'],
                                            'filing_loader': request_parameters['filing_loader'],
                                            'request_manager': request_manager},
                                      callback=self.parse_document_page
                                      )

            return request
        else:

            return docket_loader.load_item()

    @staticmethod
    def get_filling_parties(table_rows, docket_loader):
        filling_parties = table_rows.xpath("//span[@id='P56_FILED_BY']/text()").get()
        docket_loader.add_value('filing_parties', filling_parties)

    @staticmethod
    def get_industries(table_rows, docket_loader):
        industries = table_rows.xpath("//span[@id='P56_INDUSTRY']/text()").get()
        docket_loader.add_value('industries', industries)

    @staticmethod
    def get_assignees(table_rows, docket_loader):
        assignees = table_rows.xpath("//span[@id='P56_STAFF']/text()").get()
        docket_loader.add_value('assignees', assignees)

    @staticmethod
    def get_proceeding_numbers(response):
        proceeding_set = response.meta['proceeding_set']
        table_rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
        if table_rows:

            for row in table_rows:
                proceeding_numbers = row.xpath("td[@class='ResultTitleTD']/text()")[1].get()
                proceeding_numbers = re.findall(r'[A-Z][0-9]{7}', proceeding_numbers)

                for proceeding_number in proceeding_numbers:
                    proceeding_set.add(proceeding_number)

            return proceeding_set
        else:

            return proceeding_set

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

    @staticmethod
    def is_exists(document_link, requests):
        for request in requests:

            if document_link == request['document_link']:
                return True

        return False

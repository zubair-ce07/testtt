"""
CPUC Module.

CPUC Module to extract data from
cpuc website according to the date
ranges given.
"""

from datetime import datetime
from urllib.parse import urljoin
import scrapy

from CPUC.items import ProceedingLoader, \
                       ProceedingDocumentLoader, \
                       DocumentLoader


class CpucSpider(scrapy.Spider):
    """
    CPUC Class Spider.

    CPUC website spider to crawl
    through the website and scrape
    data.
    """

    name = 'cpuc'
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP']
    PAGNITION_URL = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
    URL_JOIN_PART = 'https://apps.cpuc.ca.gov/apex/'
    P_WIDGET_NUM_RETURN = '100'
    P_WIDGET_NAME = 'worksheet'
    P_WIDGET_MOD = 'ACTION'
    P_WIDGET_ACTION = 'PAGE'
    p_instance = ''
    p_flow_id = ''
    p_flow_step_id = ''
    p_widget_action_mod = ''
    cookie_count = 0

    def __init__(self, low_date_range=None, high_date_range=None, **kwargs):
        """
        CPUC class iniatilise method.

        Mehthod to iniatilize input arguments
        for high and low data ranges.
        """
        super(CpucSpider, self).__init__(**kwargs)
        if low_date_range is None or high_date_range is None:
            self.low_date_range = ''
            self.high_date_range = ''
        else:
            self.low_date_range = low_date_range
            self.high_date_range = high_date_range

    @staticmethod
    def validate_date(date):
        """Date validation for data ranges."""
        try:
            datetime.strptime(date, '%m/%d/%Y')
            return True
        except ValueError:
            print("Date format is not correct.")
            exit()

    def parse(self, response):
        """
        CPUC main page parse method.

        Mehthod to check input dates to
        be valid and yield a scrapy request.
        """
        if self.low_date_range and self.high_date_range:
            if self.validate_date(self.low_date_range) and \
                    self.validate_date(self.high_date_range):
                form_data = {'p_t05': self.low_date_range,
                             'p_t06': self.high_date_range}
        else:
            form_data = {'p_t05': '09/01/2019',
                         'p_t06': '10/09/2019'
                        }

        yield scrapy.FormRequest.from_response(response,
                                               formdata=form_data,
                                               callback=self.parse_proceedings
                                              )

    def parse_proceedings(self, response):
        """
        Proceedings pagition method.

        Method to capture proceeding urls from
        main page and following pagnition pages.
        """
        proceeding_urls = response.css("table.apexir_WORKSHEET_DATA tr a::attr(href)").getall()
        for url in proceeding_urls:
            self.cookie_count += 1
            proceeding_url = self.URL_JOIN_PART + url
            yield scrapy.Request(url=proceeding_url,
                                 callback=self.parse_proceeding_data,
                                 meta={'cookiejar': self.cookie_count})

        self.p_widget_action_mod = response.css('.fielddata > a:nth-child(2)::attr(href)').get()
        if self.p_widget_action_mod is not None:
            self.p_widget_action_mod = self.p_widget_action_mod.split("'")[1]
        if not self.p_widget_action_mod:
            self.p_widget_action_mod = response.css('.fielddata > a::attr(href)').get()
        if self.p_widget_action_mod is not None:
            self.p_widget_action_mod = self.p_widget_action_mod.split("'")[1]
        if not self.p_instance:
            self.p_instance = response.css('#pInstance::attr(value)').get()
        if not self.p_flow_id:
            self.p_flow_id = response.css('#pFlowId::attr(value)').get()
        if not self.p_flow_step_id:
            self.p_flow_step_id = response.css('#pFlowStepId::attr(value)').get()

        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            form_data = {'p_request': 'APXWGT',
                         'p_instance': self.p_instance,
                         'p_flow_id': self.p_flow_id,
                         'p_flow_step_id': self.p_flow_step_id,
                         'p_widget_num_return': self.P_WIDGET_NUM_RETURN,
                         'p_widget_name': self.P_WIDGET_NAME,
                         'p_widget_mod': self.P_WIDGET_MOD,
                         'p_widget_action': self.P_WIDGET_ACTION,
                         'p_widget_action_mod': self.p_widget_action_mod,
                         'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                         'x02': response.css('#apexir_REPORT_ID::attr(value)').get(),
                         }
            yield scrapy.FormRequest(
                self.PAGNITION_URL,
                formdata=form_data,
                callback=self.parse_proceedings,
                meta={'cookiejar': response.meta['cookiejar']}
                )

    def parse_proceeding_data(self, response):
        """
        Proceeding details method.

        Method to yield details about proceedings
        and capture document urls and yield a scrapy
        request.
        """
        proceeding_number = response.css('div.rc-content-main >h1::text').get()
        if proceeding_number:
            proceeding_number = proceeding_number.split(' ')[0]
        proceeding = ProceedingLoader(selector=response)
        proceeding.add_css("proceeding_number", '.rc-content-main > h1::text')
        proceeding.add_css("filed_by", '#P56_FILED_BY::text')
        proceeding.add_css(
            "filed_by", '#P56_SERVICE_LISTS > span > a::attr(href)')
        proceeding.add_css(
            "service_lists", '#P56_SERVICE_LISTS > span > a::attr(href)')
        proceeding.add_css("industry", '#P56_INDUSTRY::text')
        proceeding.add_css("filing_date", '#P56_FILING_DATE::text')
        proceeding.add_css("category", '#P56_CATEGORY::text')
        proceeding.add_css("current_status", '#P56_STATUS::text')
        proceeding.add_css("description", '#P56_DESCRIPTION::text')
        proceeding.add_css("staff", '#P56_STAFF::text')
        proceeding.add_value("total_documents", 0)

        documents_url = str(response.url).replace(':56:', ':57:')
        scrapy_request = scrapy.Request(url=documents_url,
                                        callback=self.parse_proceeding_documents,
                                        meta={'cookiejar': response.meta['cookiejar']})

        if scrapy_request:
            scrapy_request.meta['proceeding'] = proceeding
            yield scrapy_request
        else:
            yield proceeding

    def parse_proceeding_documents(self, response):
        """
        Proceeding documents method.

        Method to extract list of documents
        available for a proceeding and its data.
        """
        proceeding = response.meta['proceeding']
        documents_table = response.css('#apexir_WORKSHEET_ID::attr(value)').get()
        document_urls = []
        documents = response.css("#{} > tr + tr".format(documents_table)).getall()
        for document in documents:
            document = scrapy.Selector(text=document)
            document_url = document.css("tr > td[headers*='DOCUMENT_TYPE'] > a::attr(href)").get()
            if document_url:
                proceeding_document = self.parse_documents_data(document)
                proceeding.replace_value('total_documents',
                                         proceeding.get_collected_values("total_documents")[0]+1)
                document_urls.append(document_url)
                scrapy_request = scrapy.Request(document_url,
                                                callback=self.parse_document,
                                                meta={'cookiejar': response.meta['cookiejar']})
                scrapy_request.meta['proceeding'] = proceeding
                scrapy_request.meta['proceeding_document'] = proceeding_document
                yield scrapy_request

        self.p_widget_action_mod = response.css('.fielddata > a:nth-child(2)::attr(href)').get()

        if self.p_widget_action_mod is not None:
            self.p_widget_action_mod = self.p_widget_action_mod.split("'")[1]
        if not self.p_widget_action_mod:
            self.p_widget_action_mod = response.css('.fielddata > a::attr(href)').get()
        if self.p_widget_action_mod is not None:
            self.p_widget_action_mod = self.p_widget_action_mod.split("'")[1]
        if not self.p_instance:
            self.p_instance = response.css('#pInstance::attr(value)').get()
        if not self.p_flow_id:
            self.p_flow_id = response.css('#pFlowId::attr(value)').get()
        if not self.p_flow_step_id:
            self.p_flow_step_id = response.css('#pFlowStepId::attr(value)').get()

            if response.css('.fielddata > a') and response.css(
                    ".fielddata > a > img[title*='Next']"):
                form_data = {'p_request': 'APXWGT',
                             'p_instance': self.p_instance,
                             'p_flow_id': self.p_flow_id,
                             'p_flow_step_id': self.p_flow_step_id,
                             'p_widget_num_return': self.P_WIDGET_NUM_RETURN,
                             'p_widget_name': self.P_WIDGET_NAME,
                             'p_widget_mod': self.P_WIDGET_MOD,
                             'p_widget_action': self.P_WIDGET_ACTION,
                             'p_widget_action_mod': self.p_widget_action_mod,
                             'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                             'x02': response.css('#apexir_REPORT_ID::attr(value)').get(),
                            }
                scrapy_request = scrapy.FormRequest(
                    self.PAGNITION_URL,
                    callback=self.parse_proceeding_documents,
                    formdata=form_data,
                    headers={'Referer': response.url},
                    meta={'cookiejar': response.meta['cookiejar']})
                scrapy_request.meta['proceeding'] = proceeding
                yield scrapy_request

            if not document_urls:
                yield proceeding.load_item()

    @staticmethod
    def parse_documents_data(document_row):
        """
        Document's data method.

        Method to extract document's data
        and return a proceeding_document item.
        """
        proceeding_document = ProceedingDocumentLoader(
            selector=document_row)
        proceeding_document.add_css(
            'document_filing_date', "tr > td[headers*='FILING_DATE']::text")
        proceeding_document.add_css(
            'document_type', "tr > td[headers*='DOCUMENT_TYPE'] > a > span > u::text")
        proceeding_document.add_css(
            'filed_by', "tr > td[headers*='FILED_BY']::text")
        proceeding_document.add_css(
            'description', "tr > td[headers*='DESCRIPTION']::text")
        return proceeding_document

    @staticmethod
    def parse_document(response):
        """
        Each Document data method.

        Method to extract crawl each document's url
        extract its data. Also call all items
        and yield proceeding Item.
        """
        proceeding = response.meta['proceeding']
        proceeding_document = response.meta['proceeding_document']
        proceeding_document.add_value('document_url', response.url)

        files = response.selector.xpath(
            '//table[@id="ResultTable"]/tbody/tr')
        for file in files:
            if file.css('.ResultTitleTD').get():
                document = DocumentLoader(selector=file)
                document.add_css('title', '.ResultTitleTD')
                document.add_css('doc_type', '.ResultTypeTD::text')
                pdf_link = urljoin('http://docs.cpuc.ca.gov',
                                   file.css('.ResultLinkTD > a::attr(href)').get())
                document.add_value('pdf_link', pdf_link)
                document.add_css('published_date', '.ResultDateTD::text')
                proceeding_document.add_value('files', document.load_item())
        proceeding.add_value('documents', proceeding_document.load_item())

        if len(proceeding.get_collected_values("documents")) == \
                proceeding.get_collected_values("total_documents")[0]:
            yield proceeding.load_item()

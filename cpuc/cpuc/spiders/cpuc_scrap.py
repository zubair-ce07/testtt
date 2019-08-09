"""CPUC scraping module.

This module is for scraping cpuc website.
"""

# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor

from cpuc.items import ProceedingDocumentLoader, DocumentLoader, \
    ProceedingLoader


class CpucScrapSpider(scrapy.Spider):
    """Cpuc scraping class.

    this class has different method from submitting search form from a start
    date to an end date and then scraping proceeding and then documents and
    their items details.
    """

    name = 'cpuc_scrap'
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP/']
    cookie_count = 0
    DOCUMENT_LINK_VALIDATION = r"http://docs.cpuc.ca.gov/SearchRes.aspx\?"\
        "DocFormat=ALL&DocID="
    PAGINATION_URL = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
    P_WIDGET_NUM_RETURN = '100'
    P_WIDGET_Name = 'worksheet'
    P_WIDGET_MOD = 'ACTION'
    P_WIDGET_ACTION = 'PAGE'

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        """Spider parameters initialization.

        This method will check if the parameters were present.
        """
        super(CpucScrapSpider, self).__init__(*args, **kwargs)
        if start_date is None or end_date is None:
            self.start_date = ''
            self.end_date = ''
        else:
            self.start_date = start_date
            self.end_date = end_date

    def parse(self, response):
        """Search proceeding.

        This method submit search form from a start date to an end date.
        """
        if self.start_date and self.end_date:
            if self.date_validation(self.start_date) and \
                    self.date_validation(self.end_date):
                form_data = {'p_t04': self.start_date,
                             'p_t05': self.end_date, 'p_request': 'Go'}
            else:
                print("Date format is false, Date Format is m/d/y")
                return
        else:
            form_data = {'p_t04': '01/01/2019',
                         'p_t05': '08/02/2019', 'p_request': 'Go'}

        yield scrapy.FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.proceedings_parse
        )

    def proceedings_parse(self, response):
        """Scrap proceeding documents.

        This method scrap all the proceeding document and handle it's pagination.
        """
        proceeding_links = LinkExtractor(
            allow=r"::NO:RP,57,RIR:P5_PROCEEDING_SELECT:"
        ).extract_links(response)
        for link in proceeding_links:
            self.cookie_count += 1
            yield scrapy.Request(link.url, callback=self.scrap_proceeding,
                                 meta={'cookiejar': self.cookie_count})
        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            form_data = {'p_request': 'APXWGT',
                         'p_instance': response.css('#pInstance::attr(value)').get(),
                         'p_flow_id': response.css('#pFlowId::attr(value)').get(),
                         'p_flow_step_id': response.css('#pFlowStepId::attr(value)').get(),
                         'p_widget_num_return': self.P_WIDGET_NUM_RETURN,
                         'p_widget_name': self.P_WIDGET_Name,
                         'p_widget_mod': self.P_WIDGET_MOD,
                         'p_widget_action': self.P_WIDGET_ACTION,
                         'p_widget_action_mod': response.css(
                             '.fielddata > a::attr(href)').get().split("'")[1],
                         'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                         'x02': response.css('#apexir_REPORT_ID::attr(value)').get()
                         }
            req = scrapy.FormRequest(
                self.PAGINATION_URL, callback=self.proceedings_parse, formdata=form_data)
            yield req

    def scrap_proceeding(self, response):
        """Scrap a proceeding.

        This method scrap a proceeding details and request it's documnts.
        """
        proceeding = ProceedingLoader(selector=response)
        proceeding.add_css("proceeding_no", '.rc-content-main > h1::text')
        proceeding.add_css("filed_by", '#P56_FILED_BY::text')
        proceeding.add_css(
            "filed_by", '#P56_SERVICE_LISTS > span > a::attr(href)')
        proceeding.add_css(
            "service_list", '#P56_SERVICE_LISTS > span > a::attr(href)')
        proceeding.add_css("industry", '#P56_INDUSTRY::text')
        proceeding.add_css("filling_date", '#P56_FILING_DATE::text')
        proceeding.add_css("category", '#P56_CATEGORY::text')
        proceeding.add_css("current_status", '#P56_STATUS::text')
        proceeding.add_css("description", '#P56_DESCRIPTION::text')
        proceeding.add_css("staff", '#P56_STAFF::text')
        proceeding.add_value(
            "total_documents", 0)

        link = response.url.replace('56', '57')
        request = scrapy.Request(
            link, callback=self.scrap_documents,
            meta={'cookiejar': response.meta['cookiejar']})
        if request:
            request.meta['proceeding'] = proceeding
            yield request
        else:
            yield proceeding

    def scrap_documents(self, response):
        """Scrap a document.

        This method scrap documnts and handle it's pagination.
        """
        proceeding = response.meta['proceeding']
        apexir_workshet_id = response.css(
            '#apexir_WORKSHEET_ID::attr(value)').get()
        documents_links = []
        document_rows = response.css(
            "#{} > tr + tr".format(apexir_workshet_id)).getall()
        for document_row in document_rows:
            document_row = scrapy.Selector(text=document_row)
            document_link = document_row.css(
                "tr > td[headers*='DOCUMENT_TYPE'] > a::attr(href)").get()
            if document_link and re.search(
                    self.DOCUMENT_LINK_VALIDATION,
                    document_link):
                proceeding_document = self.make_proceeding_document(
                    document_row)
                proceeding.replace_value(
                    'total_documents', proceeding.get_collected_values(
                        "total_documents")[0]+1)
                documents_links.append(document_link)
                request = scrapy.Request(
                    document_link,
                    callback=self.scrap_item,
                    dont_filter=True,
                    meta={'cookiejar': response.meta['cookiejar']})
                request.meta['proceeding'] = proceeding
                request.meta['proceeding_document'] = proceeding_document
                yield request
        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            form_data = {'p_request': 'APXWGT',
                         'p_instance': response.css('#pInstance::attr(value)').get(),
                         'p_flow_id': response.css('#pFlowId::attr(value)').get(),
                         'p_flow_step_id': response.css('#pFlowStepId::attr(value)').get(),
                         'p_widget_num_return': self.P_WIDGET_NUM_RETURN,
                         'p_widget_name': self.P_WIDGET_Name,
                         'p_widget_mod': self.P_WIDGET_MOD,
                         'p_widget_action': self.P_WIDGET_ACTION,
                         'p_widget_action_mod': response.css(
                             '.fielddata > a::attr(href)').get().split("'")[1],
                         'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                         'x02': response.css('#apexir_REPORT_ID::attr(value)').get()
                         }
            req = scrapy.FormRequest(
                self.PAGINATION_URL,
                callback=self.scrap_documents,
                formdata=form_data,
                headers={'Referer': response.url},
                meta={'cookiejar': response.meta['cookiejar']})
            req.meta['proceeding'] = proceeding
            yield req

        if not documents_links:
            yield proceeding.load_item()

    @staticmethod
    def scrap_item(response):
        """Scrap a document items.

        This method scrap all the items of a document.
        """
        proceeding = response.meta['proceeding']
        proceeding_document = response.meta['proceeding_document']
        proceeding_document.add_value('link', response.url)
        files = response.selector.xpath(
            '//table[@id="ResultTable"]/tbody/tr')  # css was not working
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

    @staticmethod
    def make_proceeding_document(document_row):
        """Make proceeding_document loader object.

        make and return proceeding_document object and then return it
        """
        proceeding_document = ProceedingDocumentLoader(
            selector=document_row)
        proceeding_document.add_css(
            'filling_date', "tr > td[headers*='FILING_DATE']::text")
        proceeding_document.add_css(
            'document_type', "tr > td[headers*='DOCUMENT_TYPE'] > a > span > u::text")
        proceeding_document.add_css(
            'filed_by', "tr > td[headers*='FILED_BY']::text")
        proceeding_document.add_css(
            'description', "tr > td[headers*='DESCRIPTION']::text")
        return proceeding_document

    @staticmethod
    def date_validation(date):
        """Validate date.

        This method validate date if date formaat is correct then it return true
        """
        try:
            datetime.strptime(date, '%m/%d/%Y')
            return True
        except ValueError:
            return False

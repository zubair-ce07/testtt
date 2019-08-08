"""CPUC scraping module.

This module is for scraping cpuc website.
"""

# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
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

    def parse(self, response):
        """Search proceeding.

        This method submit search form from a start date to an end date.
        """
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'p_t04': '01/01/2019',
                      'p_t05': '08/02/2019', 'p_request': 'Go'},
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
            frmdata = {'p_request': 'APXWGT',
                       'p_instance': response.css('#pInstance::attr(value)').get(),
                       'p_flow_id': '401',
                       'p_flow_step_id': '5',
                       'p_widget_num_return': '100',
                       'p_widget_name': 'worksheet',
                       'p_widget_mod': 'ACTION',
                       'p_widget_action': 'PAGE',
                       'p_widget_action_mod': response.css(
                           '.fielddata > a::attr(href)').get().split("'")[1],
                       'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                       'x02': response.css('#apexir_REPORT_ID::attr(value)').get()
                       }
            req = scrapy.FormRequest(
                self.PAGINATION_URL, callback=self.proceedings_parse, formdata=frmdata)
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

        documents_links = []
        document_rows = response.css(
            "#{} > tr + tr".format(response.css(
                '#apexir_WORKSHEET_ID::attr(value)').get())).getall()
        for document_row in document_rows:
            document_row = scrapy.Selector(text=document_row)
            document_link = document_row.css(
                "tr > td[headers*='DOCUMENT_TYPE'] > a::attr(href)").get()
            if document_link and re.search(
                    self.DOCUMENT_LINK_VALIDATION,
                    document_link):
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
            frmdata = {'p_request': 'APXWGT',
                       'p_instance': response.css('#pInstance::attr(value)').get(),
                       'p_flow_id': '401',
                       'p_flow_step_id': '57',
                       'p_widget_num_return': '100',
                       'p_widget_name': 'worksheet',
                       'p_widget_mod': 'ACTION',
                       'p_widget_action': 'PAGE',
                       'p_widget_action_mod': response.css(
                           '.fielddata > a::attr(href)').get().split("'")[1],
                       'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                       'x02': response.css('#apexir_REPORT_ID::attr(value)').get()
                       }
            req = scrapy.FormRequest(
                self.PAGINATION_URL,
                callback=self.scrap_documents,
                formdata=frmdata,
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
                # title = re.sub(re.compile(r'<[^>]+>'), '',
                #              file.css('.ResultTitleTD').get()),
                document.add_css('title', '.ResultTitleTD')
                document.add_css('doc_type', '.ResultTypeTD::text')
                pdf_link = urljoin('http://docs.cpuc.ca.gov',
                                   file.css('.ResultLinkTD > a::attr(href)').get())
                document.add_value('pdf_link', pdf_link)
                document.add_css('published_date', '.ResultDateTD::text')
                proceeding_document.add_value('files', document.load_item())
        proceeding.add_value('documents', proceeding_document.load_item())

        if len(proceeding.get_collected_values("documents")) == proceeding.get_collected_values("total_documents")[0]:
            yield proceeding.load_item()

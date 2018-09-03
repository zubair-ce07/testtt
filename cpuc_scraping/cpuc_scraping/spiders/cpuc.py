# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import CaseProceeding, ProceedingDocument, ProceedingFile


class CpucSpider(CrawlSpider):
    name = 'cpuc'
    allowed_domains = ['cpuc.ca.gov']
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP::']

    pagination_url = 'https://apps.cpuc.ca.gov/apex/wwv_flow.show'
    cookiejar_counter = 0

    case_detail_extractor_1 = LinkExtractor(restrict_css="tr.even")
    case_detail_extractor_2 = LinkExtractor(restrict_css="tr.odd")

    rules = (
        Rule(case_detail_extractor_1, callback='case_detail_page', follow=True),
        Rule(case_detail_extractor_2, callback='case_detail_page', follow=True),
    )

    custom_settings = {
        'DUPEFILTER_DEBUG': True,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.117 Safari/537.36',
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    }

    def parse(self, response):
        form_data = {
            'p_t04': '03/30/2018',
            # 'p_t04': '01/01/2018',
            # 'p_t05': '08/29/2018',
            'p_t05': '03/30/2018',
        }

        yield scrapy.FormRequest.from_response(response, formid="wwvFlowForm", formdata=form_data,
                                               callback=self.search_page)

    def search_page(self, response):

        requests = super().parse(response)

        for counter, request in enumerate(requests):
            request.meta['cookiejar'] = self.cookiejar_counter
            self.cookiejar_counter += 1
            yield request

        pagination = self.extract_p_widget_action_mod(response)
        if pagination:
            form_data = {
                'p_request': 'APXWGT',
                'pInstance': self.extract_pagination_p_instance(response),
                'p_flow_id': '401',
                'p_flow_step_id': '5',
                'p_widget_num_return': '100',
                'p_widget_name': 'worksheet',
                'p_widget_action_mod': pagination,
                'x01': self.extract_pagiantion_x_01(response),
                'x02': self.extract_pagiantion_x_02(response),

                'p_widget_mod': 'ACTION',
                'p_widget_action': 'PAGE'

            }
            yield scrapy.FormRequest(self.pagination_url, formdata=form_data, callback=self.search_page)

    def case_detail_page(self, response):
        proceeding = CaseProceeding()

        proceeding['number'] = self.extract_proceeding_number(response)
        proceeding['filed_by'] = self.extract_proceeding_filed_by(response)
        proceeding['industry'] = self.extract_proceeding_industry(response)
        proceeding['filing_date'] = self.extract_proceeding_filing_date(response)
        proceeding['category'] = self.extract_proceeding_category(response)
        proceeding['status'] = self.extract_proceeding_status(response)
        proceeding['description'] = self.extract_proceeding_description(response)
        proceeding['staff_members'] = self.extract_proceeding_staff(response)
        proceeding['documents'] = []

        form_data = {
            'p_request': 'T_DOCUMENTS',
            'p_md5_checksum': ''
        }

        yield scrapy.FormRequest.from_response(response, formid="wwvFlowForm",
                                               formdata=form_data,
                                               meta={
                                                   'proceeding': proceeding,
                                                   'dont_filter': True,
                                                   'cookiejar': response.meta['cookiejar']
                                               },
                                               callback=self.document_list_page)

    def document_list_page(self, response):
        proceeding = response.meta['proceeding']
        table_rows = response.css("tr.even")
        table_rows = table_rows + response.css("tr.odd")
        index = 0
        files_urls = []
        for row in table_rows:
            proceeding_document = ProceedingDocument()
            proceeding_document['filing_date'] = self.extract_proceeding_doc_filing_date(row)
            proceeding_document['type'] = self.extract_proceeding_doc_type(row)
            proceeding_document['filed_by'] = self.extract_proceeding_doc_filed_by(row)
            proceeding_document['description'] = self.extract_proceeding_doc_description(row)
            proceeding_document['document_files'] = []
            proceeding['documents'].append(proceeding_document)
            document_url = self.extract_proceeding_doc_file_urls(row)

            if document_url.find('orderadocument') == -1:
                files_urls.append(DocumentFilesUrls(document_url, index))
            index += 1

        if files_urls:
            file_url = files_urls.pop(0)
            request = scrapy.Request(url=file_url.url,
                                     callback=self.document_files_page)
            request.meta['proceeding'] = proceeding
            request.meta['index'] = file_url.index
            request.meta['files_urls'] = files_urls
            yield request
        else:
            yield proceeding

    def document_files_page(self, response):
        files_urls = response.meta['files_urls']
        proceeding = response.meta['proceeding']
        index = response.meta['index']

        # response.css was not working on it :(
        # table_rows = response.css('table#ResultTable tr')
        table_rows = self.extract_proceeding_file_table(response)
        for row in table_rows:
            title = self.extract_proceeding_file_title(row)
            if not title:
                continue

            proceeding_file = ProceedingFile()
            proceeding_file['title'] = title[0]
            proceeding_file['type'] = self.extract_proceeding_file_type(row)
            proceeding_file['file_url'] = response.urljoin(self.extract_proceeding_file_link(row))
            proceeding_file['date_published'] = self.extract_proceeding_file_date_published(row)
            proceeding_file['related_proceedings'] = re.split(r'; |: ', title[1])
            # i have popped 1st element because it contains word "Proceeding"
            # which we do not needed
            proceeding_file['related_proceedings'].pop(0)
            proceeding['documents'][index]['document_files'].append(proceeding_file)

        if not files_urls:
            yield proceeding
        else:
            file_url = files_urls.pop(0)
            request = scrapy.Request(url=file_url.url,
                                     callback=self.document_files_page)
            request.meta['proceeding'] = proceeding
            request.meta['index'] = file_url.index
            request.meta['files_urls'] = files_urls
            yield request


    def extract_proceeding_number(self, response):
        return response.css('h1::text').extract_first(default="").split(" ")[0]

    def extract_proceeding_filed_by(self, response):
        return response.css("span#P56_FILED_BY::text").extract()

    def extract_proceeding_industry(self, response):
        return response.css("span#P56_INDUSTRY::text").extract()

    def extract_proceeding_filing_date(self, response):
        return response.css("span#P56_FILING_DATE::text").extract_first(default="")

    def extract_proceeding_category(self, response):
        return response.css("span#P56_CATEGORY::text").extract()

    def extract_proceeding_status(self, response):
        return response.css("span#P56_STATUS::text").extract_first(default="")

    def extract_proceeding_description(self, response):
        return response.css("span#P56_DESCRIPTION::text").extract_first(default="")

    def extract_proceeding_staff(self, response):
        return response.css("span#P56_STAFF::text").extract()

    def extract_pagination_p_instance(self, response):
        return response.css('input#pInstance::attr(value)').extract_first(default='')

    def extract_p_widget_action_mod(self, response):
        pagination_link = response.css('span.fielddata a::attr(href)').extract()
        if pagination_link:
            return pagination_link[-1].split("'")[1]
        return []

    def extract_pagiantion_x_01(self, response):
        return response.css('input#apexir_WORKSHEET_ID::attr(value)').extract_first(default='')

    def extract_pagiantion_x_02(self, response):
        return response.css('input#apexir_REPORT_ID::attr(value)').extract_first(default=''),

    def extract_proceeding_doc_filing_date(self, row):
        return row.css("td[headers='FILING_DATE']::text").extract_first(default="")

    def extract_proceeding_doc_type(self, row):
        return row.css("td[headers='DOCUMENT_TYPE'] u::text").extract_first(default="")

    def extract_proceeding_doc_filed_by(self, row):
        return row.css("td[headers='FILED_BY']::text").extract_first()

    def extract_proceeding_doc_description(self, row):
        return row.css("td[headers='DESCRIPTION']::text").extract_first(default="")


    def extract_proceeding_doc_file_urls(self, row):
        return row.css("a::attr(href)").extract_first(default="")

    def extract_proceeding_file_table(self, response):
        return response.xpath('//table[@id="ResultTable"]//tr')

    def extract_proceeding_file_title(self, row):
        return row.css('td.ResultTitleTD::text').extract()

    def extract_proceeding_file_type(self, row):
        return row.css('td.ResultTypeTD::text').extract_first()

    def extract_proceeding_file_link(self, row):
        return row.css('td.ResultLinkTD a::attr(href)').extract_first()

    def extract_proceeding_file_date_published(self, row):
        return row.css('td.ResultDateTD::text').extract_first()




class DocumentFilesUrls:
    def __init__(self, url="", index=0):
        self.url = url
        self.index = index


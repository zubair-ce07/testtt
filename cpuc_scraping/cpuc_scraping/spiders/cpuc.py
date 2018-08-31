# -*- coding: utf-8 -*-
import re
from functools import partial
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CaseProceeding, ProceedingDocument, ProceedingFile


class CpucSpider(CrawlSpider):
    name = 'cpuc'
    allowed_domains = ['cpuc.ca.gov']
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP::']

    search_page_url = 'https://apps.cpuc.ca.gov/apex/wwv_flow.accept'

    case_detail_extractor_1 = LinkExtractor(restrict_css="tr.even")
    case_detail_extractor_2 = LinkExtractor(restrict_css="tr.odd")

    rules = (
        Rule(case_detail_extractor_1, callback='case_detail_page', follow=True),
        Rule(case_detail_extractor_2, callback='case_detail_page', follow=True),
    )

    cpuc_cookies = ""

    def parse(self, response):
        self.cpuc_cookies = response.headers.getlist('Set-Cookie')[0].decode("utf-8").split(';')[0]
        form_data = {
            'p_t04': '03/30/2018',
            # 'p_t04': '01/01/2018',
            # 'p_t05': '08/29/2018',
            'p_t05': '03/30/2018',
        }

        yield scrapy.FormRequest.from_response(response, formid="wwvFlowForm", formdata=form_data,
                                               callback=self.search_page)

    def search_page(self, response):
        yield from super().parse(response)

    def case_detail_page(self, response):
        proceeding = CaseProceeding()

        proceeding['number'] = response.css('h1::text').extract_first(default="").split(" ")[0]
        proceeding['filed_by'] = response.css("span#P56_FILED_BY::text").extract()
        proceeding['industry'] = response.css("span#P56_INDUSTRY::text").extract()
        proceeding['filing_date'] = response.css("span#P56_FILING_DATE::text").extract_first(
            default="")
        proceeding['category'] = response.css("span#P56_CATEGORY::text").extract()
        proceeding['status'] = response.css("span#P56_STATUS::text").extract_first(default="")
        proceeding['description'] = response.css("span#P56_DESCRIPTION::text").extract_first(
            default="")
        proceeding['staff_members'] = response.css("span#P56_STAFF::text").extract()
        proceeding['documents'] = []

        form_data = {
            'p_request': 'T_DOCUMENTS',
        }

        request = scrapy.FormRequest.from_response(response, formid="wwvFlowForm",
                                                   formdata=form_data,
                                                   callback=self.document_list_page)
        request.meta['proceeding'] = proceeding
        yield request

    def document_list_page(self, response):
        proceeding = response.meta['proceeding']
        print("i ----------------------------------------------")
        table_rows = response.css("tr.even")
        table_rows = table_rows + response.css("tr.odd")

        index = 0
        last_doc_flag = False
        table_size = len(table_rows)

        for row in table_rows:
            proceeding_document = ProceedingDocument()
            proceeding_document['filing_date'] = row.css(
                "td[headers='FILING_DATE']::text").extract_first(default="")
            proceeding_document['type'] = row.css(
                "td[headers='DOCUMENT_TYPE'] u::text").extract_first(default="")
            proceeding_document['filed_by'] = row.css(
                "td[headers='FILED_BY']::text").extract_first()
            proceeding_document['description'] = row.css(
                "td[headers='DESCRIPTION']::text").extract_first(default="")

            proceeding_document['document_files'] = []

            document_url = row.css("a::attr(href)").extract_first(default="")

            proceeding['documents'].append(proceeding_document)

            if (index + 1) == table_size:
                last_doc_flag = True
            if document_url.find('orderadocument') == -1:
                request = scrapy.Request(url=document_url,
                                         callback=self.document_files_page,
                                         headers={"Cookie": self.cpuc_cookies}, priority=1)
                request.meta['proceeding'] = proceeding
                request.meta['index'] = index
                request.meta['last_doc_flag'] = last_doc_flag
                # yield request

            index += 1

        yield proceeding

        # documents_urls = response.css("tr.even a::attr(href)").extract()
        # documents_urls = documents_urls + response.css("tr.odd a::attr(href)").extract()

    def document_files_page(self, response):
        proceeding = response.meta['proceeding']
        index = response.meta['index']
        last_doc_flag = response.meta['last_doc_flag']

        # response.css was not working on it :(
        # table_rows = response.css('table#ResultTable tr')
        table_rows = response.xpath('//table[@id="ResultTable"]//tr')
        for row in table_rows:
            title = row.css('td.ResultTitleTD::text').extract()
            if not title:
                continue

            proceeding_file = ProceedingFile()
            proceeding_file['title'] = title[0]
            proceeding_file['type'] = row.css('td.ResultTypeTD::text').extract_first()
            proceeding_file['file_url'] = response.urljoin(
                row.css('td.ResultLinkTD a::attr(href)').extract_first())
            proceeding_file['date_published'] = row.css('td.ResultDateTD::text').extract_first()
            proceeding_file['related_proceedings'] = re.split(r'; |: ', title[1])
            # i have popped 1st element because it contains word "Proceeding" which we do not needed
            proceeding_file['related_proceedings'].pop(0)

            proceeding['documents'][index]['document_files'].append(proceeding_file)
        if last_doc_flag:
            return proceeding

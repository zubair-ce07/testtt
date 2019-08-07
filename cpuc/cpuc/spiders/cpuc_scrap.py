# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor

from cpuc.items import Proceeding, ProceedingDocument, Document


class CpucScrapSpider(scrapy.Spider):
    name = 'cpuc_scrap'
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP/']
    cookie_count = 0

    def parse(self, response):
        # self.cookie = response.headers.getlist(
        #     'Set-Cookie')[0].decode("utf-8").split(';')[0]
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'p_t04': '01/01/2019',
                      'p_t05': '08/02/2019', 'p_request': 'Go'},
            callback=self.proceeding_parse
        )

    def proceeding_parse(self, response):
        proceeding_links = LinkExtractor(
            allow=r"::NO:RP,57,RIR:P5_PROCEEDING_SELECT:"
        ).extract_links(response)
        p_instance = response.css('#pInstance::attr(value)').get()
        x01 = response.css('#apexir_WORKSHEET_ID::attr(value)').get()
        x02 = response.css('#apexir_REPORT_ID::attr(value)').get()
        for link in proceeding_links:
            self.cookie_count += 1
            yield scrapy.Request(link.url, callback=self.scrap_proceeding, meta={'cookiejar': self.cookie_count})
        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            frmdata = {'p_request': 'APXWGT',
                       'p_instance': p_instance,
                       'p_flow_id': '401',
                       'p_flow_step_id': '5',
                       'p_widget_num_return': '100',
                       'p_widget_name': 'worksheet',
                       'p_widget_mod': 'ACTION',
                       'p_widget_action': 'PAGE',
                       'p_widget_action_mod': response.css(
                           '.fielddata > a::attr(href)').get().split("'")[1],
                       'x01': x01,
                       'x02': x02
                       }
            url = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
            req = scrapy.FormRequest(
                url, callback=self.proceeding_parse, formdata=frmdata)
            yield req

    def scrap_proceeding(self, response):
        proceeding = Proceeding(
            proceeding_no=response.css(
                '.rc-content-main > h1::text').get().split('-')[0].strip(),
            filed_by=response.css(
                '#P56_FILED_BY::text').get(),
            service_list=response.css(
                '#P56_SERVICE_LISTS > span > a::attr(href)').get(),
            industry=response.css(
                '#P56_INDUSTRY::text').get(),
            filling_date=response.css(
                '#P56_FILING_DATE::text').get(),
            category=response.css(
                '#P56_CATEGORY::text').get(),
            current_status=response.css(
                '#P56_STATUS::text').get(),
            description=response.css(
                '#P56_DESCRIPTION::text').get(),
            staff=response.css(
                '#P56_STAFF::text').get(),
            documents=[]
        )
        proceeding['total_documents'] = 0

        link = response.url.replace('56', '57')
        request = scrapy.Request(
            link, callback=self.scrap_documents,
            meta={'cookiejar': response.meta['cookiejar']})
        if request:
            request.meta['proceeding'] = proceeding
            yield request
        else:
            yield Proceeding

    def scrap_documents(self, response):
        print(response.url)
        proceeding = response.meta['proceeding']
        p_instance = response.css('#pInstance::attr(value)').get()
        x01 = response.css('#apexir_WORKSHEET_ID::attr(value)').get()
        x02 = response.css('#apexir_REPORT_ID::attr(value)').get()

        documents_links = []
        document_rows = response.css("#{} > tr + tr".format(x01)).getall()
        for document_row in document_rows:
            document_row = scrapy.Selector(text=document_row)
            document_link = document_row.css(
                "tr > td[headers*='DOCUMENT_TYPE'] > a::attr(href)").get()
            if document_link and re.search(r"http://docs.cpuc.ca.gov/SearchRes.aspx\?DocFormat=ALL&DocID=", document_link):
                if(response.url == "https://apps.cpuc.ca.gov/apex/wwv_flow.show"):
                    proceeding_document = response.meta['proceeding_document']
                else:
                    proceeding_document = ProceedingDocument()
                proceeding_document['filling_date'] = document_row.css(
                    "tr > td[headers*='FILING_DATE']::text").get()
                proceeding_document['document_type'] = document_row.css(
                    "tr > td[headers*='DOCUMENT_TYPE'] > a > span > u::text").get()
                proceeding_document['filed_by'] = document_row.css(
                    "tr > td[headers*='FILED_BY']::text").get()
                proceeding_document['description'] = document_row.css(
                    "tr > td[headers*='DESCRIPTION']::text").get()

                proceeding['total_documents'] += 1
                documents_links.append(document_link)
                request = scrapy.Request(
                    document_link, callback=self.scrap_document, dont_filter=True, meta={'cookiejar': response.meta['cookiejar']})
                request.meta['proceeding'] = proceeding
                request.meta['proceeding_document'] = proceeding_document
                yield request
        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            frmdata = {'p_request': 'APXWGT',
                       'p_instance': p_instance,
                       'p_flow_id': '401',
                       'p_flow_step_id': '57',
                       'p_widget_num_return': '100',
                       'p_widget_name': 'worksheet',
                       'p_widget_mod': 'ACTION',
                       'p_widget_action': 'PAGE',
                       'p_widget_action_mod': response.css(
                           '.fielddata > a::attr(href)').get().split("'")[1],
                       'x01': x01,
                       'x02': x02
                       }
            url = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
            req = scrapy.FormRequest(url, callback=self.scrap_documents, formdata=frmdata,
                                     headers={'Referer': response.url}, meta={'cookiejar': response.meta['cookiejar']})
            req.meta['proceeding'] = proceeding
            req.meta['proceeding_document'] = proceeding_document
            print(req.headers)
            print(req._body)
            yield req

        if not documents_links:
            yield proceeding

    def scrap_document(self, response):
        proceeding = response.meta['proceeding']
        proceeding_document = response.meta['proceeding_document']
        proceeding_document['link'] = response.url
        files = response.selector.xpath(
            '//table[@id="ResultTable"]/tbody/tr')  # css was not working
        proceeding_document['files'] = []
        for file in files:
            if(file.css('.ResultTitleTD').get()):
                document = Document(
                    title=re.sub(re.compile(r'<[^>]+>'), '',
                                 file.css('.ResultTitleTD').get()),
                    doc_type=file.css('.ResultTypeTD::text').get(),
                    pdf_link=urljoin(
                        'http://docs.cpuc.ca.gov', file.css(
                            '.ResultLinkTD > a::attr(href)').get()
                    ),
                    published_date=file.css('.ResultDateTD::text').get()
                )
                proceeding_document['files'].append(document)
        proceeding['documents'].append(proceeding_document)

        if len(proceeding['documents']) == proceeding['total_documents']:
            yield proceeding

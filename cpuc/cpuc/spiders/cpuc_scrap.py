# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor

from cpuc.items import Proceeding, ProceedingDocument, Document


class CpucScrapSpider(scrapy.Spider):
    name = 'cpuc_scrap'
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP/']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'p_t04': '01/01/2019',
                      'p_t05': '08/02/2019', 'p_request': 'Go'},
            callback=self.proceeding_parse
        )

    def proceeding_parse(self, response):
        proceeding_links = LinkExtractor(
            allow=r"f\?p=401:56:0::NO:RP,57,RIR:P5_PROCEEDING_SELECT:"
        ).extract_links(response)
        for link in proceeding_links:
            yield scrapy.Request(link.url, callback=self.scrap_proceeding)

    def scrap_proceeding(self, response):
        proceeding = Proceeding(
            proceeding_no=response.css(
                '.rc-content-main > h1::text').get().split('-')[0].strip(),
            filled_by=response.css(
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

        # print(self.data[proceeding_code])
        link = response.url.replace('56', '57')
        request = scrapy.Request(
            link, callback=self.scrap_documents)
        request.meta['proceeding'] = proceeding
        yield request

    def scrap_documents(self, response):
        proceeding = response.meta['proceeding']

        documents_links = LinkExtractor(
            allow=r"http://docs.cpuc.ca.gov/SearchRes.aspx\?DocFormat=ALL&DocID="
        ).extract_links(response)
        if documents_links:
            request = scrapy.Request(
                documents_links[0].url, callback=self.scrap_document, dont_filter=True)
            request.meta['proceeding'] = proceeding
            # proceeding_document = ProceedingDocument()
            # proceeding_document['link'] = link.url
            # proceeding_document['results'] = []
            # request.meta['proceeding_document'] = proceeding_document
            request.meta['documents_links'] = documents_links
            yield request
        else:
            yield proceeding

    def scrap_document(self, response):
        proceeding = response.meta['proceeding']
        documents_links = response.meta['documents_links']
        proceeding_document = ProceedingDocument()
        proceeding_document['link'] = documents_links[0].url
        results = response.selector.xpath(
            '//table[@id="ResultTable"]/tbody/tr')  # css was not working
        proceeding_document['results'] = []
        for result in results:
            if(result.css('.ResultTitleTD').get()):
                document = Document(
                    title=re.sub(re.compile(r'<[^>]+>'), '',
                                 result.css('.ResultTitleTD').get()),
                    doc_type=result.css('.ResultTypeTD::text').get(),
                    pdf_link=urljoin(
                        'http://docs.cpuc.ca.gov', result.css(
                            '.ResultLinkTD > a::attr(href)').get()
                    ),
                    published_date=result.css('.ResultDateTD::text').get()
                )
                proceeding_document['results'].append(document)
        documents_links.remove(documents_links[0])
        proceeding['documents'].append(proceeding_document)

        if documents_links:
            request = scrapy.Request(
                documents_links[0].url, callback=self.scrap_document, dont_filter=True)
            request.meta['proceeding'] = proceeding
            request.meta['documents_links'] = documents_links
            yield request
        else:
            yield proceeding

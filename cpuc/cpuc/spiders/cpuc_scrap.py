# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class CpucScrapSpider(scrapy.Spider):
    name = 'cpuc_scrap'
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP/']

    data = {}

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'p_t04': '01/01/2019',
                      'p_t05': '08/02/2019', 'p_request': 'Go'},
            callback=self.proceeding_parse
        )

    def proceeding_parse(self, response):
        proceeding_links = LinkExtractor(
            allow=r"f?p=401:56:0::NO:RP,57,RIR:P5_PROCEEDING_SELECT:"
        ).extract_links(response)
        for link in proceeding_links:
            yield scrapy.Request(link.url, callback=self.scrap_proceeding)

    def scrap_proceeding(self, response):
        proceeding_code = response.css(
            '.rc-content-main > h1::text').get().split('-')[0].strip()
        # print(proceeding_code)
        filled_by = response.css(
            '#P56_FILED_BY::text').get()
        service_list_url = response.css(
            '#P56_SERVICE_LISTS > span > a::attr(href)').get()
        industry = response.css(
            '#P56_INDUSTR::text').get()
        filling_date = response.css(
            '#P56_FILING_DATE::text').get()
        category = response.css(
            '#P56_CATEGORY::text').get()
        status = response.css(
            '#P56_STATUS::text').get()
        description = response.css(
            '#P56_DESCRIPTION::text').get()
        staff = response.css(
            '#P56_STAFF::text').get()

        self.data[proceeding_code] = {
            "filled_by": filled_by,
            "service_list_url": service_list_url,
            "industry": industry,
            "filling_date": filling_date,
            "category": category,
            "status": status,
            "description": description,
            "staff": staff
        }
        # print(self.data[proceeding_code])
        link = response.url.replace('56', '57')
        yield scrapy.Request(link, callback=self.scrap_documents)

    def scrap_documents(self, response):
        documents_links = LinkExtractor(
            allow=r"http: // docs.cpuc.ca.gov/SearchRes.aspx?DocFormat \
             = ALL & DocID =.*"
        ).extract_links(response)
        for link in documents_links:
            print(link.url)

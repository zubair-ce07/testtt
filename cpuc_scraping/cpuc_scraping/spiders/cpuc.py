# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from functools import partial
from ..items import CaseProceeding, Document


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

    def parse(self, response):
        form_data = {
            'p_flow_id': response.css("input#pFlowId::attr(value)").extract_first(default=""),
            'p_flow_step_id': response.css("input#pFlowStepId::attr(value)").extract_first(
                default=""),
            'p_instance': response.css("input#pInstance::attr(value)").extract_first(default=""),
            'p_page_submission_id': response.css(
                "input#pPageSubmissionId::attr(value)").extract_first(default=""),
            'p_request': 'Go',
            'p_arg_names': response.xpath(
                "//input[@id='PREPARE_URL']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t01': response.xpath(
                "preceding-sibling//input[@id='PREPARE_URL']/@value").extract_first(default=""),
            'p_arg_names': response.xpath(
                "//input[@id='P1_PROCEEDING_NUM']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t02': response.xpath(
                "preceding-sibling//input[@id='P1_PROCEEDING_NUM']/@value").extract_first(
                default=""),
            'p_arg_names': response.xpath(
                "//input[@id='P1_FILER_NAME']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t03': response.xpath(
                "preceding-sibling//input[@id='P1_FILER_NAME']/@value").extract_first(default=""),
            'p_arg_names': response.xpath(
                "//input[@id='P1_FILED_DATE_L']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t04': '01/01/2018',
            'p_arg_names': response.xpath(
                "//input[@id='P1_FILED_DATE_H']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t05': '08/29/2018',
            'p_arg_names': response.xpath(
                "//input[@id='P1_DESCRIPTION']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t06': response.xpath(
                "preceding-sibling//input[@id='P1_DESCRIPTION']/@value").extract_first(default=""),
            'p_arg_names': response.xpath(
                "//input[@id='P1_LAST_NAME']/preceding-sibling::input/@value").extract_first(
                default=""),
            'p_t07': response.xpath(
                "preceding-sibling//input[@id='P1_LAST_NAME']/@value").extract_first(default=""),

            'p_md5_checksum': response.xpath(
                "//input[@name='p_md5_checksum']/@value").extract_first(default=""),
            'p_page_checksum': response.xpath(
                "//input[@name='p_page_checksum']/@value").extract_first(default=""),
        }
        yield scrapy.FormRequest(url=self.search_page_url, formdata=form_data,
                                 callback=self.search_page)

    def search_page(self, response):
        yield from super().parse(response)
        # self.logger.info("i am search page")
        # self.logger.info("my url is %s" % response.url)

    def case_detail_page(self, response):
        proceeding = CaseProceeding()

        proceeding['number'] = response.css('h1::text').extract_first(default="").split(" ")[0]
        proceeding['filed_by'] = response.css("span#P56_FILED_BY::text").extract()
        proceeding['industry'] = response.css("span#P56_INDUSTRY::text").extract_first(default="")
        proceeding['filing_date'] = response.css("span#P56_FILING_DATE::text").extract_first(
            default="")
        proceeding['category'] = response.css("span#P56_CATEGORY::text").extract_first(default="")
        proceeding['status'] = response.css("span#P56_STATUS::text").extract_first(default="")
        proceeding['description'] = response.css("span#P56_DESCRIPTION::text").extract_first(
            default="")
        proceeding['staff_members'] = response.css("span#P56_STAFF::text").extract()
        proceeding['documents'] = []

        form_data = {
            'p_flow_id': response.css("input#pFlowId::attr(value)").extract_first(default=""),
            'p_flow_step_id': response.css("input#pFlowStepId::attr(value)").extract_first(
                default=""),
            'p_instance': response.css("input#pInstance::attr(value)").extract_first(default=""),
            'p_page_submission_id': response.css(
                "input#pPageSubmissionId::attr(value)").extract_first(default=""),
            'p_request': 'T_DOCUMENTS',
            'p_md5_checksum': "",
            'p_page_checksum': response.css("input#pPageChecksum::attr(value)").extract_first(
                default=""),
        }

        documents_url = response.css("form#wwvFlowForm::attr(action)").extract_first(default="")
        documents_url = response.urljoin(documents_url)

        yield scrapy.FormRequest(url=documents_url, formdata=form_data,
                                 callback=partial(self.document_list_page, proceeding=proceeding))

    def document_list_page(self, response, proceeding=None):
        documents_urls = response.css("tr.even a::attr(href)").extract()
        documents_urls = documents_urls + response.css("tr.odd a::attr(href)").extract()

        for document_url in documents_urls:
            if document_url.find('orderadocument') != -1:
                yield scrapy.Request(url=document_url,
                                     callback=partial(self.document_detail, proceeding=proceeding))

    def document_detail(self, response, proceeding=None):
        pass



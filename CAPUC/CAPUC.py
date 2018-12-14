import re

import scrapy
from CAPUC.items import Item
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule


class CapucParseSpider(scrapy.Spider):
    name = 'capuc-parser'

    proceeding_filings_url_t = 'https://apps.cpuc.ca.gov/apex/f?p=401:57:0::NO'

    def parse(self, response):

        item = Item()
        item['_id'] = self.extract_id(response)
        item['filed_on'] = self.extract_proceeding_filing_date(response)
        item['source_title'] = self.extract_title(response)
        item['source_url'] = self.extract_proceeding_url(response)
        item['state_id'] = self.extract_state_id(response)
        item['status'] = self.extract_proceeding_status(response)
        item['assignees'] = self.extract_proceeding_assignees(response)
        item['industries'] = self.extract_proceeding_industries(response)
        item['major_parties'] = self.extract_major_parties(response)
        item['proceeding_type'] = self.extract_proceeding_type(response)
        item['uploaded'] = 'true'
        item['state'] = 'CA'
        item['filings'] = []
        item['meta'] = []

        yield Request(self.proceeding_filings_url_t, meta={'item': item}, dont_filter=True,
                      callback=self.parse_proceeding_filings)

    def parse_proceeding_filings(self, response):

        item = response.meta['item']

        proceeding_filings = response.xpath('//table[@class="apexir_WORKSHEET_DATA"]')
        for raw_filing in proceeding_filings.xpath('.//tr'):
            filings = {}
            filings['filed_on'] = self.extract_filing_date(raw_filing)
            filings['source_filing_parties'] = self.extract_filing_parties(raw_filing)
            filings['description'] = self.extract_filing_description(raw_filing)
            filings['meta'] = {'docs_request': self.extract_docs_requests(raw_filing)}

            if filings['filed_on']:
                item['meta'].append(filings)

        if self.get_next_button(response):
            formdata = {
                'p_request': 'APXWGT',
                'p_widget_num_return': '100',
                'p_widget_name': 'worksheet',
                'p_widget_mod': 'ACTION',
                'p_widget_action': 'PAGE',
                'p_widget_action_mod': 'pgR_min_row={}max_rows=100rows_fetched=100'.format(
                    int(self.extract_current_filings(response) + 1)),
                'x01': self.extract_formdata_X01(response),
                'x02': self.extract_formdata_X02(response),
            }

            return FormRequest.from_response(response, formid='wwvFlowForm', formdata=formdata,
                                             callback=self.parse_proceeding_filings)

        return self.next_filing_or_item(item)

    def next_filing_or_item(self, item):

        if item['meta']:
            filing = item['meta'].pop(0)
            if filing['meta'].get('docs_request'):
                request = filing['meta'].get('docs_request')
                request.meta['item'] = item
                request.meta['filing'] = filing
                yield request

        else:
            del item['meta']
            yield item

    def extract_filing_docs(self, response):

        item = response.meta['item']
        filing = response.meta['filing']

        filings_docs = response.xpath('//table[@class="ResultTable"]')
        for raw_filing in filings_docs.xpath('.//tr'):
            filing['title'] = self.extract_filings_titles(raw_filing)
            filing['source_url'] = '{}{}'.format('http://docs.cpuc.ca.gov', self.extract_filings_docs_links(raw_filing))
            filing['blob_name'] = "{}-{}-{}".format(item['state'], item['state_id'],
                                                    filing['source_url'].split('/')[-1])
            filing['extension'] = filing['source_url'].rsplit('.', 1)
            filing['name'] = filing['source_url'].rsplit('/', 1)

        del filing['meta']
        item['filings'].append(filing)

        return self.next_filing_or_item(item)

    def extract_id(self, response):
        return response.css('.rounded-corner-region::attr(id)').extract_first()

    def extract_proceeding_filing_date(self, response):
        return response.css('#P56_FILING_DATE::text').extract_first()

    def extract_title(self, response):
        return response.css('#P56_DESCRIPTION::text').extract_first()

    def extract_proceeding_url(self, response):
        return response.url

    def extract_state_id(self, response):
        return response.css('div.rc-content-main h1::text').extract_first().split('-')[0]

    def extract_proceeding_status(self, response):
        return response.css('#P56_STATUS::text').extract_first()

    def extract_proceeding_assignees(self, response):
        return response.css('#P56_STAFF::text').extract_first()

    def extract_proceeding_industries(self, response):
        return response.css('#P56_INDUSTRY::text').extract_first()

    def extract_major_parties(self, response):
        return response.css('#P56_FILED_BY::text').extract_first()

    def extract_proceeding_type(self, response):
        return response.css('#P56_CATEGORY::text').extract_first()

    def extract_filing_date(self, raw_filing):
        return raw_filing.css('td[headers="FILING_DATE"]::text').extract()

    def extract_filing_parties(self, raw_filing):
        return raw_filing.css('td[headers="FILED_BY"]::text').extract()

    def extract_filing_description(self, raw_filing):
        return raw_filing.css('td[headers="DESCRIPTION"]::text').extract()

    def extract_docs_requests(self, raw_filing):
        if raw_filing.css('td[headers="DOCUMENT_TYPE"] a::attr(href)').extract_first():
            return Request(raw_filing.css('td[headers="DOCUMENT_TYPE"] a::attr(href)').extract_first(),
                           dont_filter=True, callback=self.extract_filing_docs)

    def extract_filings_titles(self, response):
        return response.xpath('//td[@class="ResultTitleTD"]//text()').extract()

    def extract_filings_docs_links(self, response):
        return response.xpath('//td[@class="ResultLinkTD"]//text()').extract()

    def extract_filing_source_url(self, raw_filing):
        return re.findall(r'(\/PublishedDocs.*?")', str(raw_filing[1]))[0].strip('"')

    def extract_current_filings(self, response):
        return re.findall(r"-(.*)of", response.xpath('//span[@class="fielddata"]//text()').extract_first())[0]

    def extract_formdata_X01(self, response):
        return response.xpath('//input[contains(@id,"apexir_WORKSHEET_ID")]/@value').extract()

    def extract_formdata_X02(self, response):
        return response.xpath('//input[contains(@id,"apexir_REPORT_ID")]/@value').extract()

    def get_next_button(self, response):
        return response.xpath('//td[@class="pagination"]//span//a//img//@title').extract()


class CapucCrawlSpider(CrawlSpider):
    name = 'capuc-crawler'
    start_urls = ['http://docs.cpuc.ca.gov/advancedsearchform.aspx']
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0(X11; Linux x86_64)AppleWebKit/537.36" \
                      "(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    base_url_t = 'http://docs.cpuc.ca.gov/advancedsearchform.aspx'
    proceeding_url_t = 'https://apps.cpuc.ca.gov/apex/f?p=401:56:12117329809176::NO:RP,57,RIR:P5_PROCEEDING_SELECT'
    page_count = 00

    capuc_parser = CapucParseSpider()

    def parse(self, response):

        formdata = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ddlCpuc01Types': '-1',
            'IndustryID': '-1',
            'FilingDateFrom': '12/01/17',
            'FilingDateTo': '12/01/18',
            'SearchButton': 'Search',
        }

        yield FormRequest.from_response(response, formid='frmSearchform', formdata=formdata,
                                        callback=self.parse_proceeding)

    def parse_proceeding(self, response):
        proceeding_ids = self.extract_proceeding_ids(response)

        for proceeding in proceeding_ids:
            yield Request('{}:{}'.format(self.proceeding_url_t, proceeding), callback=self.capuc_parser.parse)

        if response.xpath('//a[contains(@id,"lnkNextPage")]').extract():
            if self.page_count == 24:
                self.page_count = 00

            self.page_count += 1

            formdata = {
                '__EVENTTARGET': 'rptPages$ctl0{}$btnPage'.format(self.page_count),
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': self.get_viewstate(response),
                '__EVENTVALIDATION': self.get_eventvalidation(response),
                ' __VIEWSTATEGENERATOR': self.get_viewstategenerator(response),
            }

            yield FormRequest('http://docs.cpuc.ca.gov/SearchRes.aspx', formdata=formdata,
                              callback=self.parse_proceeding)

    def extract_proceeding_ids(self, response):
        proceedings_list = []
        proceedings = response.xpath('//table[@class="ResultTable"]//td[@class="ResultTitleTD"]//text()').extract()
        for proceeding in proceedings:
            if re.findall(r"(\w\d{7})", proceeding):
                proceedings_list.append(re.findall(r"(\w\d{7})", proceeding)[0])

        return proceedings_list

    def get_viewstate(self, response):
        return response.xpath('//input[contains(@id,"__VIEWSTATE")]/@value').extract_first()

    def get_viewstategenerator(self, response):
        return response.xpath('//input[contains(@id,"__VIEWSTATEGENERATOR")]/@value').extract_first()

    def get_eventvalidation(self, response):
        return response.xpath('//input[contains(@id,"__EVENTVALIDATION")]/@value').extract()

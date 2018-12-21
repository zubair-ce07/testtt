import json
import re

import scrapy
from nysdps.items import Item
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule


class NYSDPSSpider(CrawlSpider):
    name = 'nysdps-crawler'

    base_url = "http://documents.dps.ny.gov/public/CaseMaster/MatterExternal/17-02256?" \
               "MC=1&IA=&MT=&MST=&CN=&SDT={}&SDF={}&C=&M=&CO=0&_=1545114196465"
    proceeding_url = "http://documents.dps.ny.gov/public/CaseMaster/PublicDocuments/{}?_=1545127757859"
    source_url = "http://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterSeq={}&MNO={}"
    doc_url = "http://documents.dps.ny.gov/public/MatterManagement/MatterFilingItem.aspx?{}"

    start_date = '12/01/2017'
    end_date = '12/01/2018'

    def start_requests(self):

        yield Request(self.base_url.format(self.end_date, self.start_date), callback=self.parse_proceeding)

    def parse_proceeding(self, response):
        proceedings = json.loads(response.text)
        item = Item()

        for raw_proceeding in proceedings:
            item['source_major_parties'] = self.get_major_parties(raw_proceeding)
            item['_id'] = self.get_sequence_number(raw_proceeding)
            item['state_id'] = self.get_state_id(raw_proceeding)
            item['description'] = self.get_description(raw_proceeding)
            item['proceeding_type'] = self.get_proceeding_type(raw_proceeding)
            item['source_url'] = self.source_url.format(self.get_sequence_number(raw_proceeding),
                                                        self.get_state_id(raw_proceeding))
            item['filings'] = []
            item['meta'] = []

            yield Request(
                self.source_url.format(self.get_sequence_number(raw_proceeding), self.get_state_id(raw_proceeding)),
                meta={'item': item.copy()},
                callback=self.parse_industry)

    def parse_industry(self, response):
        item = response.meta['item']

        item['industries'] = self.get_industries(response)
        item['source_title'] = self.extract_source_title(response)

        yield Request(self.proceeding_url.format(item['_id']),
                      meta={'item': item.copy()},
                      callback=self.parse_fillings)

    def parse_fillings(self, response):
        fillings = json.loads(response.text)
        item = response.meta['item']

        for raw_filing in fillings:
            filing = {}
            filing['filed_on'] = raw_filing['DateFiled']
            filing['slug'] = raw_filing['DocRefNo']
            filing['filing_parties'] = raw_filing['FilingCompany']
            filing['meta'] = {'docs_request': self.extract_docs_requests(raw_filing)}

            if raw_filing['DocName']:
                filing['name'] = raw_filing['DocName']
                filing['extension'] = filing['name'].rsplit('.',1)[1]
            else:
                filing['name'] = self.extract_document_name(raw_filing)
                filing['extension'] = ''

            item['meta'].append(filing)

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

    def parse_documents(self, response):

        item = response.meta['item']
        filing = response.meta['filing']

        filing['description'] = self.extract_filing_description(response)
        filing['filing_parties'] = self.extract_filing_parties(response)
        filing['filed_on'] = self.extract_filing_date(response)
        filing['title'] = self.extract_filing_title(response)
        filing['source_filing_parties'] = self.extract_filing_parties(response)
        filing['source_url'] = self.extract_filing_source_url(response)
        filing['blob_name'] = "{}-{}-{}".format('NY', item['state_id'], filing['name'])

        del filing['meta']
        item['filings'].append(filing)

        return self.next_filing_or_item(item)

    def extract_docs_requests(self, filing):

        doc_link = re.findall(r"(FilingSeq.*?\')", filing['FilingNo'])[0]
        doc_link = doc_link.strip("'")
        return Request(self.doc_url.format(doc_link), callback=self.parse_documents)

    def get_sequence_number(self, response):
        matter_seq = re.findall(r"(MatterSeq=\d{5})", response['CaseOrMatterNumber'])[0]
        return matter_seq.strip("MatterSeq=")

    def get_state_id(self, response):
        state_id = re.findall(r"(>.*<)", response['CaseOrMatterNumber'])[0]
        return state_id.strip('>').strip('<')

    def get_major_parties(self, raw_proceeding):
        return raw_proceeding['MatterCompanies']

    def get_proceeding_id(self, raw_proceeding):
        return raw_proceeding['MatterID']

    def get_industries(self, response):
        return response.css('span#GridPlaceHolder_MatterControl1_lblIndustryAffectedValue::text').extract_first()

    def get_description(self, raw_proceeding):
        return raw_proceeding['MatterTitle']

    def get_proceeding_type(self, raw_proceeding):
        return raw_proceeding['MatterType']

    def extract_filing_description(self, response):
        return response.css('span#MatterDetail1_lblTitle::text').extract_first()

    def extract_filing_parties(self, response):
        return response.css('span#lblFilingonbehalfofval::text').extract_first()

    def extract_filing_date(selfself, response):
        return response.css('span#lblDateFiledval::text').extract_first()

    def extract_filing_title(self, response):
        return response.css('span#lblDescriptionofFilingval::text').extract_first()

    def exrtact_filing_parties(self, response):
        return response.css('span#lblFiledByval::text').extract_first()

    def extract_case_number(self, response):
        return response.css('span#MatterDetail1_lblCaseNumberVal::text').extract_first()

    def extract_filing_source_url(self, response):
        if response.css('a#grdMatterFilingDocuments_DgdCustomGrid_lnkDocTitle_0::attr(onclick)').extract():
            ref_id = re.findall(r"({.*})", response.css(
                'a#grdMatterFilingDocuments_DgdCustomGrid_lnkDocTitle_0::attr(onclick)').extract_first())[0]
            doc_ref_id = ref_id.strip('{').strip('}')
            return "http://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId={}".format(doc_ref_id)

    def extract_document_title(self, response):
        return response.css('a#grdMatterFilingDocuments_DgdCustomGrid_lnkDocTitle_0::text').extract()

    def extract_source_title(self, response):
        return response.xpath(
            '//textarea[@name="ctl00$GridPlaceHolder$MatterControl1$txtTitleofMatterValue"]//text()').extract_first()

    def extract_document_name(self, raw_filing):
        name = re.findall(r"(>.*<)", raw_filing['DocTitle'])[0]
        name = name.split('blank')[1]
        return name.strip("'>").strip('</a>')

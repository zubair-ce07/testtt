import re
import json

import scrapy
from nysdps.items import Item
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule


class NYSDPSSpider(CrawlSpider):
    name = 'nysdps-crawler'

    base_url = "http://documents.dps.ny.gov/public/CaseMaster/MatterExternal/17-02256?" \
               "MC=1&IA=&MT=&MST=&CN=&SDT=12/01/2018&SDF=12/01/2017&C=&M=&CO=0&_=1545114196465"
    proceeding_url = "http://documents.dps.ny.gov/public/CaseMaster/PublicDocuments/{}?_=1545127757859"
    doc_url = "http://documents.dps.ny.gov/public/MatterManagement/MatterFilingItem.aspx?{}"

    def start_requests(self):

        yield Request(self.base_url, callback=self.parse_proceeding)

    def parse_proceeding(self, response):
        proceedings = json.loads(response.text)
        item = Item()

        for raw_proceeding in proceedings:
            item['source_major_parties'] = self.get_major_parties(raw_proceeding)
            item['_id'] = self.get_proceeding_id(raw_proceeding)
            item['industries'] = self.get_industries(raw_proceeding)
            item['description'] = self.get_description(raw_proceeding)
            item['proceeding_type'] = self.get_proceeding_type(raw_proceeding)
            item['source_url'] = self.proceeding_url.format(self.get_sequence_number(raw_proceeding))
            item['filings'] = []
            item['meta'] = []

            yield Request(self.proceeding_url.format(self.get_sequence_number(raw_proceeding)),
                          meta={'item': item.copy()},
                          callback=self.parse_fillings)

    def parse_fillings(self, response):
        fillings = json.loads(response.text)
        item = response.meta['item']

        for raw_filing in fillings:
            filing = {}
            filing['filed_on'] = raw_filing['DateFiled']
            filing['extension'] = raw_filing['DocExt']
            filing['name'] = raw_filing['DocName']
            filing['slug'] = raw_filing['DocRefNo']
            filing['title'] = re.findall(r"(>.*<)", raw_filing['DocTitle'])
            filing['filing_parties'] = raw_filing['FilingCompany']
            filing['meta'] = {'docs_request': self.extract_docs_requests(raw_filing)}

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

        filing['title'] = self.extract_filing_title(response)
        filing['filing_parties'] = self.extract_filing_parties(response)
        filing['filed_on'] = self.extract_filing_date(response)
        filing['description'] = self.extract_filing_description(response)
        filing['source_filing_parties'] = self.extract_filing_parties(response)
        filing['source_url'] = self.extract_source_url(response)

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

    def get_major_parties(self, raw_proceeding):
        return raw_proceeding['MatterCompanies']

    def get_proceeding_id(self, raw_proceeding):
        return raw_proceeding['MatterID']

    def get_industries(self, raw_proceeding):
        return raw_proceeding['MatterSubType']

    def get_description(self, raw_proceeding):
        return raw_proceeding['MatterTitle']

    def get_proceeding_type(self, raw_proceeding):
        return raw_proceeding['MatterType']

    def extract_filing_title(self, response):
        return response.css('span#MatterDetail1_lblTitle::text').extract_first()

    def extract_filing_parties(self, response):
        return response.css('span#lblFilingonbehalfofval::text').extract_first()

    def extract_filing_date(selfself, response):
        return response.css('span#lblDateFiledval::text').extract_first()

    def extract_filing_description(self, response):
        return response.css('span#lblDescriptionofFilingval::text').extract_first()

    def exrtact_filing_parties(self, response):
        return response.css('span#lblFiledByval::text').extract_first()

    def extract_case_number(self, response):
        return response.css('span#MatterDetail1_lblCaseNumberVal::text').extract_first()

    def extract_source_url(self, response):
        if response.css('a#grdMatterFilingDocuments_DgdCustomGrid_lnkDocTitle_0::attr(onclick)').extract():
            ref_id = re.findall(r"({.*})", response.css(
                'a#grdMatterFilingDocuments_DgdCustomGrid_lnkDocTitle_0::attr(onclick)').extract_first())[0]
            doc_ref_id = ref_id.strip('{').strip('}')
            return "http://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId={}".format(doc_ref_id)

""" NY PUC Spider"""
import json
import logging
import re
from urllib.parse import urlencode, urljoin

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError
# Errors
from twisted.internet.error import (DNSLookupError, TCPTimedOutError,
                                    TimeoutError)
from w3lib.html import remove_tags

from puc_scaping.item_loaders.docket_loader import DocketLoader, FilingLoader
from puc_scaping.items.docket_item import DocketItem, DocumentItem, FilingItem
from puc_scaping.util.date_time_util import DateTimeUtil
from puc_scaping.util.util import remove_relativness


class DocketSpider(scrapy.Spider):
    """ Docket spider class for puc scraping"""
    name = 'docket'

    def __init__(self, from_date=None, to_date=None, *args, **kwargs):
        """ Docket Spider intializer"""
        super(DocketSpider, self).__init__(*args, **kwargs)

        base_domain = "documents.dps.ny.gov"
        self.from_date = from_date
        self.to_date = to_date
        self.base_url = f"http://{base_domain}/public/"
        self.allowed_domains = [base_domain]
        self.start_urls = [self.base_url]
        self.endpoints = {
            "search_result": "Common/SearchResults.aspx",
            "dockets": "CaseMaster/MatterExternal/",
            "docket_filings": "CaseMaster/PublicDocuments/",
            "docket_filing": "MatterManagement/MatterFilingItem.aspx",
            "file_doc": "Common/ViewDoc.aspx"
        }
        self.state_alpha_code = re.findall(r'(\w.?).gov', base_domain)[0]

    def start_requests(self):
        """This function validates date args get associated fields for dockets"""
        # date args validation
        self.validate_date_args()

        start_from_date = getattr(self, 'from_date', '')
        start_to_date = getattr(self, 'to_date', '')

        params_dict = {
            "MC": 1,
            "SDT": start_to_date,
            "SDF": start_from_date,
            "CO": 0
        }
        url = urljoin(self.base_url, self.endpoints['search_result'])
        search_url = f"{url}?{urlencode(params_dict)}"
        yield scrapy.Request(url=search_url,
                             callback=self.redirect_to_dockets,
                             errback=self.errback_docket,
                             dont_filter=True)

    def redirect_to_dockets(self, response):
        """functioon to generate final link to get dockets"""
        matter_sq_re = r"\bvar\s+MatterSeq\s*=\s*'(.*?)\?'\s*\+\s*\$\('(#.*?)'\)\[0\]\.value;\s*\n"

        matter_seq, query_params = response.css('script::text').re(
            matter_sq_re)
        querry_params = response.css(query_params).attrib['value']
        url = urljoin(self.base_url, self.endpoints['dockets'])
        url = f"{urljoin(url, matter_seq)}?{querry_params}"

        final_url = response.urljoin(url)

        yield scrapy.Request(url=final_url,
                             callback=self.parse_docket,
                             errback=self.errback_docket,
                             dont_filter=True)

    def parse_docket(self, response):
        """function for parsing docket data"""

        try:
            dockets_response = json.loads(response.body)
        except json.decoder.JSONDecodeError as exp:
            logging.error(
                f"Failed to parse json response from: {response.url}")
            logging.error(f"Error Deatils: {str(exp)}")
            raise CloseSpider("Invalid dockets data in response")

        for docket_obj in dockets_response:
            docket = DocketItem()

            matter_no_elem = docket_obj["CaseOrMatterNumber"]
            link = Selector(text=matter_no_elem).css("a").attrib['href']

            # Remove relative path's leading dots and / i-e ../
            link = remove_relativness(link)
            docket_url = urljoin(self.base_url, link)

            docket['filed_on'] = docket_obj["strSubmitDate"]
            docket['matter_id'] = str(docket_obj["MatterID"])
            docket['proceeding_sub_type'] = docket_obj["MatterSubType"]
            docket['proceeding_type'] = docket_obj["MatterType"]
            docket['source_url'] = docket_url
            docket['state'] = self.state_alpha_code.upper()
            docket['state_id'] = remove_tags(matter_no_elem)
            docket['status'] = docket_obj["Status"]
            docket['title'] = docket_obj["MatterTitle"]

            yield scrapy.Request(url=docket['source_url'],
                                 meta={"docket": docket},
                                 callback=self.parse_docket_details,
                                 errback=self.errback_docket,
                                 dont_filter=True)

    def parse_docket_details(self, response):
        """This function parses docket details"""
        docket = response.meta["docket"]
        docket_loader = DocketLoader(item=docket, response=response)
        INDUSTRY_SEL = "#GridPlaceHolder_MatterControl1_lblIndustryAffectedValue"
        PARTIES_SEL = "#GridPlaceHolder_MatterControl1_pnlCompanyValue table td"
        JUDGE_SEL = "#GridPlaceHolder_MatterControl1_lblPnlAssignedJudge"

        docket_loader.add_css("industries", INDUSTRY_SEL)
        docket_loader.add_css("major_parties", PARTIES_SEL)
        docket_loader.add_css("assignees", JUDGE_SEL)

        link = urljoin(self.base_url, self.endpoints['docket_filings'])
        docs_url = urljoin(link, docket["matter_id"])
        docket = docket_loader.load_item()

        yield scrapy.Request(url=docs_url,
                             meta={"docket": docket},
                             callback=self.parse_filings,
                             errback=self.errback_docket,
                             dont_filter=True)

    def parse_filings(self, response):
        """This function parses docket filings"""
        docket = response.meta["docket"]

        try:
            filings = json.loads(response.body)

            docket['filings'] = []
            for filing in filings:
                filing_item = FilingItem()
                filing_item['types'] = [filing['Doctype']]

                filing_data = Selector(
                    text=filing['FilingNo']).css('a::attr(onclick)')
                endpoint, params = filing_data.re(
                    r"^javascript:.*\('(.*)',\s*'(.*)'\)")
                endpoint = remove_relativness(endpoint)

                fling_url = f"{urljoin(self.base_url, endpoint)}?{params}"

                yield scrapy.Request(url=fling_url,
                                     meta={
                                         "docket": docket,
                                         "filing": filing_item
                                     },
                                     callback=self.parse_filing,
                                     errback=self.errback_docket,
                                     dont_filter=True)

        except json.decoder.JSONDecodeError as exp:
            logging.error(
                f"Failed to parse json response from: {response.url}")
            logging.error(f"Error Deatils: {str(exp)}")
            yield docket

    def parse_filing(self, response):
        """This function parses docket filings each file and its related docs"""
        docket = response.meta["docket"]
        # get the last filing item
        filing = response.meta["filing"]
        STATE_ID_SELECTOR = "#MatterDetail1_lblMatterNumberVal"
        DATE_FILED_SELECTOR = "#lblDateFiledval"
        DESCRIPTION_SELECTOR = "#lblDescriptionofFilingval"
        PARTIES_SELECTOR = "#lblFiledByval"
        SRC_PARTIES_SELECTOR = "lblFilingonbehalfofval"
        DOCS_SELECTOR = "#grdMatterFilingDocuments_DgdCustomGrid tr:not(:first-child)"

        # Regexp for selecting doc download link and doc type
        PATTERN = r"^javascript.*\('.*'\,'(\w+={[-\w]+})\&DocExt=(\w+)&.*"

        filing_loader = FilingLoader(item=filing, response=response)
        filing_loader.add_css("state_id", STATE_ID_SELECTOR)
        filing_loader.add_css("filed_on", DATE_FILED_SELECTOR)
        filing_loader.add_css("description", DESCRIPTION_SELECTOR)
        filing_loader.add_css("filing_parties", PARTIES_SELECTOR)
        filing_loader.add_css("source_filing_parties", SRC_PARTIES_SELECTOR)
        filing = filing_loader.load_item()

        # set for filing types as filing can have multiple docs with same types
        filing_types = set()
        if filing['types']:
            for file_type in filing['types']:
                filing_types.add(file_type)

        docs = response.css(DOCS_SELECTOR)
        documents = []
        for doc in docs:
            document = DocumentItem()
            # 1st colum: download source url an doc type
            row_data = doc.css('td')
            doc_ref, extension = row_data[0].css('a::attr(onclick)').re(
                PATTERN)
            link = urljoin(self.base_url, self.endpoints['file_doc'])
            doc_source = f"{link}?{doc_ref}"
            name_exp = re.findall(r'DocRefNo=(\{[-\w]+\})', doc_ref)
            doc_name = None
            blob_name = None
            if name_exp and extension:
                doc_name = f"{name_exp[0]}.{extension}"
                blob_name = self.generate_blob_name(filing['state_id'],
                                                    doc_name)

            # 2nd column: title
            title = row_data[1].css('a::text').get()
            # 3rd column: proceeding Type
            filing_types.add(row_data[2].css('::text').get())

            document["blob_name"] = blob_name
            document["extension"] = extension
            document["name"] = doc_name
            document["onS3"] = False
            document["source_url"] = doc_source
            document["title"] = title
            documents.append(document)

        filing['types'] = list(filing_types)
        filing["documents"] = documents

        docket["filings"].append(filing)
        yield docket

    def generate_blob_name(self, filiing_id, doc_name):
        """This function craeted blob name for filing doc"""
        return f"{self.state_alpha_code.upper()}-{filiing_id}-{doc_name}"

    def validate_date_args(self):
        """This function validates froma and to date"""
        DATE_FORMAT = "%m/%d/%Y"
        if not DateTimeUtil.validate_dates(self.from_date, self.to_date,
                                           DATE_FORMAT):
            raise CloseSpider("Invalid date argumemts")

    def errback_docket(self, failure):
        """This function logs all errback failures"""
        logging.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            logging.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            logging.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logging.error('TimeoutError on %s', request.url)

""" NY PUC Spider"""
import json
import logging
import re
import sys
from datetime import datetime
from urllib.parse import urlencode

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from w3lib.html import remove_tags

from puc_scaping.item_loaders.docket_loader import DocketLoader, FilingLoader
from puc_scaping.items.docket_item import DocketItem, DocumentItem, FilingItem


class DocketSpider(scrapy.Spider):
    """ Docket spider class for puc scraping"""
    name = 'docket'

    def __init__(self, from_date=None, to_date=None, *args, **kwargs):
        """ Docket Spider intializer"""
        super(DocketSpider, self).__init__(*args, **kwargs)

        DATE_FORMAT = "%m/%d/%Y"
        if not validate_date_args(from_date, to_date, DATE_FORMAT):
            raise CloseSpider()

        self.from_date = from_date
        self.to_date = to_date

        self.base_url = "http://documents.dps.ny.gov/public/"
        self.state_alpha_code = "NY"

    def start_requests(self):
        """This function gets associated fields for dockets"""

        params = {"MC": 1, "SDT": self.to_date, "SDF": self.from_date, "CO": 0}

        search_url = f"{self.base_url}Common/SearchResults.aspx?{urlencode(params)}"
        yield scrapy.Request(url=search_url,
                             callback=self.get_dockets,
                             errback=self.errback_docket)

    def get_dockets(self, response):
        """functioon to generate final link to get dockets"""
        matter_sq_re = r"\bvar\s+MatterSeq\s*=\s*'(.*?)\?'\s*\+\s*\$\('(#.*?)'\)\[0\]\.value;\s*\n"

        matter_seq, query_params_css = response.css('script::text').re(
            matter_sq_re)
        querry_params = response.css(query_params_css).attrib['value']
        url = f"{self.base_url}CaseMaster/MatterExternal/{matter_seq}?{querry_params}"

        yield scrapy.Request(url=url,
                             callback=self.parse_docket,
                             errback=self.errback_docket)

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

            matter_no_sel = Selector(text=docket_obj["CaseOrMatterNumber"])
            link = matter_no_sel.css("a").attrib['href']

            # Remove relative path's leading dots and / i-e ../
            link = remove_relativeness(link)

            docket_url = f"{self.base_url}{link}"

            docket['filed_on'] = docket_obj["strSubmitDate"]
            docket['matter_id'] = str(docket_obj["MatterID"])
            docket['proceeding_sub_type'] = docket_obj["MatterSubType"]
            docket['proceeding_type'] = docket_obj["MatterType"]
            docket['source_url'] = docket_url
            docket['state'] = self.state_alpha_code.upper()
            docket['state_id'] = matter_no_sel.css("a::text").get()
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
        INDUSTRY_CSS = "#GridPlaceHolder_MatterControl1_lblIndustryAffectedValue"
        PARTIES_CSS = "#GridPlaceHolder_MatterControl1_pnlCompanyValue table td"
        JUDGE_CSS = "#GridPlaceHolder_MatterControl1_lblPnlAssignedJudge"

        docket_loader.add_css("industries", INDUSTRY_CSS)
        docket_loader.add_css("major_parties", PARTIES_CSS)
        docket_loader.add_css("assignees", JUDGE_CSS)

        docs_url = f"{self.base_url}CaseMaster/PublicDocuments/{docket['matter_id']}"
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
        except json.decoder.JSONDecodeError as exp:
            logging.error(
                f"Failed to parse json response from: {response.url}")
            logging.error(f"Error Details: {str(exp)}")
            yield docket

        docket["filings"] = []
        is_last = False
        filings_count = len(filings)

        for index, filing in enumerate(filings):
            filing_item = FilingItem()
            filing_item['types'] = [filing['Doctype']]

            filing_data = Selector(
                text=filing['FilingNo']).css('a::attr(onclick)')
            endpoint, params = filing_data.re(
                r"^javascript:.*\('(.*)',\s*'(.*)'\)")
            endpoint = remove_relativeness(endpoint)

            filing_url = f"{self.base_url}{endpoint}?{params}"

            if (index == filings_count - 1):
                is_last = True

            yield scrapy.Request(url=filing_url,
                                 meta={
                                     "docket": docket,
                                     "filing": filing_item,
                                     "is_last": is_last
                                 },
                                 callback=self.parse_filing_documents,
                                 errback=self.errback_docket,
                                 dont_filter=True)

    def parse_filing_documents(self, response):
        """This function parses docket filings each file and its related docs"""
        docket = response.meta["docket"]
        # get the last filing item
        filing = response.meta["filing"]
        is_last = response.meta["is_last"]

        STATE_ID = "#MatterDetail1_lblMatterNumberVal"
        DATE_FILED = "#lblDateFiledval"
        DESCRIPTION = "#lblDescriptionofFilingval"
        PARTIES = "#lblFiledByval"
        SRC_PARTIES = "lblFilingonbehalfofval"
        DOCS = "#grdMatterFilingDocuments_DgdCustomGrid tr:not(:first-child)"

        # Regexp for selecting doc download link and doc type
        PATTERN = r"^javascript.*\('.*'\,'(\w+={[-\w]+})\&DocExt=(\w+)&.*"

        filing_loader = FilingLoader(item=filing, response=response)
        filing_loader.add_css("state_id", STATE_ID)
        filing_loader.add_css("filed_on", DATE_FILED)
        filing_loader.add_css("description", DESCRIPTION)
        filing_loader.add_css("filing_parties", PARTIES)
        filing_loader.add_css("source_filing_parties", SRC_PARTIES)
        filing = filing_loader.load_item()

        # set for filing types as filing can have multiple docs with same types
        filing_types = set()
        if filing['types']:
            for file_type in filing['types']:
                filing_types.add(file_type)

        docs = response.css(DOCS)
        documents = []
        for doc in docs:
            document = DocumentItem()
            # 1st colum: download source url an doc type
            row_data = doc.css('td')
            doc_ref, extension = row_data[0].css('a::attr(onclick)').re(
                PATTERN)
            doc_source = f"{self.base_url}Common/ViewDoc.aspx?{doc_ref}"
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

        if (is_last):
            yield docket

    def generate_blob_name(self, filiing_id, doc_name):
        """This function craetes blob name for filing doc"""
        return f"{self.state_alpha_code.upper()}-{filiing_id}-{doc_name}"

    def errback_docket(self, failure):
        """This function logs all errback failures"""
        logging.error(repr(failure))


def remove_relativeness(link_str):
    """This function removes the '../' from start of url"""
    # or re.sub("^../|/$", "", link_str)
    return link_str.strip("../")


def validate_date_args(from_date, to_date, date_format):
    """
    Validates and Compare if both from and to date are not in future and
    from date is not ahead of to date
    Parameters:
        from_date (str): from date string.
        to_date (str): to date string
        date_format (str): Format of the given dates
    Returns:
        bool: True if valid and False incase of invalid
    """
    if not (from_date and to_date):
        logging.error("from date or to date missing")
        return False

    today = datetime.now()

    try:
        f_date = datetime.strptime(from_date, date_format)
        t_date = datetime.strptime(to_date, date_format)
    except ValueError:
        logging.error("Invald date format: <MM/DD/YYYY>")
        return False

    if (f_date > today or t_date > today):
        logging.error("From and to date must not be in future")
        return False

    if f_date > t_date:
        logging.error("From date must be less than or equal to to date")
        return False

    return True

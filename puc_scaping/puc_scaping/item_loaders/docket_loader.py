"""Docket and related Loader"""
import re
from scrapy.loader.processors import Identity
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags

from .base_loader import BaseLoader
from puc_scaping.util.date_time_util import DateTimeUtil


def format_date(date_string):
    if date_string:
        # check if already formatted in July 25, 2017 format:
        matches = re.match(r"^[A-Za-z]+\s[0-9]{2}\,\s[0-9]+", date_string)
        if (matches):
            return date_string
        input_format = "%m/%d/%Y"
        output_format = "%B %d, %Y"
        return DateTimeUtil.format_date(date_string, input_format,
                                        output_format)


class DocketLoader(BaseLoader):
    """Docket Loader class with custom processors"""
    major_parties_out = Identity()
    filed_on_in = MapCompose(remove_tags, format_date)
    filings_out = Identity()
    filings_in = MapCompose()


class FilingLoader(BaseLoader):
    """Filing Loader class with custom processors"""
    types_out = Identity()
    filing_parties_out = Identity()
    source_filing_parties_out = Identity()
    documents_out = Identity()

    documents_in = MapCompose()

    filed_on_in = MapCompose(remove_tags, format_date)

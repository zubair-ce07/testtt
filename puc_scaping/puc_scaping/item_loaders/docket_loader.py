"""Docket and related Loader"""
import logging
from datetime import datetime

from scrapy.loader.processors import Identity, MapCompose
from w3lib.html import remove_tags

from .base_loader import BaseLoader


def parse_date(date_str, date_format, log_error=True):
    date_obj = None
    try:
        date_obj = datetime.strptime(date_str, date_format)
    except ValueError as exp:
        if (log_error):
            logging.error(f"Error in pasring date: {str(exp)}")

    return date_obj


def format_date(date_string):
    if date_string:
        input_format = "%m/%d/%Y"
        output_format = "%B %d, %Y"

        # check if already formatted in July 25, 2017 format:
        date_obj = parse_date(date_string, output_format, False)
        if (date_obj):
            return date_string

        date_obj = parse_date(date_string, input_format)
        return datetime.strftime(date_obj, output_format)


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

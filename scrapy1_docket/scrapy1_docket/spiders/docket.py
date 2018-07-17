# -*- coding: utf-8 -*-
import re

import scrapy

from .. import items


class DocketSpider(scrapy.Spider):
    name = 'docket'
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.is_description_spanning, self.is_filer_spanning, self.is_docket_spanning = False, False, False

    def parse(self, response):
        PATH = '/html/body/table[3]/tr[1]/td[3]/table/tr'
        self.all_rows = response.xpath(PATH)
        row_index = 0
        while row_index < len(self.all_rows):
            self.item = items.DocketItem()
            self.parse_row_for_item(row_index, self.item, False, False)

            if self.is_special_case(row_index):
                self.handle_special_case(row_index)
                yield self.item
                yield self.item2
                self.is_description_spanning, self.is_filer_spanning, self.is_docket_spanning = False, False, False
                row_index += 2
            else:
                yield self.item
                row_index += 1

    def parse_row_for_item(self, row_index, item, is_single_span, is_double_span):
        column_no = 0 if is_single_span else 1
        item['docket'] = self.get_value_from_column(self.all_rows[row_index], 1)
        item['filer'] = self.get_value_from_column(self.all_rows[row_index], column_no + 1 if not is_double_span else 1)
        item['description'] = self.get_value_from_column(self.all_rows[row_index], column_no + 2 if not is_double_span else 1)
        item['filed_date'] = self.get_filer_from_description(self.item['description'])

    def get_value_from_column(self, row, colunm_no):
        return row.xpath('td[{}]//text()'.format(colunm_no)).extract_first()

    def get_filer_from_description(self, description):
        if description is None: return "Not Available"
        date = re.search(r'(\d+/\d+/\d+)', description)
        if date: return date.group()
        return "Not Available"

    def handle_special_case(self, row_index):
        self.item2 = items.DocketItem()
        self.parse_row_for_item(row_index+1, self.item2, True, self.get_is_double_span())

        if self.is_docket_spanning:
            self.item2['docket'] = self.item['docket']
        if self.is_filer_spanning:
            self.item2['filer'] = self.item['filer']
        if self.is_description_spanning:
            self.item2['description'] = self.item['description']
            self.item2['filed_date'] = self.item['filed_date']

    def get_is_double_span(self):
        if self.is_description_spanning and self.is_filer_spanning:
            return True
        if self.is_filer_spanning and self.is_docket_spanning:
            return True
        if self.is_description_spanning and self.is_docket_spanning:
            return True

    def is_special_case(self, index):
        if self.all_rows[index].xpath('td[1]/@rowspan').extract_first() is not None:
            self.is_docket_spanning = True
        if self.all_rows[index].xpath('td[2]/@rowspan').extract_first() is not None:
            self.is_filer_spanning = True
        if self.all_rows[index].xpath('td[3]/@rowspan').extract_first() is not None:
            self.is_description_spanning = True

        if True in [self.is_description_spanning, self.is_docket_spanning, self.is_filer_spanning]:
            return True
        return False

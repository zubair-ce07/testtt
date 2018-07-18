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
        PATH = '//td[@class="normal"]//tr'
        self.all_rows = response.xpath(PATH)
        row_index = 0
        while row_index < len(self.all_rows):
            item = items.DocketItem()
            self.parse_row_for_item(row_index, item, False, False)
            self.detect_spanning(self.all_rows[row_index], item)

            if self.is_special_case():
                yield item
                for new_item in self.handle_special_case(row_index, item):
                    yield new_item
                row_index += int(item['max_span'])
            else:
                yield item
                row_index += 1
            self.is_description_spanning, self.is_filer_spanning, self.is_docket_spanning = False, False, False

    def parse_row_for_item(self, row_index, item, is_single_span, is_double_span):
        column_no = 0 if is_single_span else 1
        item['docket'] = self.get_value_from_column(self.all_rows[row_index], 1)
        item['file_url'] = self.all_rows[row_index].xpath('td[1]/a/@href').extract_first()
        item['filer'] = self.get_value_from_column(self.all_rows[row_index], column_no + 1 if not is_double_span else 1)
        item['description'] = self.get_value_from_column(self.all_rows[row_index], column_no + 2 if not is_double_span else 1)
        item['filed_date'] = self.get_filed_date_from_description(item['description'])


    def get_value_from_column(self, row, colunm_no):
        return row.xpath('td[{}]//text()'.format(colunm_no)).extract_first()

    def get_filed_date_from_description(self, description):
        if description is None: return "Not Available"
        date = re.search(r'(\d+/\d+/\d+)', description)
        if date: return date.group()
        return "Not Available"

    def handle_special_case(self, row_index, item):

        index = 1
        while index < int(item['max_span']):
            item2 = items.DocketItem()
            self.parse_row_for_item(row_index+index, item2, True, self.get_is_double_span())

            if self.is_docket_spanning:
                item2['docket'] = item['docket']
                item2['file_url'] = item['file_url']
            if self.is_filer_spanning:
                item2['filer'] = item['filer']
            if self.is_description_spanning:
                item2['description'] = item['description']
                item2['filed_date'] = item['filed_date']
            yield item2
            index += 1

    def get_is_double_span(self):
        if self.is_description_spanning and self.is_filer_spanning:
            return True
        if self.is_filer_spanning and self.is_docket_spanning:
            return True
        if self.is_description_spanning and self.is_docket_spanning:
            return True

    def detect_spanning(self, row, item):
        if row.xpath('td[1]/@rowspan').extract_first() is not None:
            self.is_docket_spanning = True
            item['max_span'] = row.xpath('td[1]/@rowspan').extract_first()
        if row.xpath('td[2]/@rowspan').extract_first() is not None:
            self.is_filer_spanning = True
            item['max_span'] = row.xpath('td[2]/@rowspan').extract_first()
        if row.xpath('td[3]/@rowspan').extract_first() is not None:
            self.is_description_spanning = True
            item['max_span'] = row.xpath('td[3]/@rowspan').extract_first()

    def is_special_case(self):
        if True in [self.is_description_spanning, self.is_docket_spanning, self.is_filer_spanning]:
            return True
        return False

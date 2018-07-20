import re
import scrapy

from docket.items import DocketItem


class DocketSpider(scrapy.Spider):
    name = "docketinfo"
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html', ]

    def parse(self, response):
        table_rows = len(response.css('td.normal tr')) - 1
        sel_trs = response.css('td.normal tr:nth-child(n+2)')
        index = 0
        while index < table_rows:
            tr = sel_trs[index]
            row_span, spanning_info = self.get_max_rowspan(tr)
            if int(row_span) > 1:
                special_case_trs = sel_trs[index: index + int(row_span)]
                for item in self.handle_special_case(special_case_trs, spanning_info):
                    yield item
                index += int(row_span)
            else:
                yield self.handle_normal_case(tr)
                index += 1

    def handle_special_case(self, special_case_trs, spanning_info):
        items = []
        index = 1
        tr = special_case_trs[0]
        td1 = tr.xpath('./child::td[1]')
        td2 = tr.xpath('./child::td[2]')
        td3 = tr.xpath('./child::td[3]')
        items.append(self.create_item(td1, td2, td3))
        while index < len(special_case_trs):
            tr = special_case_trs[index]
            if spanning_info[2] != '1':  # Case 1
                td2 = tr.xpath('./child::td[1]')
            elif spanning_info[0] != '1' and spanning_info[1] != '1':  # Case 2
                td3 = tr.xpath('./child::td[1]')
            elif spanning_info[0] != '1':  # Case 3
                td2 = tr.xpath('./child::td[1]')
                td3 = tr.xpath('./child::td[2]')
            else:  # Case 4
                td1 = tr.xpath('./child::td[1]')
                td3 = tr.xpath('./child::td[2]')
            items.append(self.create_item(td1, td2, td3))
            index += 1
        return items

    def get_max_rowspan(self, tr):
        CHECK_ROWSPAN = './child::td[{td}]/@rowspan'
        td1_rowspan = tr.xpath(CHECK_ROWSPAN.format(td=1)).extract_first('1')
        td2_rowspan = tr.xpath(CHECK_ROWSPAN.format(td=2)).extract_first('1')
        td3_rowspan = tr.xpath(CHECK_ROWSPAN.format(td=3)).extract_first('1')
        return max(td1_rowspan, td2_rowspan, td3_rowspan), [td1_rowspan, td2_rowspan, td3_rowspan]

    def handle_normal_case(self, tr):
        td1 = tr.xpath('./child::td[1]')
        td2 = tr.xpath('./child::td[2]')
        td3 = tr.xpath('./child::td[3]')
        return self.create_item(td1, td2, td3)

    def create_item(self, td1, td2, td3):
        item = DocketItem()
        item['docket_id'] = td1.css('*::text').extract_first()
        item['file_url'] = td1.css('a::attr(href)').extract_first()
        item['filer'] = td2.css('*::text').extract_first()
        item['description'] = td3.css('*::text').extract_first()
        date = re.search(r'(\d+/\d+/\d+)', item['description'])
        item['date_filed'] = date.group() if date else 'Not Available'
        return item


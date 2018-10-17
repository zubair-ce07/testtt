import scrapy
import re

from ScrapyPractice.items import Record


class RipucSpider(scrapy.Spider):
    """
    Spider to scrap table from webpage: 'http://www.ripuc.org/eventsactions/docket.html' and yield a dictionary of
    format {'docket': , 'filler': , 'description': } against each row in table
    """
    name = 'RIPUC'

    start_urls = [
        'http://www.ripuc.org/eventsactions/docket.html'
    ]

    def parse(self, response):
        for table_row in response.xpath('//table[@border="1"]/*[td[not(@class="smallheader")]]'):
            # iterate over all row except for the header row
            row_cols = table_row.xpath('./td')  # take columns of each row

            if len(row_cols) == 3:
                # if a row have 3 columns meaning no column is missing in rowspan
                docket = ''.join([x.strip() for x in row_cols[0].css('td ::text').extract()])
                filler = ''.join([x.strip() for x in row_cols[1].css('td ::text').extract()])
                description = ''.join([x.strip() for x in row_cols[2].css('td ::text').extract()])
            else:
                # else check for latest previous rows that have any td with rowspan and check which one it is,
                docket_from_rowspan = table_row.xpath('./preceding-sibling::tr[td[@rowspan]][1]/td[1][@rowspan]')
                if docket_from_rowspan:
                    # if 1st column of a preceding row has row span
                    docket = ''.join([x.strip() for x in docket_from_rowspan.css('td ::text').extract()])
                else:
                    docket = ''.join([x.strip() for x in row_cols[0].css('td ::text').extract()])
                    del row_cols[0]

                filler_from_rowspan = table_row.xpath('./preceding-sibling::tr[td[@rowspan]][1]/td[2][@rowspan]')
                if filler_from_rowspan:
                    # if second column of a preceding row has row span
                    filler = ''.join([x.strip() for x in filler_from_rowspan.css('td ::text').extract()])
                else:
                    filler = ''.join([x.strip() for x in row_cols[0].css('td ::text').extract()])
                    del row_cols[0]

                description_from_rowspan = table_row.xpath('./preceding-sibling::tr[td[@rowspan]][1]/td[3][@rowspan]')
                if description_from_rowspan:
                    # if 1st column of a preceding row has row span
                    description = ''.join([x.strip() for x in description_from_rowspan.css('td ::text').extract()])
                else:
                    description = ''.join([x.strip() for x in row_cols[0].css('td ::text').extract()])

            # remove extra escape sequences and spaces
            docket = ' '.join(docket.split())
            filler = ' '.join(filler.split())
            description = ' '.join(description.split())
            date_filed = ""

            dates_in_descriptions = re.findall('([0-9]+/[0-9]+/[0-9]+)', description)

            if dates_in_descriptions:
                date_filed = dates_in_descriptions

            if docket != '':
                # docket number is available yield data
                record = Record(
                    docket=docket,
                    filler=filler,
                    description=description,
                    date_filed=date_filed,
                )
                yield record

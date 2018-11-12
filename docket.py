# -*- coding: utf-8 -*-
import scrapy
import re


class DocketSpider(scrapy.Spider):
    name = 'docket'
    allowed_domains = ['ripuc.org']
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']
    base_url = 'http://www.ripuc.org/eventsactions/docket.html'

    def parse(self, response):
        previous_id = ''
        table = response.xpath('//table[3]//td[@class="normal"]//table[@width = "100%"]/tr')
        for row in table:
            identifier = row.css('a::text').extract_first('') or row.css('td::text').extract_first('')
            valid_identifier = re.search('\d\d\d\d', identifier.split('-')[0])
            previous_id = identifier if valid_identifier else previous_id
            if not valid_identifier:
                identifier = previous_id

            # selecting second column
            for row_two in row.css('td:nth-child(2)'):
                if row_two.css('td:last-child'):
                    break

                previous_value = ''
                value = row_two.css('::text').extract_first('') or row_two.css('.normal::text').extract_first('')
                if not value or value == identifier:
                    previous_value =  row_two.css('p:first-child::text').extract()
                    value = previous_value
                    continue

            # selecting 3 column
            for row_three in row.css('td:nth-child(3)'):
                if not row_three:
                    break
                description = row_three.css('::text').extract_first('') or row_three.css('.normal::text').extract_first('')

            # extracting date from 3rd column
            date_filed = row.xpath('//td//text()').re(r'\d{1,2}\/\d{1,2}\/\/?\d{1,4}')
            yield {
                'identifier': identifier.strip('').strip().strip(')'),
                'value': value.strip().strip(')'),
                'description': description.strip(),
                'date_filed': date_filed,
            }

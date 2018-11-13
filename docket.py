# -*- coding: utf-8 -*-
import scrapy
import re


class DocketSpider(scrapy.Spider):
    name = 'docket'
    allowed_domains = ['ripuc.org']
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']
    base_url = 'http://www.ripuc.org/eventsactions/docket.html'

    def parse(self, response):
        identifier = ''
        previous_id = ''
        table = response.xpath('//table[3]//td[@class="normal"]//table[@width = "100%"]/tr')
        for row in table:
            id = row.xpath('.//td[last()-2]//a//text()').extract() or row.xpath('.//td[last()-2]//text()').extract()
            for i in id:
                identifier = i
                continue

            val = row.xpath('.//td[last()-1]//text()').extract()
            for v in val:
                value = v
                continue

            descrip = row.xpath('.//td[last()-0]//text()')
            for desc in descrip:
                description = descrip.extract_first()
                continue

            dates = row.xpath('.//td[last()-0]//text()').re(r'\d{1,2}\/\d{1,2}\/\/?\d{1,4}')
            date_filed = dates

            yield {
                'identifier': identifier.strip('').strip().strip(')'),
                'value': value.strip().strip(')'),
                'description': description.strip(),
                'date_filed': date_filed,
            }


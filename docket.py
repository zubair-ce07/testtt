# -*- coding: utf-8 -*-
import scrapy
from items import DocketSpiderItem
import re


class DocketSpider(scrapy.Spider):
    name = 'docket'
    allowed_domains = ['ripuc.org']
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']
    base_url = 'http://www.ripuc.org/eventsactions/docket.html'

    def parse(self, response):
        docket = DocketSpiderItem()
        identifier = ''
        table = response.xpath('//table[3]//td[@class="normal"]//table[@width = "100%"]/tr')
        for row in table:
            docket_id = row.xpath('.//td[last()-2]//a//text()').extract() or row.xpath('.//td[last()-2]//text()').extract() or \
            row.xpath('.//td[@class="normal"]//text()').extract()
            for i in docket_id:
                identifier = i
                if identifier == "":
                    identifier = row.xpath('string(.//td[1][@class="normal"]//text())').extract()

            filer_names = row.xpath('.//td[last()-1]//text()').extract() or row.xpath('.//td[last()-1]//p//text()').extract()
            for name in filer_names:
                value = name

            description = row.xpath('.//td[last()-0]//text()').extract_first()
            regex = re.compile(r'\d{1,2}\/\d{1,2}\/\/?\d{1,4}')
            date = regex.findall(description)

            docket['docket_id'] = identifier.strip('').strip().strip(')')
            docket['filer'] = value.strip().strip(')')
            docket['description'] = description.strip()
            docket['date'] = date

            yield docket

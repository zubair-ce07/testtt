import re
import datetime

from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider


class JetsmartSpider(CrawlSpider):
    name = 'jetsmart'
    allowed_domains = ['www.jetsmart.com']
    start_urls = [
        'https://booking.jetsmart.com/Flight/InternalSelect?o1=SCL&d1=ANF&dd1=2018-7-27&ADT=1&CHD=0&inl=0&r=true&s=true&mon=true&cur=CLP&culture=es-CL&pc=&dd2=2018-8-8'
        # 'https://booking.jetsmart.com/Flight/InternalSelect?o1=SCL&d1=LIM&dd1=2018-7-28&ADT=1&CHD=0&inl=0&r=true&s=true&mon=true&cur=CLP&culture=es-CL&pc=&dd2=2018-8-5'
    ]

    def parse(self, response):
        tables = response.css('.table.avail-table').extract()
        for outbound in self.extract_data(response, tables[0]):
            for inbound in self.extract_data(response, tables[1]):
                item = {
                    'pos': 'CL',
                    'origin': self.extract_origin(response),
                    'destination': self.extract_destination(response),
                    'source': 'Jetsmart',
                    'site_source': 'Jetsmart',
                    'carrier': 'Jetsmart',
                    'outbound_flight_number': outbound[4],
                    'currency': self.extract_currency(response),
                    'price_outbound': self.extract_price_outbound(outbound),
                    'price_inbound': self.extract_price_inbound(inbound),
                    'OD': '{0}{1}'.format(self.extract_origin(response), self.extract_destination(response)),
                    'obsevation_time': datetime.datetime.now().time(),
                    'observation_date': datetime.datetime.now().date(),
                    'outbound_departure': outbound[0],
                    'outbound_arrival': outbound[1],
                    'inbound_departure': inbound[0],
                    'inbound_arrival': inbound[1],
                }
                yield item

    def extract_price_inbound(self, inbound):
        return inbound[5] if 'N/A' not in inbound[5] else inbound[6]

    def extract_price_outbound(self, outbound):
        return outbound[5] if 'N/A' not in outbound[5] else outbound[6]

    def extract_currency(self, response):
        return response.css("#currencyList option[selected]::text").extract_first()

    def extract_origin(self, response):
        return response.css('.price-display-stations-two li *::text').extract()[0]

    def extract_destination(self, response):
        return response.css('.price-display-stations-two li *::text').extract()[1]

    def extract_data(self, response, resp):
        resp = HtmlResponse(url=response.url, body=resp.encode('utf-8'))
        data = resp.css('table tbody tr *::text').extract()
        data = [single_row.strip() for single_row in data if
                         len(single_row.strip()) and 'restantes' not in single_row
                         and 'restante' not in single_row]
        return [data[single_row:single_row + 7] for single_row in range(0, len(data), 7)]

    def clean_spaces(self, string):
        return ' '.join(re.split("\s+", string, flags=re.UNICODE))

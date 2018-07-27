import re

import time
from datetime import datetime
from datetime import timedelta
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider


class JetsmartSpider(CrawlSpider):
    name = 'jetsmart'
    allowed_domains = ['www.jetsmart.com']
    #download_delay = 3
    MAX_DAYS = 120

    def __init__(self, *args, **kwargs):
        super(JetsmartSpider, self).__init__(*args, **kwargs)
        self.input_airports = [
            ("ANF", "SCL"),
            ("SCL", "ANF"),
            ("CJC", "SCL"),
            ("SCL", "CJC"),
            ("PUQ", "SCL"),
            ("SCL", "PUQ"),
            ("SCL", "PMC"),
            ("PMC", "SCL"),
        ]
        self.depart_dates = self.get_next_dates()
        self.date_pairs = self.get_next_date_pairs()

    def get_next_dates(self):
        now = datetime.now()
        dates = [(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, self.MAX_DAYS)]
        return dates

    def get_next_date_pairs(self):
        now = datetime.now()
        dates = [((now + timedelta(days=x)).strftime("%Y-%m-%d"), (now + timedelta(days=x + 7)).strftime("%Y-%m-%d"))
                 for x in range(0, self.MAX_DAYS)]
        return dates

    def start_requests(self):
        yield from self.search_twoway()
        yield from self.search_oneway()

    def search_twoway(self):
        for depart_date, arrive_date in self.date_pairs:
            for depart, arrival in self.input_airports:
                url = '{}{}{}{}{}{}{}{}'.format('https://booking.jetsmart.com/Flight/InternalSelect?o1=', depart,
                                                '&d1=', arrival, '&dd1=', depart_date,
                                                '&ADT=1&CHD=0&inl=0&r=true&s=true&mon=true&cur=CLP&culture=es-CL&pc=&dd2=',
                                                arrive_date)
                yield Request(url, callback=self.parse_twoway_trips)

    def search_oneway(self):
        for depart_date in self.depart_dates:
            for depart, arrival in self.input_airports:
                url = '{}{}{}{}{}{}{}'.format('https://booking.jetsmart.com/Flight/InternalSelect?o1=', depart,
                                              '&d1=', arrival, '&dd1=', depart_date,
                                              '&ADT=1&CHD=0&inl=0&r=false&s=true&mon=true&cur=CLP&culture=es-CL&pc=')
                yield Request(url, callback=self.parse_oneway_trips)

    def parse_twoway_trips(self, response):
        print(response.url)
        tables = response.css('.table.avail-table').extract()
        for outbound in self.extract_data(response, tables[0]):
            for inbound in self.extract_data(response, tables[1]):
                item = {
                    'POS': self.pos(),
                    'source': 'JA',
                    'carrier': 'JA',
                    'is_tax_inc_outin': '0',
                    'site_source': 'JA',
                    'inbound_arrival_time': inbound[1].split(u'\xa0')[0],
                    'inbound_departure_time': inbound[0].split(u'\xa0')[0],
                    'outbound_arrival_time': outbound[1].split(u'\xa0')[0],
                    'outbound_departure_time': outbound[0].split(u'\xa0')[0],
                    'inbound_arrival_date': self.extract_inbound_date(response),
                    'inbound_departure_date': self.extract_inbound_date(response),
                    'outbound_arrival_date': self.extract_outbound_date(response),
                    'outbound_departure_date': self.extract_outbound_date(response),
                    'outbound_bundle': self.extract_bound_bundle(outbound),
                    'inbound_bundle': self.extract_bound_bundle(inbound),
                    'outbound_flight_number': outbound[4],
                    'inbound_flight_number': inbound[4],
                    'origin': self.extract_origin(response),
                    'one_way_trip': 0,
                    'currency': self.extract_currency(response),
                    'obsevation_time': time.strftime("%H:%M"),
                    'price_inbound': self.extract_price(inbound),
                    'observation_date': time.strftime("%d-%b-%Y"),
                    'price_outbound': self.extract_price(outbound),
                    'destination': self.extract_destination(response),
                    'price_exclusive_tax': self.extract_price_exclusive_tax_two_way(inbound, outbound),
                    'price_inclusive_tax': self.extract_price_inclusive_tax(response),
                    'OD': '{0}{1}'.format(self.extract_origin(response), self.extract_destination(response)),
                    'tax': self.extract_tax_two_way(inbound, outbound, response)
                }
                yield item

    def parse_oneway_trips(self, response):
        tables = response.css('.table.avail-table').extract()
        for outbound in self.extract_data(response, tables[0]):
            item = {
                'POS': self.pos(),
                'source': 'JA',
                'carrier': 'JA',
                'is_tax_inc_outin': '0',
                'site_source': 'JA',
                'outbound_arrival_time': outbound[1].split(u'\xa0')[0],
                'outbound_departure_time': outbound[0].split(u'\xa0')[0],
                'outbound_arrival_date': self.extract_outbound_date(response),
                'outbound_departure_date': self.extract_outbound_date(response),
                'outbound_bundle': self.extract_bound_bundle(outbound),
                'outbound_flight_number': outbound[4],
                'origin': self.extract_origin(response),
                'one_way_trip': 1,
                'currency': self.extract_currency(response),
                'obsevation_time': time.strftime("%H:%M"),
                'observation_date': time.strftime("%d-%b-%Y"),
                'price_outbound': self.extract_price(outbound),
                'destination': self.extract_destination(response),
                'price_exclusive_tax': self.extract_price_exclusive_tax_one_way(outbound),
                'price_inclusive_tax': self.extract_price_inclusive_tax(response),
                'OD': '{0}{1}'.format(self.extract_origin(response), self.extract_destination(response)),
                'tax': self.extract_tax_one_way(outbound, response)
            }
            yield item

    def extract_bound_bundle(self, data):
        return 'Promo' if len(data) == 7 else 'Smart'

    def extract_tax_two_way(self, inbound, outbound, response):
        return self.extract_price_inclusive_tax(response) - self.extract_price_exclusive_tax_two_way(inbound, outbound)

    def extract_tax_one_way(self, outbound, response):
        return self.extract_price_inclusive_tax(response) - self.extract_price_exclusive_tax_one_way(outbound)

    def extract_outbound_date(self, response):
        return self.clean_spaces(
            response.css('.price-display-flight-info-number *::text').extract_first().strip()).replace(' ', '-')

    def extract_inbound_date(self, response):
        return self.clean_spaces(
            response.css('.price-display-flight-info-number *::text').extract()[1].strip()).replace(' ', '-')

    def pos(self):
        return 'CL'

    def fomat_rate(self, data):
        return data.replace('.', '').split('$ ')[1]

    def extract_price_exclusive_tax_one_way(self, outbound):
        return int(self.fomat_rate(outbound[6])) if len(outbound) == 7 else int(self.fomat_rate(outbound[5]))

    def extract_price_exclusive_tax_two_way(self, inbound, outbound):
        return int(self.fomat_rate(inbound[6])) + int(self.fomat_rate(outbound[6])) if len(inbound) == 7 else int(
            self.fomat_rate(inbound[5])) + int(self.fomat_rate(outbound[5]))

    def extract_price_inclusive_tax(self, response):
        price = response.css('.price-display-passenger-total *::text').extract()[3]
        return int(self.fomat_rate(self.clean_spaces(price)))

    def extract_price(self, inbound):
        return self.fomat_rate(inbound[5]) if 'N/A' not in inbound[5] else self.fomat_rate(inbound[6])

    def extract_currency(self, response):
        return response.css("#currencyList option[selected]::text").extract_first()

    def extract_origin(self, response):
        return response.css('.price-display-stations-two li *::text').extract()[0]

    def extract_destination(self, response):
        return response.css('.price-display-stations-two li *::text').extract()[1]

    def extract_data(self, response, resp):
        resp = HtmlResponse(url=response.url, body=resp.encode('utf-8'))
        head = self.clean_spaces(''.join(resp.css('thead tr *::text').extract()))
        data = resp.css('table tbody tr *::text').extract()
        data = [single_row.strip() for single_row in data if
                len(single_row.strip()) and 'restantes' not in single_row
                and 'restante' not in single_row]
        if 'Promo' in head:
            return [data[single_row:single_row + 7] for single_row in range(0, len(data), 7)]
        else:
            return [data[single_row:single_row + 6] for single_row in range(0, len(data), 6)]

    def clean_spaces(self, string):
        return ' '.join(re.split("\s+", string, flags=re.UNICODE))

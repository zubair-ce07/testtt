import re
import json
import itertools
from datetime import datetime, timedelta

import w3lib.url
from scrapy import Spider, Request, Selector

from ..items import Flight


class JetSmartParser(Spider):
    name = 'jetsmart-parse'

    ONEWAY_FLIGHT_TAX = '7.592'
    TWOWAY_FLIGHT_TAX = '15.184'
    POS = 'PK'
    SITE_SOURCE = 'JA'
    SOURCE = 'Jet Smart'
    CARRIER = 'JA'
    IS_TAX_INC_OUTIN = '0'

    price_re = re.compile('(\d+\.\d+)')
    minutes_re = re.compile('(\d+)m')
    hours_re = re.compile('(\d+)h')
    time_re = re.compile('(\d+:\d+)')
    time_format = '%Y-%m-%d %H:%M'

    default_inbound = [
        {
            'bundle': '',
            'departure_date': '',
            'travel_duration': '',
            'arrival_date': '',
            'flight_number': '',
            'price': ''
        }
    ]

    def parse(self, response):
        if self.flight_unavailable(response):
            return

        flight_common = Flight()

        flight_common['POS'] = self.POS
        flight_common['site_source'] = self.SITE_SOURCE
        flight_common['source'] = self.SOURCE
        flight_common['carrier'] = self.CARRIER
        flight_common['is_tax_inc_outin'] = self.IS_TAX_INC_OUTIN
        flight_common['outbound_travel_stopover'] = ''
        flight_common['inbound_travel_stopover'] = ''
        flight_common['outbound_fare_basis'] = ''
        flight_common['inbound_fare_basis'] = ''
        flight_common['outbound_booking_class'] = ''
        flight_common['inbound_booking_class'] = ''
        flight_common['currency'] = self.currency(response)
        flight_common['oneway_indicator'] = self.oneway_indicator(response)
        flight_common['observation_time'] = self.observation_time(response)
        flight_common['observation_date'] = self.observation_date(response)
        flight_common['origin'] = self.origin(response)
        flight_common['destination'] = self.destination(response)
        flight_common['OD'] = self.origin_destination(response)

        outbound_flights = self.outbound_flights(response)

        if self.is_oneway_flight(response):
            flight_common['tax'] = self.ONEWAY_FLIGHT_TAX
            inbound_flights = self.default_inbound
        else:
            flight_common['tax'] = self.TWOWAY_FLIGHT_TAX
            inbound_flights = self.inbound_flights(response)

        return self.available_trips(flight_common, outbound_flights, inbound_flights)

    def available_trips(self, flight_common, outbound_flights, inbound_flights):
        for outbound_flight, inbound_flight in itertools.product(outbound_flights, inbound_flights):
            flight = flight_common.copy()

            outbound_price = outbound_flight['price']
            flight['price_outbound'] = outbound_price
            flight['outbound_bundle'] = outbound_flight['bundle']
            flight['outbound_arrival_date'] = outbound_flight['arrival_date']
            flight['outbound_departure_date'] = outbound_flight['departure_date']
            flight['outbound_travel_duration'] = outbound_flight['travel_duration']
            flight['outbound_flight_number'] = outbound_flight['flight_number']

            inbound_price = inbound_flight['price']
            flight['price_inbound'] = inbound_price
            flight['inbound_bundle'] = inbound_flight['bundle']
            flight['inbound_arrival_date'] = inbound_flight['arrival_date']
            flight['inbound_departure_date'] = inbound_flight['departure_date']
            flight['inbound_travel_duration'] = inbound_flight['travel_duration']
            flight['inbound_flight_number'] = inbound_flight['flight_number']

            exl_tax_price = self.excluding_tax_price(outbound_price, inbound_price)
            flight['price_exc'] = exl_tax_price
            flight['price_inc'] = self.including_tax_price(exl_tax_price, flight_common['tax'])

            yield flight

    def outbound_flights(self, response):
        departure_date = self.outbound_departure_date(response)

        outbound_flight = {
            'bundle': self.outbound_bundle(response)
        }

        outbound_flights = []
        outbound_raw_flights = self.outbound_raw_flights(response)
        for outbound_raw_flight in outbound_raw_flights:
            outbound_flight.update(self.flight_details(outbound_raw_flight, departure_date))
            outbound_flights.append(outbound_flight)
        return outbound_flights

    def inbound_flights(self, response):
        departure_date = self.inbound_departure_date(response)

        inbound_flight = {
            'bundle': self.inbound_bundle(response)
        }

        inbound_flights = []
        inbound_raw_flights = self.inbound_raw_flights(response)
        for inbound_raw_flight in inbound_raw_flights:
            inbound_flight.update(self.flight_details(inbound_raw_flight, departure_date))
            inbound_flights.append(inbound_flight)
        return inbound_flights

    def flight_details(self, raw_flight, departure_date):
        selector = Selector(text=raw_flight)

        departure_date = self.departure_date_utc(departure_date, self.raw_departure_time(selector))
        travel_duration = self.travel_duration(selector)
        arrival_date = self.arrival_date_utc(departure_date, *self.duration_hours_minutes(travel_duration))

        flight_details = {
            'departure_date': departure_date,
            'travel_duration': travel_duration,
            'arrival_date': arrival_date,
            'flight_number': self.flight_number(selector),
            'price': self.price(selector)
        }
        return flight_details

    def excluding_tax_price(self, outbound_price, inbound_price):
        inbound_price = float(inbound_price) if inbound_price else 0
        outbound_price = float(outbound_price)
        return "{0:.3f}".format(outbound_price + inbound_price)

    def including_tax_price(self, exl_tax_price, tax):
        return "{0:.3f}".format(float(exl_tax_price) + float(tax))

    def departure_date_utc(self, departure_date, departure_time):
        parsed_date = datetime.strptime(f'{departure_date} {departure_time}', self.time_format)
        utc_adjusted_date = parsed_date - timedelta(hours=3)
        return utc_adjusted_date.strftime(self.time_format)

    def arrival_date_utc(self, departure_date_utc, hours, minutes):
        parsed_date = datetime.strptime(departure_date_utc, self.time_format)
        return (parsed_date + timedelta(hours=hours, minutes=minutes)).strftime(self.time_format)

    def duration_hours_minutes(self, travel_duration):
        minutes = self.minutes_re.findall(travel_duration)
        minutes = int(minutes[0]) if minutes else 0

        hours = self.hours_re.findall(travel_duration)
        hours = int(hours[0]) if hours else 0

        return hours, minutes

    def raw_departure_time(self, selector):
        departure_time_css = 'td:first-of-type ::text'
        raw_time = ''.join(selector.css(departure_time_css).extract())
        return self.time_re.findall(raw_time)[0]

    def travel_duration(self, selector):
        duration_css = 'td:nth-of-type(3) ::text'
        return ' '.join([td.strip() for td in selector.css(duration_css).extract()])

    def flight_number(self, selector):
        flight_number_css = 'td:nth-of-type(4) ::text'
        return ''.join(selector.css(flight_number_css).extract()).strip()

    def price(self, selector):
        price_css = 'td:last-of-type .mdl-radio ::text'
        price = ''.join(selector.css(price_css).extract())
        return self.price_re.findall(price)[0]

    def outbound_raw_flights(self, response):
        flight_rows_css = 'table:first-of-type tbody tr'
        return response.css(flight_rows_css).extract()

    def inbound_raw_flights(self, response):
        flight_rows_css = 'table:nth-of-type(2) tbody tr'
        return response.css(flight_rows_css).extract()

    def outbound_bundle(self, response):
        outbound_bundle_css = 'table:nth-of-type(1) th:last-of-type ::text'
        return response.css(outbound_bundle_css).extract_first()

    def inbound_bundle(self, response):
        inbound_bundle_css = 'table:nth-of-type(2) th:last-of-type ::text'
        return response.css(inbound_bundle_css).extract_first()

    def outbound_departure_date(self, response):
        url = response.meta['url']
        return w3lib.url.url_query_parameter(url, 'dd1')

    def inbound_departure_date(self, response):
        url = response.meta['url']
        return w3lib.url.url_query_parameter(url, 'dd2')

    def oneway_indicator(self, response):
        url = response.meta['url']
        if w3lib.url.url_query_parameter(url, 'r') == 'true':
            return '0'
        return '1'

    def origin(self, response):
        url = response.meta['url']
        return w3lib.url.url_query_parameter(url, 'o1')

    def destination(self, response):
        url = response.meta['url']
        return w3lib.url.url_query_parameter(url, 'd1')

    def currency(self, response):
        url = response.meta['url']
        return w3lib.url.url_query_parameter(url, 'cur')

    def observation_time(self, response):
        return datetime.utcnow().strftime('%H:%M')

    def observation_date(self, response):
        return datetime.utcnow().strftime('%Y-%m-%d')

    def origin_destination(self, response):
        return self.origin(response) + self.destination(response)

    def flight_unavailable(self, response):
        unavailability_css = '.avail-info-no-flights'
        return response.css(unavailability_css)

    def is_oneway_flight(self, response):
        if self.oneway_indicator(response) == '1':
            return True
        return False

class JetSmartCrawler(Spider):
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'DOWNLOAD_DELAY': 1
    }

    name = 'jetsmart-crawl'
    start_urls = ['https://jetsmart.com/cl/es']
    allowed_domains = ['jetsmart.com']

    route_url_t = 'https://jetsmart.com/api/TimeTable?fromStation={}&toStation={}'
    one_way_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}' \
                '&ADT=1&r=false&s=true&mon=true&cur=CLP'
    two_way_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}&' \
                'ADT=1&r=true&s=true&mon=true&cur=CLP&dd2={}'
    ymd_date = '%Y-%m-%d'
    dmy_date = '%d-%m-%Y'

    flight_routes = [
        ('ANF', 'SCL'),
        ('SCL', 'ANF'),
        ('CJC', 'SCL'),
        ('SCL', 'CJC'),
        ('PUQ', 'SCL'),
        ('SCL', 'PUQ'),
        ('SCL', 'PMC'),
        ('PMC', 'SCL')
    ]

    cookie_jar = 1
    item_parser = JetSmartParser()

    def parse(self, response):
        yield from self.route_requests()

    def parse_route(self, response):
        selectable_days = json.loads(response.text)['calendarSelectableDays']
        dates_to_crawl = self.dates_to_crawl()

        outbound_days = [date for date in dates_to_crawl if date.strftime(self.dmy_date) not in
                                selectable_days['firstJourneyScheduleInformation']['disabledDates']]
        inbound_days = [date for date in dates_to_crawl if date.strftime(self.dmy_date) not in
                                selectable_days['secondJourneyScheduleInformation']['disabledDates']]
        origin = selectable_days['origin']
        destination = selectable_days['destination']

        one_way_requests = self.one_way_requests(outbound_days, origin, destination)
        two_way_requests = self.two_way_requests(outbound_days, inbound_days, origin, destination)

        yield from one_way_requests + two_way_requests

    def parse_item(self, response):
        return self.item_parser.parse(response)

    def route_requests(self):
        return [Request(url=self.route_url_t.format(*flight_route), callback=self.parse_route)
                for flight_route in self.flight_routes]

    def one_way_requests(self, outbound_days, origin, destination):
        requests = []
        for day in outbound_days:
            url = self.one_way_t.format(origin, destination, day.strftime(self.ymd_date))
            requests.append(Request(url=url, callback=self.parse_item, meta={'url': url, 'cookiejar': self.cookie_jar}))
            self.cookie_jar += 1
        return requests

    def two_way_requests(self, outgoing_days, incoming_days, origin, destination):
        requests = []
        for outgoing_day, incoming_day in itertools.product(outgoing_days, incoming_days):
            if incoming_day <= outgoing_day:
                continue

            url = self.two_way_t.format(
                origin, destination, outgoing_day.strftime(self.ymd_date), incoming_day.strftime(self.ymd_date)
            )
            requests.append(Request(url=url, callback=self.parse_item, meta={'url': url, 'cookiejar': self.cookie_jar}))
            self.cookie_jar += 1
        return requests

    def dates_to_crawl(self):
        date = datetime.utcnow()
        return [(date + timedelta(days=d)) for d in range(31)]

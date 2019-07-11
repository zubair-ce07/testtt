import itertools
import json
from datetime import datetime, timedelta

import scrapy
import w3lib.url
from scrapy.item import Item
from scrapy.selector import Selector, SelectorList
from scrapy.spiders import Request, Spider


class Item(Item):
    observation_date = scrapy.Field()
    observation_time = scrapy.Field()
    POS = scrapy.Field()
    oneway_indicator = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    outbound_travel_stopover = scrapy.Field()
    outbound_travel_duration = scrapy.Field()
    inbound_travel_stopover = scrapy.Field()
    inbound_travel_duration = scrapy.Field()
    carrier = scrapy.Field()
    outbound_flight_number = scrapy.Field()
    inbound_flight_number = scrapy.Field()
    site_source = scrapy.Field()
    source = scrapy.Field()
    outbound_departure_date = scrapy.Field()
    outbound_arrival_date = scrapy.Field()
    inbound_arrival_date = scrapy.Field()
    inbound_departure_date = scrapy.Field()
    outbound_fare_basis = scrapy.Field()
    inbound_fare_basis = scrapy.Field()
    outbound_booking_class = scrapy.Field()
    inbound_booking_class = scrapy.Field()
    outbound_bundle = scrapy.Field()
    inbound_bundle = scrapy.Field()
    tax = scrapy.Field()
    currency = scrapy.Field()
    price_outbound = scrapy.Field()
    price_inbound = scrapy.Field()
    is_tax_inc_outin = scrapy.Field()
    OD = scrapy.Field()


class JetSmartParser(Spider):
    name = 'jetsmart-parser'

    POS = 'PK'
    SITE_SOURCE = 'JA'
    SOURCE = 'Jet Smart'
    IS_TAX_INC_OUTIN = '0'
    CARRIER = 'JA'

    default_incoming_flights = [
        {
            'arrival_date': '',
            'departure_date': '',
            'travel_duration': '',
            'flight_number': '',
            'bundle': '',
            'inbound': ''
        }
    ]

    ONE_WAY_FLIGHT_TAX = '7.592'
    TWO_WAY_FLIGHT_TAX = '15.184'

    OUTBOUND_TRAVEL_STOPOVER = ''
    INBOUND_TRAVEL_STOPOVER = ''

    OUTBOUND_FARE_BASIS = ''
    INBOUND_FARE_BASIS = ''

    OUTBOUND_BOOKING_CLASS = ''
    INBOUND_BOOKING_CLASS = ''

    def parse(self, response):
        common_item = Item()
        common_item['POS'] = self.extract_pos(response)
        common_item['observation_date'] = self.extract_observation_date(response)
        common_item['observation_time'] = self.extract_observation_time(response)
        common_item['site_source'] = self.extract_site_source(response)
        common_item['source'] = self.extract_source(response)
        common_item['carrier'] = self.extract_carrier(response)
        common_item['is_tax_inc_outin'] = self.extract_is_tax_inc_outin(response)
        common_item['origin'] = self.extract_origin(response)
        common_item['destination'] = self.extract_destination(response)
        common_item['OD'] = self.extract_origin_destination(response)
        common_item['oneway_indicator'] = self.extract_oneway_indicator(response)
        common_item['currency'] = self.extract_currency(response)
        common_item['outbound_travel_stopover'] = self.extract_outbound_travel_stopover(response)
        common_item['inbound_travel_stopover'] = self.extract_inbound_travel_stopover(response)
        common_item['outbound_fare_basis'] = self.extract_outbound_fare_basis(response)
        common_item['inbound_fare_basis'] = self.extract_inbound_fare_basis(response)
        common_item['outbound_booking_class'] = self.extract_outbound_booking_class(response)
        common_item['inbound_booking_class'] = self.extract_inbound_booking_class(response)
        common_item['tax'] = self.extract_flight_tax(response)

        incoming_flights = self.extract_incoming_flights(response)
        outgoing_flights = self.extract_outgoing_flights(response)

        return self.extract_flight_trips(incoming_flights, outgoing_flights, common_item)

    def extract_flight_trips(self, incoming_flights, outgoing_flights, common_item):
        for outgoing_flight, incoming_flight in itertools.product(outgoing_flights, incoming_flights):
            item = common_item.copy()

            item['outbound_bundle'] = outgoing_flight['bundle']
            item['price_outbound'] = outgoing_flight['price']
            item['outbound_travel_duration'] = outgoing_flight['travel_duration']
            item['outbound_flight_number'] = outgoing_flight['flight_number']
            item['outbound_arrival_date'] = outgoing_flight['arrival_date']
            item['outbound_departure_date'] = outgoing_flight['departure_date']

            item['price_inbound'] = incoming_flight['price']
            item['inbound_departure_date'] = incoming_flight['departure_date']
            item['inbound_bundle'] = incoming_flight['bundle']
            item['inbound_travel_duration'] = incoming_flight['travel_duration']
            item['inbound_flight_number'] = incoming_flight['flight_number']
            item['inbound_arrival_date'] = incoming_flight['arrival_date']

            yield item

    def extract_observation_time(self, response):
        return datetime.utcnow().strftime('%H:%M')

    def extract_observation_date(self, response):
        return datetime.utcnow().strftime('%Y-%m-%d')

    def extract_pos(self, response):
        return self.POS

    def extract_site_source(self, response):
        return self.SITE_SOURCE

    def extract_source(self, response):
        return self.SOURCE

    def extract_carrier(self, response):
        return self.CARRIER

    def extract_is_tax_inc_outin(self, response):
        return self.IS_TAX_INC_OUTIN

    def extract_outbound_travel_stopover(self, response):
        return self.OUTBOUND_TRAVEL_STOPOVER

    def extract_inbound_travel_stopover(self, response):
        return self.INBOUND_TRAVEL_STOPOVER

    def extract_outbound_fare_basis(self, response):
        return self.OUTBOUND_FARE_BASIS

    def extract_inbound_fare_basis(self, response):
        return self.INBOUND_FARE_BASIS

    def extract_outbound_booking_class(self, response):
        return self.OUTBOUND_BOOKING_CLASS

    def extract_inbound_booking_class(self, response):
        return self.INBOUND_BOOKING_CLASS

    def extract_flight_tax(self, response):
        if self.is_oneway_flight(response):
            return self.ONE_WAY_FLIGHT_TAX

        return self.TWO_WAY_FLIGHT_TAX

    def extract_travel_duration(self, raw_outgoing_flight):
        departure_time = clean(raw_outgoing_flight.css('flight-fee ::attr(departure-time)'))[0]
        arrival_time = clean(raw_outgoing_flight.css('flight-fee ::attr(arrival-time)'))[0]
        time_format = '%H:%M'

        return datetime.strptime(arrival_time, time_format) - datetime.strptime(departure_time, time_format)

    def extract_price(self, raw_outgoing_flight):
        return clean(raw_outgoing_flight.css('flight-fee ::attr(discounted-price)'))[0]

    def extract_flight_number(self, raw_outgoing_flight):
        return clean(raw_outgoing_flight.css('flight-fee ::attr(flight-number)'))[0]

    def extract_outgoing_departure_date(self, response):
        return w3lib.url.url_query_parameter(response.meta['url'], 'dd1')

    def extract_incoming_departure_date(self, response):
        return w3lib.url.url_query_parameter(response.meta['url'], 'dd2')

    def extract_oneway_indicator(self, response):
        if w3lib.url.url_query_parameter(response.meta['url'], 'r') == 'true':
            return '0'

        return '1'

    def is_oneway_flight(self, response):
        if self.extract_oneway_indicator(response) == '1':
            return True

        return False

    def extract_origin(self, response):
        return w3lib.url.url_query_parameter(response.meta['url'], 'o1')

    def extract_destination(self, response):
        return w3lib.url.url_query_parameter(response.meta['url'], 'd1')

    def extract_origin_destination(self, response):
        return self.extract_origin(response) + self.extract_destination(response)

    def extract_arrival_date(self, raw_outgoing_flight):
        raw_arrival_date = clean(raw_outgoing_flight.css('flight-fee ::attr(arrival-date)'))
        return raw_arrival_date[0] if raw_arrival_date else ''

    def extract_bundle(self, raw_outgoing_flight):
        return clean(raw_outgoing_flight.css('flight-fee ::attr(departure-station)'))[0]

    def extract_currency(self, response):
        return w3lib.url.url_query_parameter(response.meta['url'], 'cur')

    def extract_incoming_flights(self, response):
        if self.is_oneway_flight(response):
            return self.default_incoming_flights

        departure_date = self.extract_incoming_departure_date(response)
        raw_incoming_flights = clean(response.css('.fee-selector li:nth-of-type(2)'))
        incoming_flights = []

        for raw_incoming_flight in raw_incoming_flights:
            incoming_flights.append(self.extract_flight_details(raw_incoming_flight, departure_date))

        return incoming_flights

    def extract_outgoing_flights(self, response):
        departure_date = self.extract_outgoing_departure_date(response)
        raw_outgoing_flights = clean(response.css('.fee-selector li'))
        outgoing_flights = []

        for raw_outgoing_flight in raw_outgoing_flights:
            outgoing_flights.append(self.extract_flight_details(raw_outgoing_flight, departure_date))

        return outgoing_flights

    def extract_flight_details(self, raw_flight, departure_date):
        raw_outgoing_flight = Selector(text=raw_flight)

        flight_details = {
            'travel_duration': self.extract_travel_duration(raw_outgoing_flight),
            'arrival_date': self.extract_arrival_date(raw_outgoing_flight),
            'departure_date': departure_date,
            'flight_number': self.extract_flight_number(raw_outgoing_flight),
            'price': self.extract_price(raw_outgoing_flight),
            'bundle': self.extract_bundle(raw_outgoing_flight)
        }

        return flight_details


def clean(raw_item):
    if isinstance(raw_item, str):
        return raw_item.strip()
    elif isinstance(raw_item, SelectorList):
        return [r.strip() for r in raw_item.getall() if r.strip()]

    return [r.strip() for r in raw_item if r.strip()]


class JetSmartCrawler(Spider):
    name = 'jetsmart-crawler'
    start_urls = ['https://jetsmart.com/cl/es']
    allowed_domains = ['jetsmart.com']

    flight_route_url_t = 'https://jetsmart.com/api/TimeTable?fromStation={}&toStation={}'
    one_way_flight_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}' \
                       '&ADT=1&r=false&s=true&mon=true&cur=CLP'
    two_way_flight_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}&' \
                       'ADT=1&r=true&s=true&mon=true&cur=CLP&dd2={}'

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

    date_month_year_t = '%d-%m-%Y'
    year_month_date_t = '%Y-%m-%d'

    parser = JetSmartParser()

    def parse(self, response):
        yield from [Request(url=self.flight_route_url_t.format(*flight_route),
                            callback=self.parse_flight_route) for flight_route in self.flight_routes]

    def parse_flight_route(self, response):
        selectable_days = json.loads(response.text)['calendarSelectableDays']
        days_to_crawl = self.days_to_crawl()

        outgoing_flight_days = [date for date in days_to_crawl
                                if date.strftime(self.date_month_year_t) not in
                                selectable_days['firstJourneyScheduleInformation']['disabledDates']]

        incoming_fight_days = [date for date in days_to_crawl
                               if date.strftime(self.date_month_year_t) not in
                               selectable_days['secondJourneyScheduleInformation']['disabledDates']]

        origin = selectable_days['origin']
        destination = selectable_days['destination']

        one_way_requests = self.construct_one_way_requests(outgoing_flight_days, origin, destination)
        two_way_requests = self.construct_two_way_requests(incoming_fight_days, outgoing_flight_days,
                                                           origin, destination)

        yield from one_way_requests + two_way_requests

    def days_to_crawl(self):
        date = datetime.utcnow()
        return [(date + timedelta(days=d)) for d in range(31)]

    def construct_one_way_requests(self, outgoing_flight_days, origin, destination):
        one_way_requests = []

        for day in outgoing_flight_days:
            url = self.one_way_flight_t.format(origin, destination, day.strftime(self.year_month_date_t))
            one_way_requests.append(Request(url=url, callback=self.parser.parse, meta={'url': url}, dont_filter=True))

        return one_way_requests

    def construct_two_way_requests(self, incoming_fight_days, outgoing_flight_days, origin, destination):
        two_way_requests = []

        for out_day, in_day in itertools.product(outgoing_flight_days, incoming_fight_days):
            if in_day <= out_day:
                continue

            url = self.two_way_flight_t.format(origin, destination, out_day.strftime(self.year_month_date_t),
                                               in_day.strftime(self.year_month_date_t))
            two_way_requests.append(Request(url=url, callback=self.parser.parse, meta={'url': url}, dont_filter=True))

        return two_way_requests

import re
import json
import itertools
from datetime import datetime, timedelta

import w3lib.url
from scrapy import Spider, Request, Selector

from ..items import Item


class JetSmartParser(Spider):
    name = 'jetsmart-parse'

    solo_flight_tax = '7.592'
    return_flight_tax = '15.184'
    pos = 'PK'
    site_source = 'JA'
    source = 'Jet Smart'
    carrier = 'JA'
    is_tax_inc_outin = '0'

    price_re = re.compile('(\d+\.\d+)')
    minutes_re = re.compile('(\d+)m')
    hours_re = re.compile('(\d+)h')
    time_re = re.compile('(\d+:\d+)')

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

        item = Item()

        item['POS'] = self.pos
        item['site_source'] = self.site_source
        item['source'] = self.source
        item['carrier'] = self.carrier
        item['is_tax_inc_outin'] = self.is_tax_inc_outin
        item['outbound_travel_stopover'] = ''
        item['inbound_travel_stopover'] = ''
        item['outbound_fare_basis'] = ''
        item['inbound_fare_basis'] = ''
        item['outbound_booking_class'] = ''
        item['inbound_booking_class'] = ''
        item['currency'] = self.currency(response)
        item['oneway_indicator'] = self.oneway_indicator(response)
        item['observation_time'] = self.observation_time(response)
        item['observation_date'] = self.observation_date(response)
        item['origin'] = self.origin(response)
        item['destination'] = self.destination(response)
        item['OD'] = self.origin_destination(response)

        outbound_options = self.outbound_options(response)

        if item['oneway_indicator'] == '1':
            item['tax'] = self.solo_flight_tax
            inbound_options = self.default_inbound
        else:
            item['tax'] = self.return_flight_tax
            inbound_options = self.inbound_options(response)

        return self.flight_options(item, outbound_options, inbound_options)

    def flight_options(self, item, outbound_options, inbound_options):
        for outbound_option, inbound_option in itertools.product(outbound_options, inbound_options):
            item_copy = item.copy()

            outbound_price = outbound_option['price']
            item_copy['price_outbound'] = outbound_price
            item_copy['outbound_bundle'] = outbound_option['bundle']
            item_copy['outbound_arrival_date'] = outbound_option['arrival_date']
            item_copy['outbound_departure_date'] = outbound_option['departure_date']
            item_copy['outbound_travel_duration'] = outbound_option['travel_duration']
            item_copy['outbound_flight_number'] = outbound_option['flight_number']

            inbound_price = inbound_option['price']
            item_copy['price_inbound'] = inbound_price
            item_copy['inbound_bundle'] = inbound_option['bundle']
            item_copy['inbound_arrival_date'] = inbound_option['arrival_date']
            item_copy['inbound_departure_date'] = inbound_option['departure_date']
            item_copy['inbound_travel_duration'] = inbound_option['travel_duration']
            item_copy['inbound_flight_number'] = inbound_option['flight_number']

            exl_tax_price = self.excluding_tax_price(outbound_price, inbound_price)
            item_copy['price_exc'] = exl_tax_price
            item_copy['price_inc'] = self.including_tax_price(exl_tax_price, item['tax'])

            yield item_copy

    def outbound_options(self, response):
        departure_date = self.outbound_departure_date(response)

        outbound_option_common = {
            'bundle': self.outbound_bundle(response)
        }

        outbound_options = []
        outbound_raw_options = self.outbound_raw_options(response)
        for outbound_raw_option in outbound_raw_options:
            outbound_option = outbound_option_common.copy()
            outbound_option.update(self.flight_option(outbound_raw_option, departure_date))
            outbound_options.append(outbound_option)
        return outbound_options

    def inbound_options(self, response):
        departure_date = self.inbound_departure_date(response)

        inbound_option_common = {
            'bundle': self.inbound_bundle(response)
        }

        inbound_options = []
        inbound_raw_options = self.inbound_raw_options(response)
        for inbound_raw_option in inbound_raw_options:
            inbound_option = inbound_option_common.copy()
            inbound_option.update(self.flight_option(inbound_raw_option, departure_date))
            inbound_options.append(inbound_option)
        return inbound_options

    def flight_option(self, raw_option, departure_date):
        selector = Selector(text=raw_option)

        departure_date = self.departure_date_utc(departure_date, self.raw_departure_time(selector))
        travel_duration = self.travel_duration(selector)
        arrival_date = self.arrival_date_utc(departure_date, *self.duration_hours_minutes(travel_duration))

        option_details = {
            'departure_date': departure_date,
            'travel_duration': travel_duration,
            'arrival_date': arrival_date,
            'flight_number': self.flight_number(selector),
            'price': self.price(selector)
        }
        return option_details

    def excluding_tax_price(self, outbound_price, inbound_price):
        inbound_price = float(inbound_price) if inbound_price else 0
        outbound_price = float(outbound_price)
        return "{0:.3f}".format(outbound_price + inbound_price)

    def including_tax_price(self, exl_tax_price, tax):
        return "{0:.3f}".format(float(exl_tax_price) + float(tax))

    def departure_date_utc(self, departure_date, departure_time):
        parsed_date = datetime.strptime(f'{departure_date} {departure_time}', '%Y-%m-%d %H:%M')
        utc_adjusted_date = parsed_date - timedelta(hours=3)
        return utc_adjusted_date.strftime('%Y-%m-%d %H:%M')

    def arrival_date_utc(self, departure_date_utc, hours, minutes):
        parsed_date = datetime.strptime(departure_date_utc, '%Y-%m-%d %H:%M')
        return (parsed_date + timedelta(hours=hours, minutes=minutes)).strftime('%Y-%m-%d %H:%M')

    def duration_hours_minutes(self, travel_duration):
        minutes = self.minutes_re.findall(travel_duration)
        minutes = int(minutes[0]) if minutes else 0

        hours = self.hours_re.findall(travel_duration)
        hours = int(hours[0]) if hours else 0

        return hours, minutes

    def raw_departure_time(self, selector):
        departure_time_css = 'td:first-of-type ::text'
        raw_time = ''.join(selector.css(departure_time_css).extract()).strip()
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

    def outbound_raw_options(self, response):
        options_rows_css = 'table:first-of-type tbody tr'
        return response.css(options_rows_css).extract()

    def inbound_raw_options(self, response):
        options_rows_css = 'table:nth-of-type(2) tbody tr'
        return response.css(options_rows_css).extract()

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

class JetSmartCrawler(Spider):
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    #    'DOWNLOAD_DELAY': 1
    }

    name = 'jetsmart-crawl'
    start_urls = ['https://jetsmart.com/cl/es']
    allowed_domains = ['jetsmart.com']

    calendar_url_t = 'https://jetsmart.com/api/TimeTable?fromStation={}&toStation={}'
    one_way_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}' \
                '&ADT=1&r=false&s=true&mon=true&cur=CLP'
    two_way_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1={}&d1={}&dd1={}&' \
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

    cookie_jar = 1
    item_parser = JetSmartParser()

    def parse(self, response):
        yield from self.flight_requests()

    def parse_flights(self, response):
        selectable_days = json.loads(response.text)['calendarSelectableDays']
        dates_to_crawl = self.dates_to_crawl()

        outbound_days = [date for date in dates_to_crawl if date.strftime('%d-%m-%Y') not in
                                selectable_days['firstJourneyScheduleInformation']['disabledDates']]
        inbound_days = [date for date in dates_to_crawl if date.strftime('%d-%m-%Y') not in
                                selectable_days['secondJourneyScheduleInformation']['disabledDates']]
        origin = w3lib.url.url_query_parameter(response.url, 'fromStation')
        destination = w3lib.url.url_query_parameter(response.url, 'toStation')

        one_way_requests = self.one_way_requests(outbound_days, origin, destination)
        two_way_requests = self.two_way_requests(outbound_days, inbound_days, origin, destination)

        yield from one_way_requests + two_way_requests

    def parse_item(self, response):
        return self.item_parser.parse(response)

    def flight_requests(self):
        return [Request(url=self.calendar_url_t.format(*flight_route), callback=self.parse_flights)
                for flight_route in self.flight_routes]

    def one_way_requests(self, flight_days, origin, destination):
        requests = []
        for day in flight_days:
            url = self.one_way_t.format(origin, destination, day.strftime('%Y-%m-%d'))
            requests.append(Request(url=url, callback=self.parse_item, meta={'url': url, 'cookiejar': self.cookie_jar}))
            self.cookie_jar += 1
        return requests

    def two_way_requests(self, outgoing_days, incoming_days, origin, destination):
        requests = []
        for outgoing_day, incoming_day in itertools.product(outgoing_days, incoming_days):
            url = self.two_way_t.format(
                origin, destination, outgoing_day.strftime('%Y-%m-%d'), incoming_day.strftime('%Y-%m-%d')
            )

            if incoming_day <= outgoing_day:
                continue

            requests.append(Request(url=url, callback=self.parse_item, meta={'url': url, 'cookiejar': self.cookie_jar}))
            self.cookie_jar += 1

        return requests

    def dates_to_crawl(self):
        date = datetime.utcnow()
        return [(date + timedelta(days=n)) for n in range(1, 31)]

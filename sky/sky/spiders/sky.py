import json
from datetime import datetime, timedelta

import scrapy
from scrapy import FormRequest

from sky.items import SkyItem


class SkySpider(scrapy.Spider):
    name = "sky"
    MAX_DAYS = 14
    api_url = "https://www.skyairline.com/Availability/Post"

    def __init__(self, *args, **kwargs):
        super(SkySpider, self).__init__(*args, **kwargs)

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
        yield from self.search_oneway()
        yield from self.search_twoway()

    def search_oneway(self):
        for depart_date in self.depart_dates:
            for depart, arrival in self.input_airports:
                depature_date = datetime.strptime(depart_date, "%Y-%m-%d").date()
                returnDateString = str(depature_date + timedelta(days=3))
                startDateStringOutbound = str(depature_date - timedelta(days=3))
                form_data = {"interline": 'false', "fromCityCode": [depart], "toCityCode": [arrival],
                             "departureDate": depart_date, "departureDateString": [depart_date],
                             "returnDateString": returnDateString, "startDateStringOutbound": [startDateStringOutbound],
                             "endDateStringOutbound": [returnDateString],
                             "startDateStringInbound": str(datetime.now().date()),
                             "endDateStringInbound": str(datetime.now().date()), "adults": '1', "children": '0',
                             "infants": '0', "pets": '0',
                             "roundTrip": 'false', "useFlexDates": 'false', "isOutbound": 'true', "filterMethod": '102',
                             "promocode": "", "currency": "USD", "useRealCacheKey": 'false', "regularSearch": 'false',
                             "taLogin": "", "taPin": "", "iataNumber": "", "apiKey": "", "fareTypeCategory": '1',
                             "languageCode": "en-US", "securityToken": "", "isMobileSearch": 'false'}
                yield FormRequest(url=self.api_url, formdata=form_data, callback=self.parse_oneway_routes)

    def search_twoway(self):
        for depart_date, arrive_date in self.date_pairs:
            for depart, arrival in self.input_airports:
                depature_date = datetime.strptime(arrive_date, "%Y-%m-%d").date()
                returnDateString = str(depature_date + timedelta(days=3))
                arrival_date = datetime.strptime(depart_date, "%Y-%m-%d").date()
                departureDateString = str(arrival_date + timedelta(days=3))

                form_data = {"interline": 'false', "fromCityCode": [arrival, depart], "toCityCode": [depart, arrival],
                             "departureDate": arrive_date, "departureDateString": [arrive_date],
                             "returnDateString": returnDateString,
                             "startDateStringOutbound": [departureDateString, depart_date],
                             "endDateStringOutbound": [returnDateString, depart_date],
                             "startDateStringInbound": str(datetime.now().date()),
                             "endDateStringInbound": str(datetime.now().date()), "adults": '1', "children": '0',
                             "infants": '0',
                             "pets": '0',
                             "roundTrip": 'true', "useFlexDates": 'false', "isOutbound": 'false', "filterMethod": '102',
                             "promocode": "", "currency": "USD", "useRealCacheKey": 'false', "regularSearch": 'false',
                             "taLogin": "", "taPin": "", "iataNumber": "", "apiKey": "", "fareTypeCategory": '1',
                             "languageCode": "en-US", "securityToken": "", "isMobileSearch": 'false'}
                yield FormRequest(url=self.api_url, formdata=form_data, callback=self.parse_twoway_routes)

    def parse_oneway_routes(self, response):
        data = json.loads(response.text)
        for outbound_segment in data['Availability']['Routes'][0]['Segments']:
            for outbound_fare_type in outbound_segment['FaresTypes']:
                item = SkyItem()
                item['observation_date'] = str(datetime.now().date())
                item['observation_time'] = str(datetime.time(datetime.now()))
                item['outbound_Bundle'] = outbound_fare_type['Name']
                item['origin'] = outbound_segment['Origin']['Code']
                item['destination'] = outbound_segment['Destination']['Code']
                item['OD'] = f"{item['origin']}{item['destination']}"
                item['OneWayIndicator'] = False
                item['price_outbound'] = outbound_fare_type['Fares'][0]['AmountIncludingTax']
                item['OutboundFareBasis'] = outbound_fare_type['Fares'][0]['FareBasis']
                item['outbound_booking_class'] = item['OutboundFareBasis'][0][0]
                item['carrier'] = outbound_segment['Carrier']['Code']
                item['OutboundFlightNumber'] = outbound_segment['FlightNumber']
                item['outbound_departure_date'] = f'{outbound_segment["DepartureDateString"]} ' \
                                                  f'{outbound_segment["DepartureTimeString"]}'
                item['outbound_arrival_date'] = f"{outbound_segment['ArrivalDateString']} " \
                                                f"{outbound_segment['ArrivalTimeString']}"
                item['price_inc'] = float(item['price_outbound'])
                item['price_exc'] = float(outbound_fare_type['Fares'][0]['Amount'])
                item['Tax'] = outbound_fare_type['Fares'][0]['Taxes'][0]['Amount']
                item['currency'] = outbound_fare_type['Fares'][0]['Currency']
                item['is_tax_inc_outin'] = True
                yield item.copy()

    def parse_twoway_routes(self, response):
        data = json.loads(response.text)
        for outbound_segment in data['Availability']['Routes'][1]['Segments']:
            for outbound_fare_type in outbound_segment['FaresTypes']:
                item = SkyItem()
                item['observation_date'] = str(datetime.now().date())
                item['observation_time'] = str(datetime.time(datetime.now()))
                item['outbound_Bundle'] = outbound_fare_type['Name']
                item['origin'] = outbound_segment['Origin']['Code']
                item['destination'] = outbound_segment['Destination']['Code']
                item['OD'] = f"{item['origin']}{item['destination']}"
                item['OneWayIndicator'] = False
                item['price_outbound'] = outbound_fare_type['Fares'][0]['AmountIncludingTax']
                item['OutboundFareBasis'] = outbound_fare_type['Fares'][0]['FareBasis']
                item['outbound_booking_class'] = item['OutboundFareBasis'][0][0]
                item['carrier'] = outbound_segment['Carrier']['Code']
                item['OutboundFlightNumber'] = outbound_segment['FlightNumber']
                item['outbound_departure_date'] = f'{outbound_segment["DepartureDateString"]} ' \
                                                  f'{outbound_segment["DepartureTimeString"]}'
                item['outbound_arrival_date'] = f"{outbound_segment['ArrivalDateString']} " \
                                                f"{outbound_segment['ArrivalTimeString']}"
                for inbound_segment in data['Availability']['Routes'][0]['Segments']:
                    for inbound_fare_type in inbound_segment['FaresTypes']:
                        item['inbound_bundle'] = inbound_fare_type['Name']
                        item['price_inbound'] = inbound_fare_type['Fares'][0]['AmountIncludingTax']
                        item['InboundFareBasis'] = inbound_fare_type['Fares'][0]['FareBasis']
                        item['inbound_booking_class'] = item['InboundFareBasis'][0][0]
                        item['inbound_departure_date'] = f'{inbound_segment["DepartureDateString"]} ' \
                                                         f'{inbound_segment["DepartureTimeString"]}'
                        item['inbound_arrival_date'] = f"{inbound_segment['ArrivalDateString']} " \
                                                       f"{inbound_segment['ArrivalTimeString']}"
                        item['InboundFlightNumber'] = inbound_segment['FlightNumber']
                        item['price_inc'] = float(item['price_outbound']) + float(item['price_inbound'])
                        item['price_exc'] = float(outbound_fare_type['Fares'][0]['Amount']) + float(
                            inbound_fare_type['Fares'][0]['Amount'])
                        item['Tax'] = inbound_fare_type['Fares'][0]['Taxes'][0]['Amount']
                        item['currency'] = outbound_fare_type['Fares'][0]['Currency']
                        item['is_tax_inc_outin'] = True
                        yield item.copy()

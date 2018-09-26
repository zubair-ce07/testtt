from datetime import datetime, timedelta
from w3lib.url import add_or_replace_parameter
from itertools import product
from re import findall, compile

from scrapy.spiders import CrawlSpider
from scrapy import Request

from ..items import Product


class JetSmart(CrawlSpider):
    name = 'jetsmart'

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = ['jetsmart.com']

    trip_url_t = 'https://booking.jetsmart.com/Flight/InternalSelect?o1=SCL&d1=ANF&' \
                 'dd1=2018-9-26&ADT=1&CHD=0&inl=0&r=false&s=true&mon=true&cur=CLP&culture=es-CL&pc='

    routes = [("ANF", "SCL"),
              ("SCL", "ANF"),
              ("CJC", "SCL"),
              ("SCL", "CJC"),
              ("PUQ", "SCL"),
              ("SCL", "PUQ"),
              ("SCL", "PMC"),
              ("PMC", "SCL")]

    price_re = compile('\$\s*(\d[\d\.\,]*)')
    date_time_re = compile('\s*(\d[\d\-\:]*)')

    organization_code = 'JA'
    source_name = 'Jet Smart'
    point_of_sale = 'PK'
    pricing_bundle = 'Tarifa Smart'

    def start_requests(self):
        for route, date in product(self.routes, self.extract_dates()):
            url = self.common_url(route, date)

            yield self.oneway_trip_request(url, route)
            yield self.round_trip_request(url, route, date)

    def common_url(self, route, date):
        url = add_or_replace_parameter(self.trip_url_t, 'dd1', date.strftime('%Y-%m-%d'))
        url = add_or_replace_parameter(url, 'o1', route[0])
        return add_or_replace_parameter(url, 'd1', route[1])

    def extract_dates(self):
        return [datetime.today() + timedelta(days=x) for x in range(1, 31)]

    def oneway_trip_request(self, url, route):
        meta = {'route': route, 'oneway_indicator': True}
        return Request(url, callback=self.parse_product, meta=meta, dont_filter=True)

    def round_trip_request(self, url, route, date):
        url = add_or_replace_parameter(url, 'dd2', date.strftime('%Y-%m-%d'))
        url = add_or_replace_parameter(url, 'r', 'true')

        meta = {'route': route, 'oneway_indicator': False}

        return Request(url, callback=self.parse_product, meta=meta, dont_filter=True)

    def common_product(self):
        product = Product()

        product['carrier'] = self.organization_code
        product['site_source'] = self.organization_code
        product['POS'] = self.point_of_sale
        product['source'] = self.source_name
        product['outbound_bundle'] = self.pricing_bundle
        product['inbound_bundle'] = self.pricing_bundle
        product['outbound_booking_class'] = ''
        product['inbound_booking_class'] = ''
        product['outbound_travel_stopover'] = ''
        product['inbound_travel_stopover'] = ''
        product['inbound_fare_basis'] = ''
        product['outbound_fare_basis'] = ''
        product['is_tax_inc_outin'] = 1

        return product

    def parse_product(self, response):
        product = self.common_product()

        product['OD'] = self.extract_od(response)
        product['tax'] = self.extract_tax(response)
        product['origin'] = self.extract_origin(response)
        product['destination'] = self.extract_destination(response)
        product['observation_date'] = self.extract_observation_date()
        product['observation_time'] = self.extract_observation_time()
        product['oneway_indicator'] = self.extract_oneway_indicator(response)
        product['price_exc'] = self.extract_pricing_without_tax(response)
        product['price_inc'] = self.extract_pricing_with_tax(response)
        product['currency'] = self.extract_currency(response)

        return self.extract_inbound_outbound_fields(response, product)

    def extract_inbound_outbound_fields(self, response, product):
        css_t = '.avail-table  [name="availability.MarketFareKeys[{}]"]'

        if not response.css(css_t.format(0)):
            return product

        for product in self.extract_outbound_fields(response, product):

            if response.css(css_t.format(1)) and not response.meta['oneway_indicator']:
                for product in self.extract_inbound_fields(response, product):
                    yield product
            else:
                yield product

    def extract_outbound_fields(self, response, product):
        outbound_sel = response.css('.avail-table')[0]
        for sel in outbound_sel.css('tbody tr'):
            product['outbound_flight_number'] = self.extract_flightno(sel)
            product['price_outbound'] = self.extract_outbound_price(sel)
            product['outbound_travel_duration'] = self.extract_duration(sel)
            product['outbound_departure_date'] = self.extract_outbound_date(sel, response,
                                                                            product['origin'])
            product['outbound_arrival_date'] = self.extract_outbound_date(sel, response,
                                                                          product['destination'])

            yield product

    def extract_inbound_fields(self, response, product):
        inbound_sel = response.css('.avail-table')[1]
        for sel in inbound_sel.css('tbody tr'):
            product['inbound_flight_number'] = self.extract_flightno(sel)
            product['price_inbound'] = self.extract_inbound_price(sel)
            product['inbound_travel_duration'] = self.extract_duration(sel)
            product['inbound_departure_date'] = self.extract_inbound_date(sel, response,
                                                                          product['destination'])
            product['inbound_arrival_date'] = self.extract_inbound_date(sel, response, product['origin'])

            yield product

    def extract_pricing_without_tax(self, response):
        pricing = self.extract_pricing_with_tax(response)
        return float(pricing) - float(self.extract_tax(response))

    def extract_pricing_with_tax(self, response):
        return response.css('.price-display-section-total ::text').re_first(self.price_re)

    def extract_currency(self, response):
        css = '#currencySelectorPriceItinerary [selected="selected"]::attr(value)'
        return response.css(css).extract_first()

    def extract_od(self, response):
        return ''.join(response.meta['route'])

    def extract_duration(self, response):
        css = '.avail-table-vert:contains("Sin escalas") ::text'
        duration = self.clean(response.css(css).extract())
        return ' '.join(duration)

    def extract_tax(self, response):
        return response.css('.price-display-passenger-charges ::text').re_first(self.price_re)

    def extract_outbound_date(self, time_sel, response, keyword):
        date_sel = response.css('.low-fare-tabs')[0]
        return self.extract_date_time(date_sel, time_sel, keyword)

    def extract_inbound_date(self, time_sel, response, keyword):
        date_sel = response.css('.low-fare-tabs')[1]
        return self.extract_date_time(date_sel, time_sel, keyword)

    def extract_flightno(self, response):
        return self.clean(response.css('.avail-table-carrierinfo ::text').extract())[0]

    def extract_inbound_price(self, response):
        return response.css('.text-center ::text').re_first(self.price_re)

    def extract_outbound_price(self, response):
        return response.css('.text-center ::text').re_first(self.price_re)

    def extract_origin(self, response):
        return response.meta['route'][0]

    def extract_destination(self, response):
        return response.meta['route'][1]

    def extract_observation_date(self):
        return f"{datetime.now():%Y-%m-%d}"

    def extract_observation_time(self):
        return f"{datetime.now():%H:%M}"

    def extract_oneway_indicator(self, response):
        return '1' if response.meta['oneway_indicator'] else '0'

    def extract_date_time(self, date_sel, time_sel, keyword):
        raw_date = self.clean(date_sel.css('.low-fare-date ::text').extract())
        date = findall(self.date_time_re, ''.join(raw_date))[0]
        raw_time = self.clean(time_sel.css(f'.avail-table-vert:contains({keyword}) ::text').extract())

        time = findall(self.date_time_re, ''.join(raw_time))[0]
        return f'{datetime.now().year}-{date} {time}'

    def clean(self, lst_of_str):
        return [s.strip() for s in lst_of_str if s.strip()]

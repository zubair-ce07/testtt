import datetime
import json
import urllib.parse
import logging
import requests
from parsel import Selector
import copy

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

credentials = {
    'username': 'Asmaulhusna',
    'password': 'QAW200'
}


class AirBlueCrawler:
    start_url = 'https://www.airblue.com/agents/default.asp'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    input_keys = {
        'economy': 'Y',
        'business': 'C',
        'one_way': 'OW',
        'round_trip': 'RT'
    }
    output_keys = {
        'Y': 'economy',
        'C': 'business',
        'OW': 'one_way',
        'RT': 'round_trip'
    }
    session = None

    def swap_input_keys(self, input_data):
        """swap input values in air blue form-data"""
        input_data['cabin'] = self.input_keys[input_data['cabin']]
        input_data['trip_type'] = self.input_keys[input_data['trip_type']]
        if 'return_trip' in input_data:
            input_data['return_trip']['cabin'] = self.input_keys[input_data['return_trip']['cabin']]
            input_data['return_trip']['trip_type'] = self.input_keys[input_data['return_trip']['trip_type']]
        return input_data

    def swap_output_keys(self, output_data):
        """swap output values"""
        output_data['cabin'] = self.output_keys[output_data['cabin']]
        output_data['trip_type'] = self.output_keys[output_data['trip_type']]
        if 'return_trip' in output_data:
            output_data['return_trip']['cabin'] = self.output_keys[output_data['return_trip']['cabin']]
            output_data['return_trip']['trip_type'] = self.output_keys[output_data['return_trip']['trip_type']]
        return output_data

    def session_manager(self):
        """create new session for every task e.g, booking or searching trips"""
        self.session = requests.session()

    def search_trips(self, search_data):
        """:returns trips for given input date and passengers"""
        self.session_manager()
        search_data = self.swap_input_keys(search_data)
        response = self.agent_login()
        new_data = copy.deepcopy(search_data)
        new_data.update({
            'passenger_adult': 1,
            'passenger_child': 1,
            'passenger_infant': 1,
        })
        response = self.parse_agent_main(response, new_data)
        searched_trips = self.get_searched_trips(response, search_data)
        # if searched_trips:
        #     searched_trips = [self.swap_output_keys(trip) for trip in searched_trips]
        logger.info('searched trips : {0}'.format(searched_trips))
        return searched_trips

    def live_check(self, trip_data):
        """check for given trip:
            :returns (True, None) if trip exists
            :returns (True, Updated trip) if trip exists but have updated
            :returns (False, new trips) if trip doesn't exists
        """
        self.session_manager()
        trip_data = self.swap_input_keys(trip_data)
        response = self.agent_login()
        response = self.parse_agent_main(response, trip_data)
        compare_result = self.compare_search_result(response, trip_data)
        logger.info('live check result : {0}'.format(compare_result))
        return compare_result

    def book_trip(self, trip_data, user):
        """take passengers info and reserves seats"""
        self.session_manager()
        trip_data = self.swap_input_keys(trip_data)
        response = self.agent_login()
        response = self.parse_agent_main(response, trip_data)
        response = self.book_search_result(response, trip_data)
        response = self.parse_itinerary(response)
        response = self.parse_passenger_info(response, user)
        response = self.parse_additional_items(response)
        booking_item = self.parse_view_reservation(response, trip_data, user)
        logger.info('booking item : {0}'.format(booking_item))
        return booking_item

    def cancel_reservation(self, booking_id):
        """take pnr and cancel reservation"""
        self.session_manager()
        booking_tracking_url = 'https://www.airblue.com/agents/bookings/view_reservation.aspx'
        form_data = {
            'passengerName': '',
            'PNR': booking_id,
            'x': '0',
            'y': '0',
        }
        response = self.agent_login()
        logger.info('making view reservation request......', )
        response_object = self.session.post(url=booking_tracking_url,
                                            data=form_data,
                                            headers=self.headers)
        logger.info('view reservation response {0}'.format(response_object.status_code))
        response = Selector(response_object.text)
        pnr_ref = self.get_pnr_ref(response)
        pnr_cc_ref = self.get_pnr_cc_ref(response)
        currency = self.get_currency(response)
        cancel_form_data = {
            'pnr': booking_id,
            'pnrRef': pnr_ref,
            'pnrCCRef': pnr_cc_ref,
            'currency': currency,
            'action': 'Cancel Reservation'
        }
        logger.info('making cancel booking request......', )
        cancel_response_object = self.session.post(url=booking_tracking_url,
                                                   data=cancel_form_data,
                                                   headers=self.headers, )
        logger.info('cancel booking response {0}'.format(cancel_response_object.status_code))
        if cancel_response_object.status_code == 200:
            logger.info('booking canceled of booking_id : {0}'.format(booking_id))
            return True
        return False

    def email_reservation(self, booking_id, name, email, email_text):
        """take pnr and email info and mail the reservation"""
        self.session_manager()
        booking_tracking_url = 'https://www.airblue.com/agents/bookings/view_reservation.aspx'
        form_data = {
            'passengerName': '',
            'PNR': booking_id,
            'x': '0',
            'y': '0',
        }
        response = self.agent_login()
        logger.info('making view reservation request......')
        response_object = self.session.post(url=booking_tracking_url,
                                            data=form_data,
                                            headers=self.headers)
        logger.info('view reservation response {0}'.format(response_object.status_code))
        response = Selector(response_object.text)
        pnr_ref = self.get_pnr_ref(response)
        pnr_cc_ref = self.get_pnr_cc_ref(response)
        currency = self.get_currency(response)
        email_form_data = {
            'pnr': booking_id,
            'pnrRef': pnr_ref,
            'pnrCCRef': pnr_cc_ref,
            'currency': currency,
            'email_recipient': name,
            'email_address': email,
            'custom_text': email_text,
            'action': 'Send Email'
        }
        logger.info('making email booking request......')
        cancel_response_object = self.session.post(url=booking_tracking_url,
                                                   data=email_form_data,
                                                   headers=self.headers, )
        logger.info('email response {0}'.format(cancel_response_object.status_code))
        if cancel_response_object.status_code == 200:
            logger.info('booking mailed at {0} :'.format(email))
            return True
        return False

    # def issue_ticket(self, booking_id):
    #     """take pnr and purchases ticket"""
    #     self.session_manager()
    #     booking_tracking_url = 'https://www.airblue.com/agents/bookings/view_reservation.aspx'
    #     form_data = {
    #         'passengerName': '',
    #         'PNR': booking_id,
    #         'x': '0',
    #         'y': '0',
    #     }
    #     response = self.agent_login()
    #     logger.info('making view reservation request......')
    #     response_object = self.session.post(url=booking_tracking_url,
    #                                         data=form_data,
    #                                         headers=self.headers)
    #     logger.info('view reservation response {0}'.format(response_object.status_code))
    #     response = Selector(response_object.text)
    #     pnr_ref = self.get_pnr_ref(response)
    #     pnr_cc_ref = self.get_pnr_cc_ref(response)
    #     currency = self.get_currency(response)
    #     payment_method = self.get_payment_method(response)
    #     amount_paid = self.get_amount_paid(response)
    #     ticket_form_data = {
    #         'pnr': booking_id,
    #         'pnrRef': pnr_ref,
    #         'pnrCCRef': pnr_cc_ref,
    #         'currency': currency,
    #         'payment_method': payment_method,
    #         'password': 'SHAH200',
    #         'amount_paid': amount_paid,
    #         'action': 'Issue E-Tickets'
    #     }
    #     logger.info('making issue ticket request......')
    #     cancel_response_object = self.session.post(url=booking_tracking_url,
    #                                                data=ticket_form_data,
    #                                                headers=self.headers)
    #     logger.info('issue ticket response {0}'.format(cancel_response_object.status_code))
    #     if cancel_response_object.status_code == 200:
    #         logger.info('ticket issued of booking_id {0} :'.format(booking_id))
    #         return True
    #     return False

    def agent_login(self):
        """login on air blue with given agent credentials"""
        logger.info('making start request......')
        response_object = self.session.get(url=self.start_url)
        logger.info('start response {0}'.format(response_object.status_code))
        response = Selector(response_object.text)
        image_check = self.get_image_check(response)
        form_data = {
            'ta_login_action': 'dologin',
            'email_password': '',
            'login': credentials['username'],
            'password': credentials['password'],
            'imagecheck': image_check,
            'x': '0',
            'y': '0',
        }
        login_url = self.start_url
        logger.info('making login request.....')
        login_response_object = self.session.post(url=login_url, data=form_data, headers=self.headers)
        logger.info('login response {0}'.format(login_response_object.status_code))
        login_response = Selector(login_response_object.text)
        return login_response

    def parse_agent_main(self, response, search_data):
        """parse agent dashboard page and do search request"""
        search_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        form_data = {
            'TT': search_data['trip_type'],
            'DC': search_data['departure_city'],
            'AC': search_data['arrival_city'],
            'AM': search_data['departure_month'],
            'AD': search_data['departure_day'],
            'RM': '',
            'RD': '',
            'FL': 'on',
            'CC': search_data['cabin'],
            'CD': '',
            'PA': search_data['passenger_adult'],
            'PC': search_data['passenger_child'],
            'PI': search_data['passenger_infant'],
            'x': '0',
            'y': '0',
        }
        if search_data['trip_type'] == 'RT':
            round_trip_data = {
                'RM': search_data['return_month'],
                'RD': search_data['return_day'],
            }
            form_data.update(round_trip_data)
        search_url += urllib.parse.urlencode(form_data)
        logger.info('making search request.....')
        search_response_object = self.session.get(url=search_url, headers=self.headers)
        logger.info('search response {0}'.format(search_response_object.status_code))
        search_response = Selector(search_response_object.text)
        return search_response

    def get_searched_trips(self, response, search_data):
        all_trips = []
        one_way_trips = []
        return_trips = []
        outbound_trips = []
        inbound_trips = []
        flight_table_id = self.get_flight_table_id(response)
        table_selector = 'table#{0} '.format(flight_table_id)
        one_way_trips = self.parse_search_result(response, table_selector, search_data)
        if search_data['trip_type'] == 'OW':
            self.update_trips_price(one_way_trips, response, search_data)
            one_way_trips = [self.swap_output_keys(trip) for trip in one_way_trips]
            return one_way_trips

        if search_data['trip_type'] == 'RT':
            return_flight_table_id = self.get_return_flight_table_id(response)
            return_table_selector = 'table#{0} '.format(return_flight_table_id)
            return_trips = self.parse_search_result(response, return_table_selector, search_data, True)
            for one_way_trip in one_way_trips:
                for return_trip in return_trips:
                    one_way_trip.update({'return_trip': return_trip})
                    trip_item = copy.deepcopy(one_way_trip)
                    all_trips.append(trip_item)
            self.update_trips_price(all_trips, response, search_data)
            all_trips = [self.swap_output_keys(trip) for trip in all_trips]
            for trip in all_trips:
                return_trip = copy.deepcopy(trip['return_trip'])
                if return_trip not in inbound_trips:
                    if not self.is_trip_exists(return_trip, inbound_trips):
                        inbound_trips.append(copy.deepcopy(return_trip))
                del trip['return_trip']
                if trip not in outbound_trips:
                    if not self.is_trip_exists(trip, outbound_trips):
                        outbound_trips.append(copy.deepcopy(trip))

            all_trips_item = {
                'outbound_trips': outbound_trips,
                'inbound_trips': inbound_trips,
            }

            return all_trips_item

    def is_trip_exists(self, search_trip, trips):
        for trip in trips:
            if (trip['flight'] == search_trip['flight'] and
                    trip['flight_type'] == search_trip['flight_type'] and
                    trip['departure_time'] == search_trip['departure_time']):
                return True
        return False

    def update_trips_price(self, trips, response, search_data):
        for trip in trips:
            prices = self.get_prices(response, trip)
            self.update_trip_prices(prices, search_data, trip)
            if trip['trip_type'] == 'RT':
                self.update_trip_prices(prices['return_prices'], search_data, trip['return_trip'])

    def update_trip_prices(self, prices, search_data, trip):
        trip.update({
            'ADT': self.get_price_info_dict(prices, trip, 'adult'),
            'CNN': self.get_price_info_dict(prices, trip, 'child'),
            'INF': self.get_price_info_dict(prices, trip, 'infant'),
        })
        del trip['trip_key']
        trip['total_amount'] = (search_data['passenger_adult'] * trip['ADT']['total_fare']) \
                               + (search_data['passenger_child'] * trip['CNN']['total_fare']) \
                               + (search_data['passenger_infant'] * trip['INF']['total_fare'])

    def get_price_info_dict(self, prices, trip, key):
        price_info_item = {
            'total_fare': prices[key].total_fare,
            'base_fare': prices[key].base_fare,
            'taxes': prices[key].taxes,
            'fee': prices[key].fee,
            'currency_code': trip['currency']
        }
        return price_info_item

    def get_prices(self, response, trip):
        ssp = self.get_ssp(response)
        fsc = self.get_fsc(response)
        form_data = {
            'ssp': ssp,
            'fsc': fsc,
            'trip_1': trip['trip_key'],
        }
        if trip['trip_type'] == 'RT':
            form_data.update({'trip_2': trip['return_trip']['trip_key']})

        next_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        if trip['trip_key']:
            logger.info('making itinerary request.....')
            itinerary_response_object = self.session.post(url=next_url,
                                                          data=form_data,
                                                          headers=self.headers)
            logger.info('itinerary response {0}'.format(itinerary_response_object.status_code))
            itinerary_response = Selector(itinerary_response_object.text)
            prices = {
                'adult': PriceDetail(),
                'child': PriceDetail(),
                'infant': PriceDetail(),
                'return_prices': {
                    'adult': PriceDetail(),
                    'child': PriceDetail(),
                    'infant': PriceDetail(),
                }
            }
            passengers = itinerary_response.css('div.passenger_summary tbody')
            for passenger in passengers:
                key = passenger.css('td.pax-type::text').extract_first().strip().lower()
                total_fare = passenger.xpath('./tr[2]').css('td.segment-total::text').extract_first()
                prices[key].total_fare = self.format_price(total_fare)

                base_fare = passenger.xpath('./tr[2]/td[3]').css('::text').extract_first()
                prices[key].base_fare = self.format_price(base_fare)

                surcharges = passenger.xpath('./tr[2]/td[4]').css('span::text').extract_first()
                prices[key].surcharges = self.format_price(surcharges)

                taxes = passenger.xpath('./tr[2]/td[5]').css('span::text').extract_first()
                prices[key].taxes = self.format_price(taxes)

                fee = passenger.xpath('./tr[2]/td[6]').css('span::text').extract_first()
                prices[key].fee = self.format_price(fee)
                if trip['trip_type'] == 'RT':
                    return_total_fare = passenger.xpath('./tr[3]').css('td.segment-total::text').extract_first()
                    prices['return_prices'][key].total_fare = self.format_price(return_total_fare)

                    return_base_fare = passenger.xpath('./tr[2]/td[3]').css('::text').extract_first()
                    prices['return_prices'][key].base_fare = self.format_price(return_base_fare)

                    return_surcharges = passenger.xpath('./tr[2]/td[4]').css('span::text').extract_first()
                    prices['return_prices'][key].surcharges = self.format_price(return_surcharges)

                    return_taxes = passenger.xpath('./tr[2]/td[5]').css('span::text').extract_first()
                    prices['return_prices'][key].taxes = self.format_price(return_taxes)

                    return_fee = passenger.xpath('./tr[2]/td[6]').css('span::text').extract_first()
                    prices['return_prices'][key].fee = self.format_price(return_fee)
            return prices

    def format_price(self, price_string):
        return float(price_string.strip().replace(',', ''))

    def parse_search_result(self, response, flight_table, search_data, is_return_trip=False):
        """parse search page and
            :returns trips if found
            :returns False if no results found
        """
        trip_number = 2 if is_return_trip else 1
        available = self.is_flight_available(response)
        logger.info('available {0}'.format(available))
        if available is None:
            return False

        trip_list = []
        all_flights = response.css(flight_table + 'tbody')
        for current_flight in all_flights:
            flight = self.get_flight_number(current_flight)
            departure_time = self.get_departure_time(current_flight)
            arrival_time = self.get_arrival_time(current_flight)
            route = current_flight.css('td.route span::text').extract()
            route = ' '.join(route)
            standard = {
                'type': 'standard',
                'total_amount': self.get_total_amount_standard(current_flight),
                'price_per_seat': self.get_standard_price(current_flight),
                'currency': self.get_standard_currency(current_flight),
                'trip_key': self.get_trip_ket_standard(current_flight, trip_number)
            }
            premium = {
                'type': 'premium',
                'total_amount': self.get_total_amount_premium(current_flight),
                'price_per_seat': self.get_premium_price(current_flight),
                'currency': self.get_premium_currency(current_flight),
                'trip_key': self.get_trip_key_premium(current_flight, trip_number)
            }

            flight_types = [standard, premium]
            for flight_type in flight_types:
                item = {
                    'trip_type': search_data['trip_type'],
                    # 'price_per_seat': flight_type['price_per_seat'].replace(',', ''),
                    # 'total_amount': flight_type['total_amount'].replace(',', ''),
                    'currency': flight_type['currency'],
                    'cabin': search_data['cabin'],
                    'flight': flight,
                    'flight_type': flight_type['type'],
                    'route': route,
                    'departure_city': search_data['departure_city'],
                    'arrival_city': search_data['arrival_city'],
                    'departure_month': search_data['departure_month'],
                    'departure_day': search_data['departure_day'],
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'passenger_adult': search_data['passenger_adult'],
                    'passenger_child': search_data['passenger_child'],
                    'passenger_infant': search_data['passenger_infant'],
                    'trip_key': flight_type['trip_key']}
                if search_data['trip_type'] == 'RT':
                    item.update({
                        'return_month': search_data['return_month'],
                        'return_day': search_data['return_day'],
                    })
                if is_return_trip:
                    item['departure_city'], item['arrival_city'] = item['arrival_city'], item['departure_city']

                trip_list.append(item)
        return trip_list

    def compare_search_result(self, response, trip_data):
        """compare search result with given trip"""
        searched_trips = self.get_searched_trips(response, trip_data)
        if searched_trips:
            if trip_data in searched_trips:
                return True, self.swap_output_keys(trip_data)
            elif trip_data['flight']:
                for trip in searched_trips:
                    if trip['flight'] == trip_data['flight']:
                        return True, self.swap_output_keys(trip)
            else:
                return False, None
        else:
            return False, None

    def book_search_result(self, response, trip_data):
        """double check search result before reservation"""
        TRIP_1 = 1
        TRIP_2 = 2
        flight_table_id = self.get_flight_table_id(response)
        table_selector = 'table#{0} '.format(flight_table_id)
        trip_key = self.get_trip_key(response, trip_data, table_selector, TRIP_1)

        ssp = self.get_ssp(response)
        fsc = self.get_fsc(response)
        form_data = {
            'ssp': ssp,
            'fsc': fsc,
            'trip_1': trip_key,
        }
        if trip_data['trip_type'] == 'RT':
            return_flight_table_id = self.get_return_flight_table_id(response)
            return_table_selector = 'table#{0} '.format(return_flight_table_id)
            return_trip = trip_data['return_trip']
            return_trip_key = self.get_trip_key(response, return_trip, return_table_selector, TRIP_2)
            form_data.update({'trip_2': return_trip_key})

        next_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        if trip_key:
            logger.info('making itinerary request.....')
            itinerary_response_object = self.session.post(url=next_url,
                                                          data=form_data,
                                                          headers=self.headers)
            logger.info('itinerary response {0}'.format(itinerary_response_object.status_code))
            itinerary_response = Selector(itinerary_response_object.text)
            return itinerary_response

    def get_trip_key(self, response, trip_data, flight_table, trip_number):
        all_flights = response.css(flight_table + 'tbody')
        for current_flight in all_flights:
            flight = self.get_flight_number(current_flight)
            depart = self.get_departure_time(current_flight)
            standard = {
                'total_amount': self.get_total_amount_standard(current_flight),
                'price_per_seat': self.get_standard_price(current_flight),
                'currency': self.get_standard_currency(current_flight),
                'trip_key': self.get_trip_ket_standard(current_flight, trip_number),
            }
            premium = {
                'total_amount': self.get_total_amount_premium(current_flight),
                'price_per_seat': self.get_premium_price(current_flight),
                'currency': self.get_premium_currency(current_flight),
                'trip_key': self.get_trip_key_premium(current_flight, trip_number),
            }
            input_data = trip_data
            if (flight == input_data['flight']) and (depart == input_data['departure_time']):
                trip_key = standard['trip_key']
                if input_data['flight_type'] == 'premium':
                    trip_key = premium['trip_key']
                return trip_key

    def parse_itinerary(self, response):
        """parse itinerary page and make next request"""
        next_url = 'https://www.airblue.com/agents/bookings/view_itinerary.aspx'
        logger.info('making passenger_info request.....')
        passenger_response_object = self.session.post(url=next_url,
                                                      data={'submit': 'Continue', 'agreed': 'on'},
                                                      headers=self.headers)
        logger.info('passenger_info response {0}'.format(passenger_response_object.status_code))
        passenger_response = Selector(passenger_response_object.text)
        return passenger_response

    def parse_passenger_info(self, response, user):
        pnr = self.get_pnr(response)
        pnr = pnr or ''
        held_seats_ref = response.css('input[name="held_seats_ref"]::attr(value)').extract_first()
        form_data = [
            ('pnr', pnr),
            ('held_seats_ref', held_seats_ref),

            ('PX[0].PH[]', '0'),
            ('PX[0].PH[0].countryCode', user['country_code']),
            ('PX[0].PH[0].phoneNumber', user['mobile']),
            ('PX[0].PH[0].type', 'Mobile'),
            ('PX[0].EM[]', '0'),
            ('PX[0].EM[0].emailAddress', user['email']),

            ('action', 'Continue')
        ]
        for index, passenger in enumerate(user['passengers']):
            form_data.append(('PX[]', index))
            form_data.append(('PX[{0}].paxType'.format(index), passenger['type']))
            form_data.append(('PX[{0}].paxCode'.format(index), passenger['code']))
            form_data.append(('PX[{0}].gender'.format(index), '0'))
            form_data.append(('PX[{0}].title'.format(index), passenger['title']))
            form_data.append(('PX[{0}].firstName'.format(index), passenger['first_name']))
            form_data.append(('PX[{0}].lastName'.format(index), passenger['last_name']))
            form_data.append(('PX[{0}].dateOfBirth.day'.format(index), passenger['dob_day']))
            form_data.append(('PX[{0}].dateOfBirth.month'.format(index), passenger['dob_month']))
            form_data.append(('PX[{0}].dateOfBirth.year'.format(index), passenger['dob_year']))

        next_url = 'https://www.airblue.com/agents/bookings/passenger_info.aspx'
        logger.info('making additinal_items request.....')
        additional_response_object = self.session.post(url=next_url,
                                                       data=form_data,
                                                       headers=self.headers)
        logger.info('additinal_items response {0}'.format(additional_response_object.status_code))
        additional_response = Selector(additional_response_object.text)
        return additional_response

    def parse_additional_items(self, response):
        """parse additional page and make next page request"""
        pnr = self.get_pnr(response)
        current_segment = self.get_current_segment(response)
        next_segment = self.get_next_segment(response)

        form_data = [
            ('pnr', pnr),
            ('currentSegment', current_segment),
            ('nextSegment', next_segment),
            ('action', 'Save Changes')
        ]
        fls = self.get_fls(response)
        for fl in fls:
            form_data.append(('FL[]', fl))

        flyers = self.get_flyers(response)
        for flyer in flyers:
            flyer_inputs = flyer.css('input')
            for flyer_input in flyer_inputs:
                key = flyer_input.css('::attr(name)').extract_first()
                value = flyer_input.css('::attr(value)').extract_first()
                form_data.append((key, value))

        next_url = 'https://www.airblue.com/agents/bookings/item_selection.aspx?segment={0}'
        next_url.format(current_segment)
        reservation_response_object = self.session.post(url=next_url,
                                                        data=form_data,
                                                        headers=self.headers)
        reservation_response = Selector(reservation_response_object.text)
        if next_segment:
            reservation_response = self.parse_additional_items(reservation_response)
        return reservation_response

    def parse_view_reservation(self, response, trip_data, user):
        """page reservation page and return item"""
        booking_id = self.get_booking_id(response)  # pnr
        flight_date = self.get_flight_date(response)
        flight_date = datetime.datetime.strptime(flight_date, '%d %b %Y').date()
        year, month = trip_data['departure_month'].split('-')
        day = trip_data['departure_day']
        parsed_date = datetime.date(int(year), int(month), int(day))
        departure_time = response.css('td.flight-time span.leaving::text').extract_first()
        arrival_time = response.css('td.flight-time span.landing::text').extract_first()
        flight_number = response.css('td.flight-number span::text').extract_first()
        amount_due = float(trip_data['total_amount'])
        if trip_data['trip_type'] == 'RT':
            amount_due = float(trip_data['total_amount']) + float(trip_data['return_trip']['total_amount'])
        item = {
            'trip_data': self.swap_output_keys(trip_data),
            'user': user,
            'amount_due': amount_due
        }
        if (trip_data['flight'] == flight_number) and (
                trip_data['departure_time'] == departure_time) and (
                trip_data['arrival_time'] == arrival_time) and (
                flight_date == parsed_date):
            item['booking_id'] = booking_id
        else:
            return False
        self.cancel_reservation(booking_id)  # remove in production
        return item

    # ---------- utility methods ----------#
    def get_flight_date(self, response):
        return response.css('td.segment-date::text').extract_first()

    def get_booking_id(self, response):
        return response.css('form.pnr_actions input[name="pnr"]::attr(value)').extract_first()

    def get_pnr_cc_ref(self, response):
        return response.css('form.pnr_actions input[name="pnrCCRef"]::attr(value)').extract_first()

    def get_currency(self, response):
        return response.css('form.pnr_actions input[name="currency"]::attr(value)').extract_first()

    def get_pnr_ref(self, response):
        return response.css('form.pnr_actions input[name="pnrRef"]::attr(value)').extract_first()

    def get_amount_paid(self, response):
        return response.css('form.pnr_actions input[name="amount_paid"]::attr(value)').extract_first()

    def get_payment_method(self, response):
        return response.css('form.pnr_actions input[name="payment_method"]::attr(value)').extract_first()

    def get_image_check(self, response):
        return response.css('input[name="imagecheck"] ::attr(value)').extract_first()

    def get_flyers(self, response):
        return response.css('tr.flyer')

    def get_fls(self, response):
        return response.css('input[name="FL[]"]::attr(value)').extract()

    def get_next_segment(self, response):
        return response.css('input[name="nextSegment"]::attr(value)').extract_first()

    def get_current_segment(self, response):
        return response.css('input[name="currentSegment"]::attr(value)').extract_first()

    def get_pnr(self, response):
        return response.css('input[name="pnr"]::attr(value)').extract_first()

    def get_amount_due(self, response):
        return response.css('td.pnr-fare-total strong.amount-due ::text').extract_first().strip().replace(',', '')

    def get_fsc(self, response):
        fsc = response.css('input[name="fsc"]::attr(value)').extract_first()
        return fsc

    def get_ssp(self, response):
        ssp = response.css('input[name="ssp"]::attr(value)').extract_first()
        return ssp

    def get_trip_ket_standard(self, current_flight, trip_number):
        return current_flight.css(
            'td.family-ES input[name="trip_{0}"]::attr(value)'.format(trip_number)).extract_first()

    def get_trip_key_premium(self, current_flight, trip_number):
        return current_flight.css(
            'td.family-EP input[name="trip_{0}"]::attr(value)'.format(trip_number)).extract_first()

    def get_premium_price(self, current_flight):
        return current_flight.css('td.family-EP span::text').extract_first().strip()

    def get_standard_price(self, current_flight):
        return current_flight.css('td.family-ES span::text').extract_first().strip()

    def get_flight_number(self, current_flight):
        return current_flight.css('td.flight::text').extract_first().strip()

    def get_arrival_time(self, current_flight):
        return current_flight.css('td.landing::text').extract_first()

    def get_premium_currency(self, current_flight):
        return current_flight.css('td.family-EP b::text').extract_first()

    def get_standard_currency(self, current_flight):
        return current_flight.css('td.family-ES b::text').extract_first()

    def get_departure_time(self, current_flight):
        return current_flight.css('td.leaving::text').extract_first().strip()

    def get_flight_table_id(self, response):
        id = response.css('li.current-date label::attr(for)').re_first(r'trip_1(.*)')
        return 'trip_1{0}'.format(id)

    def get_return_flight_table_id(self, response):
        id = response.css('li.current-date label::attr(for)').re_first(r'trip_2(.*)')
        return 'trip_2{0}'.format(id)

    def get_total_amount_premium(self, current_flight):
        total_amount = current_flight.css('td.family-EP label::attr(data-title)').extract_first().strip()
        return total_amount.split(' ')[-1]

    def get_total_amount_standard(self, current_flight):
        total_amount = current_flight.css('td.family-ES label ::attr(data-title)').extract_first().strip()
        return total_amount.split(' ')[-1]

    def is_flight_available(self, response):
        return response.css('li.current-date label span::text').extract_first()


class PriceDetail:
    total_fare = None
    base_fare = None
    surcharges = None
    taxes = None
    fee = None


class PriceInfo:
    pass

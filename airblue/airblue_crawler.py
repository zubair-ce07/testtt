import datetime
import urllib.parse
import logging
import requests
from parsel import Selector

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

credentials = {
    'username': 'HASSANALIAHMED',
    'password': 'Sasta129'
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
    }
    output_keys = {
        'Y': 'economy',
        'C': 'business',
    }
    session = None

    def swap_input_keys(self, input_data):
        """swap input values in air blue form-data"""
        input_data['cabin'] = self.input_keys[input_data['cabin']]
        return input_data

    def swap_output_keys(self, output_data):
        """swap output values"""
        output_data['cabin'] = self.output_keys[output_data['cabin']]
        return output_data

    def session_manager(self):
        """create new session for every task e.g, booking or searching trips"""
        self.session = requests.session()

    def search_trips(self, search_data):
        """:returns trips for given input date and passengers"""
        self.session_manager()
        search_data = self.swap_input_keys(search_data)
        response = self.agent_login()
        response = self.parse_agent_main(response, search_data)
        searched_trips = self.parse_search_result(response, search_data)
        if searched_trips:
            searched_trips = [self.swap_output_keys(trip) for trip in searched_trips]
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
            'TT': 'OW',
            'DC': search_data['departure_city'],
            'AC': search_data['arrival_city'],
            'AM': search_data['arrival_month'],
            'AD': search_data['arrival_day'],
            'FL': 'on',
            'CC': search_data['cabin'],
            'CD': '',
            'PA': search_data['passenger_adult'],
            'PC': search_data['passenger_child'],
            'PI': search_data['passenger_infant'],
            'x': '0',
            'y': '0',
        }
        search_url += urllib.parse.urlencode(form_data)
        logger.info('making search request.....')
        search_response_object = self.session.get(url=search_url, headers=self.headers)
        logger.info('search response {0}'.format(search_response_object.status_code))
        search_response = Selector(search_response_object.text)
        return search_response

    def parse_search_result(self, response, search_data):
        """parse search page and
            :returns trips if found
            :returns False if no results found
        """
        available = self.is_flight_available(response)
        logger.info('available {0}'.format(available))
        if available is None:
            return False
        flight_table_id = self.get_flight_table_id(response)
        table_selector = 'table#{0} '.format(flight_table_id)
        all_flights = response.css(table_selector + 'tbody')
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
            }
            premium = {
                'type': 'premium',
                'total_amount': self.get_total_amount_premium(current_flight),
                'price_per_seat': self.get_premium_price(current_flight),
                'currency': self.get_premium_currency(current_flight),
            }

            flight_types = [standard, premium]
            trip_list = []
            for flight_type in flight_types:
                item = {
                    'price_per_seat': flight_type['price_per_seat'].replace(',', ''),
                    'total_amount': flight_type['total_amount'].replace(',', ''),
                    'currency': flight_type['currency'],
                    'cabin': search_data['cabin'],
                    'flight': flight,
                    'flight_type': flight_type['type'],
                    'route': route,
                    'departure_city': search_data['departure_city'],
                    'arrival_city': search_data['arrival_city'],
                    'arrival_month': search_data['arrival_month'],
                    'arrival_day': search_data['arrival_day'],
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'passenger_adult': search_data['passenger_adult'],
                    'passenger_child': search_data['passenger_child'],
                    'passenger_infant': search_data['passenger_infant']}

                trip_list.append(item)
                # with jsonlines.open('search_data.jsonl', mode='a') as writer:
                #     writer.write(item)
            return trip_list

    def compare_search_result(self, response, trip_data):
        """compare search result with given trip"""
        searched_trips = self.parse_search_result(response, trip_data)
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
        trip_key = None
        flight_table_id = self.get_flight_table_id(response)
        table_selector = 'table#{0} '.format(flight_table_id)
        all_flights = response.css(table_selector + 'tbody')
        for current_flight in all_flights:
            flight = self.get_flight_number(current_flight)
            depart = self.get_departure_time(current_flight)
            standard = {
                'total_amount': self.get_total_amount_standard(current_flight),
                'price_per_seat': self.get_standard_price(current_flight),
                'currency': self.get_standard_currency(current_flight),
                'trip_key': self.get_trip_ket_standard(current_flight),
            }
            premium = {
                'total_amount': self.get_total_amount_premium(current_flight),
                'price_per_seat': self.get_premium_price(current_flight),
                'currency': self.get_premium_currency(current_flight),
                'trip_key': self.get_trip_key_premium(current_flight),
            }
            input_data = trip_data
            if (flight == input_data['flight']) and (depart == input_data['departure_time']):
                trip_key = standard['trip_key'] if input_data['flight_type'] else premium['trip_key']
                break
        ssp = self.get_ssp(response)
        fsc = self.get_fsc(response)
        form_data = {
            'ssp': ssp,
            'fsc': fsc,
            'trip_1': trip_key,
        }
        next_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        if trip_key:
            logger.info('making itinerary request.....')

            itinerary_response_object = self.session.post(url=next_url,
                                                          data=form_data,
                                                          headers=self.headers)
            logger.info('itinerary response {0}'.format(itinerary_response_object.status_code))
            itinerary_response = Selector(itinerary_response_object.text)
            return itinerary_response

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
            form_data.append(('PX[{0}].gender'.format(index), passenger['gender']))
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

        next_url = 'https://www.airblue.com/agents/bookings/item_selection.aspx?segment=0'
        reservation_response_object = self.session.post(url=next_url,
                                                        data=form_data,
                                                        headers=self.headers)
        reservation_response = Selector(reservation_response_object.text)
        return reservation_response

    def parse_view_reservation(self, response, trip_data, user):
        """page reservation page and return item"""
        booking_id = self.get_booking_id(response)  # pnr
        flight_date = self.get_flight_date(response)
        flight_date = datetime.datetime.strptime(flight_date, '%d %b %Y').date()
        year, month = trip_data['arrival_month'].split('-')
        day = trip_data['arrival_day']
        parsed_date = datetime.date(int(year), int(month), int(day))
        departure_time = response.css('td.flight-time span.leaving::text').extract_first()
        arrival_time = response.css('td.flight-time span.landing::text').extract_first()
        flight_number = response.css('td.flight-number span::text').extract_first()
        item = {
            'trip_data': self.swap_output_keys(trip_data),
            'user': user
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

    def get_trip_ket_standard(self, current_flight):
        return current_flight.css(
            'td.family-ES input[name="trip_1"]::attr(value)').extract_first()

    def get_trip_key_premium(self, current_flight):
        return current_flight.css(
            'td.family-EP input[name="trip_1"]::attr(value)').extract_first()

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
        return current_flight.css('td.leaving::text').extract_first()

    def get_flight_table_id(self, response):
        return response.css('li.current-date label::attr(for)').extract_first()

    def get_total_amount_premium(self, current_flight):
        total_amount = current_flight.css('td.family-EP label::attr(data-title)').extract_first().strip()
        return total_amount.split(' ')[-1]

    def get_total_amount_standard(self, current_flight):
        total_amount = current_flight.css('td.family-ES label ::attr(data-title)').extract_first().strip()
        return total_amount.split(' ')[-1]

    def is_flight_available(self, response):
        return response.css('li.current-date label span::text').extract_first()

import urllib.parse

import requests
from parsel import Selector


class AgentBooking:
    start_url = 'https://www.airblue.com/agents/default.asp'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    session = requests.session()

    def book_trip(self, trip_data, user):
        # pending: validate data
        self.agent_login(trip_data, user)

    def agent_login(self, trip_data, user):
        print('making start request......', )
        response_object = self.session.get(url=self.start_url)
        print('start response', response_object.status_code)
        response = Selector(response_object.text)
        image_check = response.css('input[name="imagecheck"] ::attr(value)').extract_first()
        form_data = {
            'ta_login_action': 'dologin',
            'email_password': '',
            'login': 'HASSANALIAHMED',
            'password': 'Sasta129',
            'imagecheck': image_check,
            'x': '0',
            'y': '0',

        }
        login_url = self.start_url
        print('making login request.....')
        login_response_object = self.session.post(url=login_url, data=form_data, headers=self.headers)
        print('login response', login_response_object.status_code)
        login_response = Selector(login_response_object.text)
        self.parse_agent_main(login_response, trip_data, user)

    def parse_agent_main(self, response, trip_data, user):
        search_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        form_data = {
            'TT': 'OW',
            'DC': trip_data['depart_city'],
            'AC': trip_data['arrival_city'],
            'AM': trip_data['arrival_month'],
            'AD': trip_data['arrival_day'],
            'FL': 'on',
            'CC': '',
            'CD': '',
            'PA': trip_data['passenger_adult'],
            'PC': trip_data['passenger_child'],
            'PI': trip_data['passenger_infant'],
            'x': '0',
            'y': '0',
        }
        search_url += urllib.parse.urlencode(form_data)
        print('making search request.....')
        search_response_object = self.session.get(url=search_url, headers=self.headers)
        print('search response ', search_response_object.status_code)
        search_response = Selector(search_response_object.text)
        self.parse_search_result(search_response, trip_data, user)

    def parse_search_result(self, response, trip_data, user):
        ssp = response.css('input[name="ssp"]::attr(value)').extract_first()
        fsc = response.css('input[name="fsc"]::attr(value)').extract_first()
        trip_key = None
        flight_table_id = response.css('li.current-date label::attr(for)').extract_first()
        table_selector = 'table#{0} '.format(flight_table_id)
        all_flights = response.css(table_selector + 'tbody')
        for current_flight in all_flights:
            flight = current_flight.css('td.flight::text').extract_first().strip()
            depart = current_flight.css('td.leaving::text').extract_first()
            arrival = current_flight.css('td.landing::text').extract_first()
            route = current_flight.css('td.route span::text').extract()
            standard = {
                'price': current_flight.css('td.family-ES span::text').extract_first(),
                'currency': current_flight.css('td.family-ES b::text').extract_first(),
                'trip_key': current_flight.css(
                    'td.family-ES input[name="trip_1"]::attr(value)').extract_first(),
            }
            premium = {
                'price': current_flight.css('td.family-EP span::text').extract_first(),
                'currency': current_flight.css('td.family-EP b::text').extract_first(),
                'trip_key': current_flight.css(
                    'td.family-EP input[name="trip_1"]::attr(value)').extract_first(),
            }
            input_data = trip_data
            if (flight == input_data['flight']) and (depart == input_data['depart_time']):
                trip_key = standard['trip_key'] if input_data['flight_type'] else premium['trip_key']
                break
        form_data = {
            'ssp': ssp,
            'fsc': fsc,
            'trip_1': trip_key,
        }
        next_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        if trip_key:
            print('making itinerary request.....')
            itinerary_response_object = self.session.post(url=next_url,
                                                          data=form_data,
                                                          headers=self.headers,
                                                          )
            print('itinerary response ', itinerary_response_object.status_code)
            itinerary_response = Selector(itinerary_response_object.text)
            self.parse_itinerary(itinerary_response, trip_data, user)

    def parse_itinerary(self, response, trip_data, user):
        flight = response.css('td.flight-number span::text').extract_first()
        depart_time = response.css('td.flight-time span.leaving::text').extract_first()
        total_fare = response.css('td.pax-type-total ::text').extract()

        if (trip_data['depart_time'] == depart_time) and (trip_data['flight'] == flight):
            print('varified......')

        booking_number = response.css('td.flight-notes span.equipment-type::text').extract_first()
        traveller_type = response.css('td.fare-basis ::text').extract_first()
        # service_fee = response.css('td.pnr-fare-service-fee input ::attr(value)').extract_first()
        amount_due = response.css('td.pnr-fare-total strong.amount-due ::text').extract()

        next_url = 'https://www.airblue.com/agents/bookings/view_itinerary.aspx'
        print('making passenger_info request.....')
        passenger_response_object = self.session.post(url=next_url,
                                                      data={'submit': 'Continue', 'agreed': 'on'},
                                                      headers=self.headers,
                                                      )
        print('passenger_info response ', passenger_response_object.status_code)
        passenger_response = Selector(passenger_response_object.text)
        self.parse_passenger_info(passenger_response, trip_data, user)

    def parse_passenger_info(self, response, trip_data, user):
        pnr = response.css('inout[name="pnr"]::attr(value)').extract_first()
        pnr = pnr or ''
        held_seats_ref = response.css('input[name="held_seats_ref"]::attr(value)').extract_first()
        # pax_type = response.css('input[name="PX[2].paxType"]::attr(value)').extract_first()
        # pax_code = response.css('input[name="PX[2].paxCode"]::attr(value)').extract_first()
        # print(pax_code, pax_type)
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
        print('making additinal_items request.....')
        additional_response_object = self.session.post(url=next_url,
                                                       data=form_data,
                                                       headers=self.headers,
                                                       )
        print('additinal_items response ', additional_response_object.status_code)
        additional_response = Selector(additional_response_object.text)
        self.parse_additional_items(additional_response, trip_data, user)

    def parse_additional_items(self, response, trip_data, user):
        pnr = response.css('input[name="pnr"]::attr(value)').extract_first()
        current_segment = response.css('input[name="currentSegment"]::attr(value)').extract_first()
        next_segment = response.css('input[name="nextSegment"]::attr(value)').extract_first()

        form_data = [
            ('pnr', pnr),
            ('currentSegment', current_segment),
            ('nextSegment', next_segment),

            ('action', 'Save Changes')
        ]
        fls = response.css('input[name="FL[]"]::attr(value)').extract()
        for fl in fls:
            form_data.append(('FL[]', fl))

        flyers = response.css('tr.flyer')
        for flyer in flyers:
            flyer_inputs = flyer.css('input')
            for flyer_input in flyer_inputs:
                key = flyer_input.css('::attr(name)').extract_first()
                value = flyer_input.css('::attr(value)').extract_first()
                form_data.append((key, value))

        next_url = 'https://www.airblue.com/agents/bookings/item_selection.aspx?segment=0'
        reservation_response_object = self.session.post(url=next_url,
                                                        data=form_data,
                                                        headers=self.headers,
                                                        )
        reservation_response = Selector(reservation_response_object.text)
        self.parse_view_reservation(reservation_response, trip_data, user)

    def parse_view_reservation(self, response, trip_data, user):
        booking_reference = response.css('form.pnr_actions input[name="pnr"]::attr(value)').extract_first()  # pnr
        flight_date = response.css('td.flight-date ::text').extract_first()
        depart_time = response.css('td.flight-time span.leaving::text').extract_first()
        arrival_time = response.css('td.flight-time span.landing::text').extract_first()
        flight_number = response.css('td.flight-number span::text').extract_first()
        flight_notes = response.css('td.flight-notes span::text').extract_first()

        copoun_code = response.css('td.coupon-code::text').extract_first()
        flight_path = response.css('td.flight-path::text').extract_first()
        flight_date = response.css('td.segment-date::text').extract_first()
        coupon_family = response.css('td.coupon-family::text').extract_first()
        coupon_status = response.css('td.coupon-status::text').extract_first()

        pnr_ref = response.css('form.pnr_actions input[name="pnrRef"]::attr(value)').extract_first()
        pnr_cc_ref = response.css('form.pnr_actions input[name="pnrCCRef"]::attr(value)').extract_first()
        currency = response.css('form.pnr_actions input[name="currency"]::attr(value)').extract_first()
        payment_method = response.css('form.pnr_actions input[name="payment_method"]::attr(value)').extract_first()
        amount_paid = response.css('form.pnr_actions input[name="amount_paid"]::attr(value)').extract_first()

        email_form_data = {
            'pnr': booking_reference,
            'pnrRef': pnr_ref,
            'pnrCCRef': pnr_cc_ref,
            'currency': currency,
            'email_recipient': user['passengers'][0]['first_name'],
            'email_address': user['email'],
            'custom_text': 'testing from spider.......',
            'action': 'Send Email'
        }
        cancel_form_data = {
            'pnr': booking_reference,
            'pnrRef': pnr_ref,
            'pnrCCRef': pnr_cc_ref,
            'currency': currency,
            'action': 'Cancel Reservation'
        }
        ticket_form_data = {
            'pnr': booking_reference,
            'pnrRef': pnr_ref,
            'pnrCCRef': pnr_cc_ref,
            'currency': currency,
            'payment_method': payment_method,
            'password': 'SHAH200',
            'amount_paid': amount_paid,
            'action': 'Issue E-Tickets'
        }
        action_url = 'https://www.airblue.com/agents/bookings/view_reservation.aspx?PNR=' + booking_reference
        cancel_response_object = self.session.post(url=action_url,
                                                   data=cancel_form_data,
                                                   headers=self.headers,
                                                   )
        cancel_response = Selector(cancel_response_object.text)
        self.parse_done(cancel_response, booking_reference, meta={'status': 'canceled'})

    def parse_done(self, response, booking_id, meta):
        print(meta['status'] + '.......')
        print('booking id : ', booking_id)


booking = AgentBooking()
trip_data = {
    'currency': 'PKR',
    'flight': 'PA-200',
    'price': ' 9,403',
    'route': 'Nonstop A320',
    'arrival_city': 'ISB',
    'arrival_month': '2018-01',
    'depart_time': '7:30 AM',
    'flight_type': 'standard',
    'depart_city': 'KHI',
    'arrival_day': '29',
    'arrival_time': '9:40 AM',
    'passenger_adult': '2',
    'passenger_child': '0',
    'passenger_infant': '0',
}
user = {
    'passengers': [
        {
            'type': 'ADT',
            'code': 'ADT',
            'gender': '0',
            'title': 'Mr',
            'first_name': 'aaa',
            'last_name': 'aaa',
            'dob_year': '20',
            'dob_month': 'Mar',
            'dob_day': '1980',
        },
        {
            'type': 'ADT',
            'code': 'ADT',
            'gender': '0',
            'title': 'Mr',
            'first_name': 'bbb',
            'last_name': 'bbb',
            'dob_year': '21',
            'dob_month': 'Mar',
            'dob_day': '1970',
        }
    ],
    'email': 'ahmad24013@gmail.com',
    'country_code': '+92',
    'mobile': '3049896759',
}
booking.book_trip(trip_data, user)

import urllib.parse

import jsonlines
import requests
from parsel import Selector


class AgentSearch:
    start_url = 'https://www.airblue.com/agents/default.asp'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    session = requests.session()

    def search_trips(self, search_data):
        # pending: validate data
        self.agent_login(search_data)

    def agent_login(self, search_data):
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
        self.parse_agent_main(login_response, search_data)

    def parse_agent_main(self, response, search_data):
        search_url = 'https://www.airblue.com/agents/bookings/flight_selection.aspx?'
        form_data = {
            'TT': 'OW',
            'DC': search_data['departure_city'],
            'AC': search_data['arrival_city'],
            'AM': search_data['arrival_month'],
            'AD': search_data['arrival_day'],
            'FL': 'on',
            'CC': '',
            'CD': '',
            'PA': search_data['passenger_adult'],
            'PC': search_data['passenger_child'],
            'PI': search_data['passenger_infant'],
            'x': '0',
            'y': '0',
        }
        search_url += urllib.parse.urlencode(form_data)
        print('making search request.....')
        search_response_object = self.session.get(url=search_url, headers=self.headers)
        print('search response ', search_response_object.status_code)
        search_response = Selector(search_response_object.text)
        self.parse_search_result(search_response, search_data)

    def parse_search_result(self, response, search_data):
        flight_table_id = response.css('li.current-date label::attr(for)').extract_first()
        table_selector = 'table#{0} '.format(flight_table_id)
        all_flights = response.css(table_selector + 'tbody')
        for current_flight in all_flights:
            flight = current_flight.css('td.flight::text').extract_first().strip()
            departure_time = current_flight.css('td.leaving::text').extract_first()
            arrival_time = current_flight.css('td.landing::text').extract_first()
            route = current_flight.css('td.route span::text').extract()
            route = ' '.join(route)
            standard = {
                'type': 'standard',
                'price': current_flight.css('td.family-ES span::text').extract_first(),
                'currency': current_flight.css('td.family-ES b::text').extract_first(),
            }
            premium = {
                'type': 'premium',
                'price': current_flight.css('td.family-EP span::text').extract_first(),
                'currency': current_flight.css('td.family-EP b::text').extract_first(),
            }

            flight_types = [standard, premium]
            item = {}
            for flight_type in flight_types:
                item['flight'] = flight
                item['departure_time'] = departure_time
                item['arrival_time'] = arrival_time
                item['route'] = route
                item['flight_type'] = flight_type['type']
                item['price'] = flight_type['price']
                item['currency'] = flight_type['currency']
                item['departure_city'] = search_data['departure_city']
                item['arrival_city'] = search_data['arrival_city']
                item['arrival_month'] = search_data['arrival_month']
                item['arrival_day'] = search_data['arrival_day']
                item['passenger_adult'] = search_data['passenger_adult']
                item['passenger_child'] = search_data['passenger_child']
                item['passenger_infant'] = search_data['passenger_infant']
                print(item)
                with jsonlines.open('search_data.jsonl', mode='a') as writer:
                    writer.write(item)


agent = AgentSearch()
search_data = {
    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'arrival_month': '2018-01',
    'arrival_day': '29',
    'passenger_adult': '1',
    'passenger_child': '0',
    'passenger_infant': '0',
}
agent.search_trips(search_data)

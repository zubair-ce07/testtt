from prices import AirBlueCrawler

round_trip_search = {
    'trip_type': 'round_trip',  # options : one_way, round_trip
    'cabin': 'economy',  # options : economy, business
    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'departure_month': '2018-03',
    'departure_day': '01',
    'return_month': '2018-03',
    'return_day': '03',
    'passenger_adult': 2,
    'passenger_child': 0,
    'passenger_infant': 0,
}
one_way_search = {
    'trip_type': 'one_way',  # options : one_way, round_trip
    'cabin': 'economy',  # options : economy, business
    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'departure_month': '2018-03',
    'departure_day': '01',
    'passenger_adult': 2,
    'passenger_child': 0,
    'passenger_infant': 0,
}
one_way_trip_data = {
    'cabin': 'economy',
    'route': 'Nonstop A320',
    'departure_day': '01',
    'CNN': {
        'base_fare': 2850.0,
        'fee': 620.0,
        'total_fare': 8405.0,
        'taxes': 2900.0,
        'currency_code': 'PKR'
    },
    'INF': {
        'base_fare': 380.0,
        'fee': 20.0,
        'total_fare': 3045.0,
        'taxes': 2645.0,
        'currency_code': 'PKR'
    },
    'passenger_child': 0,
    'arrival_city': 'ISB',
    'arrival_time': '9:40 AM',
    'departure_month': '2018-03',
    'departure_time': '7:30 AM',
    'flight_type': 'standard',
    'ADT': {
        'base_fare': 3800.0,
        'fee': 620.0,
        'total_fare': 9403.0,
        'taxes': 2948.0,
        'currency_code': 'PKR'
    },
    'passenger_adult': 2,
    'trip_type': 'one_way',
    'passenger_infant': 0,
    'departure_city': 'KHI',
    'currency': 'PKR',
    'flight': 'PA-200',
    'total_amount': 18806.0
}
round_trip_data = {
    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'INF': {
        'base_fare': 380.0,
        'total_fare': 3045.0,
        'taxes': 2645.0,
        'fee': 20.0,
        'currency_code': 'PKR'
    },
    'cabin': 'economy',
    'departure_month': '2018-03',
    'ADT': {
        'base_fare': 3800.0,
        'total_fare': 9403.0,
        'taxes': 2948.0,
        'fee': 620.0,
        'currency_code': 'PKR'
    },
    'flight': 'PA-200',
    'route': 'Nonstop A320',
    'return_day': '03',
    'arrival_time': '9:40 AM',
    'trip_type': 'round_trip',
    'passenger_child': 0,
    'CNN': {
        'base_fare': 2850.0,
        'total_fare': 8405.0,
        'taxes': 2900.0,
        'fee': 620.0,
        'currency_code': 'PKR'
    },
    'departure_time': '7:30 AM',
    'flight_type': 'standard',
    'passenger_adult': 2,
    'departure_day': '01',
    'passenger_infant': 0,
    'currency': 'PKR',
    'total_amount': 18806.0,
    'return_month': '2018-03',
    'return_trip': {
        'arrival_city': 'KHI',
        'INF': {
            'total_fare': 3045.0,
            'taxes': 2645.0,
            'fee': 20.0,
            'currency_code': 'PKR',
            'base_fare': 380.0
        },
        'cabin': 'economy',
        'departure_month': '2018-03',
        'ADT': {
            'total_fare': 9403.0,
            'taxes': 2948.0,
            'fee': 620.0,
            'currency_code': 'PKR',
            'base_fare': 3800.0
        },
        'flight': 'PA-201',
        'route': 'Nonstop A320',
        'return_day': '03',
        'arrival_time': '12:40 PM',
        'trip_type': 'round_trip',
        'passenger_child': 0,
        'departure_city': 'ISB',
        'departure_time': '10:30 AM',
        'flight_type': 'standard',
        'passenger_adult': 2,
        'departure_day': '01',
        'passenger_infant': 0,
        'currency': 'PKR',
        'total_amount': 18806.0,
        'CNN': {
            'total_fare': 8405.0,
            'taxes': 2900.0,
            'fee': 620.0,
            'currency_code': 'PKR',
            'base_fare': 2850.0
        },
        'return_month': '2018-03'
    }
}
user = {
    'passengers': [
        {
            'type': 'ADT',
            'code': 'ADT',
            'title': 'Mr',
            'first_name': 'aaa',
            'last_name': 'aaa',
            'dob_year': '1980',
            'dob_month': 'Mar',
            'dob_day': '20',
        },
        {
            'type': 'ADT',
            'code': 'ADT',
            'title': 'Mr',
            'first_name': 'bbb',
            'last_name': 'bbb',
            'dob_year': '1971',
            'dob_month': 'Mar',
            'dob_day': '13',
        }
    ],
    'email': 'ahmad24013@gmail.com',
    'country_code': '+92',
    'mobile': '3049896759',
}
agent = AirBlueCrawler()

# agent.search_trips(one_way_search)
# agent.search_trips(round_trip_search)

# agent.book_trip(one_way_trip_data, user)
# agent.book_trip(round_trip_data, user)

# agent.cancel_reservation('ISGPWN')
# agent.email_reservation('ISGPWN', 'ahmad', 'ahmad24013@gmail.com', 'testing from spider.....')

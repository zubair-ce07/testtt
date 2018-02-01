from twoway import AirBlueCrawler

search_data = {
    'trip_type': 'round_trip',  # options : one_way, round_trip
    'cabin': 'economy',  # options : economy, business
    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'arrival_month': '2018-03',
    'arrival_day': '01',
    'return_month': '2018-03',
    'return_day': '03',
    'passenger_adult': '2',
    'passenger_child': '0',
    'passenger_infant': '0',
}
trip_data = {
    'price_per_seat': '9403',
    'total_amount': '18806',
    'currency': 'PKR',

    'trip_type': 'round_trip',
    'cabin': 'economy',
    'flight': 'PA-200',
    'flight_type': 'standard',
    'route': 'Nonstop A320',

    'departure_city': 'KHI',
    'arrival_city': 'ISB',
    'arrival_month': '2018-03',
    'arrival_day': '01',
    'return_month': '2018-03',
    'return_day': '03',
    'departure_time': '7:30 AM',
    'arrival_time': '9:40 AM',

    'passenger_adult': '2',
    'passenger_child': '0',
    'passenger_infant': '0',

    'return_trip': {
        'price_per_seat': '9403',
        'total_amount': '18806',
        'currency': 'PKR',

        'trip_type': 'round_trip',
        'cabin': 'economy',
        'flight': 'PA-201',
        'flight_type': 'standard',
        'route': 'Nonstop A320',

        'departure_city': 'ISB',
        'arrival_city': 'KHI',
        'arrival_month': '2018-03',
        'arrival_day': '29',
        'return_month': '2018-03',
        'return_day': '03',
        'departure_time': '10:30 AM',
        'arrival_time': '12:40 AM',

        'passenger_adult': '2',
        'passenger_child': '0',
        'passenger_infant': '0',
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
# agent.search_trips(search_data)
# agent.live_check(trip_data)
# agent.book_trip(trip_data, user)
# agent.cancel_reservation('ISGPWN')
# agent.email_reservation('ISGPWN', 'ahmad', 'ahmad24013@gmail.com', 'testing from spider.....')

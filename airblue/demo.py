from airblue_crawler import AirBlueCrawler

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

agent = AirBlueCrawler()

# agent.search_trips(one_way_search)
# agent.search_trips(round_trip_search)

# agent.live_check(trip_data)
# agent.book_trip(trip_data, user)
# agent.cancel_reservation('ISGPWN')
# agent.email_reservation('ISGPWN', 'ahmad', 'ahmad24013@gmail.com', 'testing from spider.....')

from enum import Enum


class Numbers(Enum):
    FARE_WAIT_TIME = 5
    FARE_DISTANCE = 15
    TIME_PASSED = 0.05
    DISTANCE_KM = 1000
    WAIT_MIN = 60


class TaxiMeterApp:
    def __init__(self):
        self.total_distance = 0
        self.total_fare = 80
        self.wait_time = 0
        self.ride_time = 0
        self.taxi_speed = 0

    def calculate_ride_time(self):
        self.ride_time += Numbers.TIME_PASSED.value

    def calculate_wait_time(self):
        if self.taxi_speed <= 10:
            self.wait_time += Numbers.TIME_PASSED.value

    def calculate_distance(self):
        self.total_distance += self.taxi_speed * Numbers.TIME_PASSED.value

    def calculate_fair(self):
        distance_fair = (self.total_distance * Numbers.FARE_DISTANCE.value)/Numbers.DISTANCE_KM.value
        wait_time_fair = (self.wait_time * Numbers.FARE_WAIT_TIME.value)/Numbers.WAIT_MIN.value
        self.total_fare = distance_fair + wait_time_fair

    def print_results(self):
        print(f'Ride_Time: {round(self.ride_time)} Seconds')
        print(f'Distance: {round(self.total_distance//1000)} KM '
              f'{round(self.total_distance % 1000)} M')
        print(f'Speed: {round(self.taxi_speed)} MPS')
        print(f'Fare: {round(self.total_fare)} Rs')
        print(f'Wait_Time: {round(self.wait_time)} Seconds')

from aenum import Enum

from taxi_ride import TaxiRide


class Numbers(Enum):
    KILOMETER = 2000
    DISTANCE = 25000
    TIME_PASSED = 0.002
    SPEED_INCREMENT_DECREMENT = 1
    REAL_FARE = 250000
    FARE_MIN = 5
    BASE_FARE = 80


class FareCalculator:
    def __init__(self):
        self.total_distance = 0
        self.total_fare = 0
        self.wait_time = 0
        self.distance_fare = 0
        self.ride_fare = 0

    def get_distance(self, speed, ride_time):
        self.total_distance += (speed * ride_time/Numbers.DISTANCE.value)
        return self.total_distance

    def get_fare(self, total_distance, ride_time):
        self.distance_fare += (total_distance/Numbers.REAL_FARE.value)
        self.ride_fare += (ride_time/Numbers.REAL_FARE.value) * Numbers.FARE_MIN.value
        self.total_fare = Numbers.BASE_FARE.value + (self.distance_fare + self.ride_fare)
        return self.total_fare

    def get_wait_time(self, speed):
        if speed <= 10:
            self.wait_time += Numbers.TIME_PASSED.value
        return self.wait_time


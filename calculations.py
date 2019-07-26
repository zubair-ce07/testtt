from aenum import Enum

from taxi_ride import TaxiRide


class Numbers(Enum):
    KILOMETER = 1000
    TIME_PASSED = 0.002
    FARE_INCREMENT = 16
    SPEED_INCREMENT_DECREMENT = 1
    REAL_FARE = 50000


class RideFareCalculations:
    def __init__(self):
        self.total_distance = 0
        self.total_fare = 80
        self.wait_time = 0
        self.speed = TaxiRide()

    def get_distance(self, speed, ride_time):
        self.total_distance += (speed * ride_time)/Numbers.KILOMETER.value
        return self.total_distance

    def get_fare(self, speed, total_distance):
        if speed <= 0.5:
            self.wait_time += Numbers.TIME_PASSED.value
            if self.wait_time > 10:
                self.wait_time = 0
                self.total_fare += Numbers.FARE_INCREMENT.value
        else:
            self.total_fare += total_distance/Numbers.REAL_FARE.value
        return self.total_fare, self.wait_time

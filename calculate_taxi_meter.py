import time

from ride_fair import RideFair


class TaxiMeterCalculator:
    def __init__(self):
        self.time_increment_factor = 1  # second
        self.ride_distance = 0  # Meters
        self.ride_fare = 0  # RS
        self.ride_time = 0  # Seconds - Minutes
        self.taxi_speed = 0  # m/s
        self.ride_wait_time = 0  # Seconds - Minutes

    def calculate_ride_time(self, is_ride_paused):
        time.sleep(self.time_increment_factor)

        if is_ride_paused:
            self.ride_time += self.time_increment_factor
        else:
            self.ride_wait_time += self.time_increment_factor

    def calculate_ride_distance(self):
        self.ride_distance += self.taxi_speed * self.time_increment_factor

    def calculate_ride_fair(self):
        ride_distance_in_km = self.ride_distance / 1000
        ride_distance_fair = ride_distance_in_km * RideFair.DISTANCE_TRAVELLED_FAIR.value

        ride_time_in_minutes = self.ride_wait_time / 60
        ride_wait_time_fair = ride_time_in_minutes * RideFair.WAITING_TIME_FAIR.value

        self.ride_fare = ride_distance_fair + ride_wait_time_fair

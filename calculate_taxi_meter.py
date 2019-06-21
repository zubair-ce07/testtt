import time

from ride_fair import RideFair
from taxi_meter_record import TaxiMeterRecord


class TaxiMeterCalculator:
    def __init__(self):
        self.taxi_meter = TaxiMeterRecord()
        self.speed_increment_factor = 5
        self.time_increment_factor = 1

    def increase_taxi_speed(self):
        self.taxi_meter.taxi_speed += self.speed_increment_factor

    def decrease_taxi_speed(self):
        self.taxi_meter.taxi_speed = max(0, self.taxi_meter.taxi_speed - self.speed_increment_factor)

    def display_taxi_meter(self):
        print(f'Ride Time: {self.taxi_meter.ride_time // 60} '
              f'Minutes {self.taxi_meter.ride_time % 60} Seconds')

        print(f'Distance: {self.taxi_meter.ride_distance // 1000} KM '
              f'{self.taxi_meter.ride_distance % 1000} Meters')

        print(f'Speed: {self.taxi_meter.taxi_speed} Meter per Second')
        print(f'Fare: {self.taxi_meter.ride_fare} Rs')

        print(f'Wait Time: {self.taxi_meter.ride_wait_time // 60} '
              f'Minutes {self.taxi_meter.ride_wait_time % 60} Seconds')

    def increment_ride_time(self, driving_status):
        if driving_status:
            self.taxi_meter.ride_time += self.time_increment_factor
        else:
            self.taxi_meter.ride_wait_time += self.time_increment_factor
            self.set_taxi_state_idle()

        time.sleep(self.time_increment_factor)

    def set_taxi_state_idle(self):
        self.taxi_meter.taxi_speed = 0

    def calculate_ride_distance(self):
        self.taxi_meter.ride_distance += self.taxi_meter.taxi_speed * self.time_increment_factor

    def calculate_ride_fair(self):
        ride_distance_in_km = self.taxi_meter.ride_distance / 1000
        ride_distance_fair = ride_distance_in_km * RideFair.DISTANCE_TRAVELLED_FAIR.value

        ride_time_in_minutes = self.taxi_meter.ride_wait_time / 60
        ride_wait_time_fair = ride_time_in_minutes * RideFair.WAITING_TIME_FAIR.value

        self.taxi_meter.ride_fare = ride_distance_fair + ride_wait_time_fair

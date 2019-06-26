import os

from calculate_taxi_meter import TaxiMeterCalculator
from taxi_meter_record import TaxiMeterRecord


class TaxiRide:
    def __init__(self):
        self.taxi_meter_calc = TaxiMeterCalculator()
        self.taxi_meter = TaxiMeterRecord()

        self.is_ride_paused = False
        self.is_ride_ended = False
        self.speed_increment_factor = 5

    def display_taxi_meter(self):
        os.system('clear')
        print(f'Ride Time: {self.taxi_meter.ride_time//60} '
              f'Minutes {self.taxi_meter.ride_time % 60} Seconds')

        print(f'Distance: {self.taxi_meter.ride_distance//1000} KM '
              f'{self.taxi_meter.ride_distance % 1000} Meters')

        print(f'Speed: {self.taxi_meter.taxi_speed} Meter per Second')
        print(f'Fare: {self.taxi_meter.ride_fare} Rs')

        print(f'Wait Time: {self.taxi_meter.ride_wait_time//60} '
              f'Minutes {self.taxi_meter.ride_wait_time % 60} Seconds')

    def set_taxi_state_idle(self):
        self.taxi_meter.taxi_speed = 0

    def increase_taxi_speed(self):
        self.taxi_meter.taxi_speed += self.speed_increment_factor

    def decrease_taxi_speed(self):
        self.taxi_meter.taxi_speed = max(0, self.taxi_meter.taxi_speed - self.speed_increment_factor)
        return self.taxi_meter.taxi_speed > 0



import time

from ride_fair_constants import FairConstants
from taxi_meter_record import TaxiMeterRecord
from utils import Utils


class TaxiMeterCalculator:

    def __init__(self):
        self.taxi_meter_record = TaxiMeterRecord()
        self.taxi_speed_increment_factor = 5
        self.ride_time_increment_factor = 1

    def increase_taxi_speed(self):
        self.taxi_meter_record.taxi_speed += self.taxi_speed_increment_factor

    def decrease_taxi_speed(self):
        if self.taxi_meter_record.taxi_speed > 0:
            self.taxi_meter_record.taxi_speed -= self.taxi_speed_increment_factor

    def display_taxi_meter(self):
        Utils.show_scaled_ride_time("Ride Time", self.taxi_meter_record.ride_time)
        Utils.show_scaled_ride_distance(self.taxi_meter_record.ride_distance)
        print(f"Speed: {self.taxi_meter_record.taxi_speed} Meter per Second")
        print(f"Fare: {self.taxi_meter_record.ride_fare} Rs")
        Utils.show_scaled_ride_time("Wait Time", self.taxi_meter_record.ride_wait_time)

    def increment_ride_time(self, driving_status):
        if driving_status:
            time.sleep(self.ride_time_increment_factor)
            self.taxi_meter_record.ride_time += self.ride_time_increment_factor
        else:
            time.sleep(self.ride_time_increment_factor)
            self.taxi_meter_record.ride_wait_time += self.ride_time_increment_factor

    def set_taxi_state_idle(self):
        self.taxi_meter_record.taxi_speed = 0

    def calculate_ride_distance(self):
        self.taxi_meter_record.ride_distance += self.taxi_meter_record.taxi_speed * \
                                                self.ride_time_increment_factor

    def calculate_ride_fair(self):
        ride_distance_fair = Utils.convert_meters_into_km(
            self.taxi_meter_record.ride_distance) * FairConstants.DISTANCE_TRAVELLED_FAIR.value
        ride_wait_time_fair = Utils.convert_seconds_into_minutes(
            self.taxi_meter_record.ride_wait_time) * FairConstants.WAITING_TIME_FAIR.value
        self.taxi_meter_record.ride_fare = round(ride_distance_fair + ride_wait_time_fair)

import time

from ride_fair import RideFair


class TaxiMeterCalculator:
    def __init__(self):
        self.time_increment_factor = 1

    def calculate_ride_time(self, is_ride_paused, taxi_meter):
        time.sleep(self.time_increment_factor)

        if is_ride_paused:
            taxi_meter.ride_time += self.time_increment_factor
        else:
            taxi_meter.ride_wait_time += self.time_increment_factor

    def calculate_ride_distance(self, taxi_meter):
        taxi_meter.ride_distance += taxi_meter.taxi_speed * self.time_increment_factor

    def calculate_ride_fair(self, taxi_meter):
        ride_distance_in_km = taxi_meter.ride_distance / 1000
        ride_distance_fair = ride_distance_in_km * RideFair.DISTANCE_TRAVELLED_FAIR.value

        ride_time_in_minutes = taxi_meter.ride_wait_time / 60
        ride_wait_time_fair = ride_time_in_minutes * RideFair.WAITING_TIME_FAIR.value

        taxi_meter.ride_fare = ride_distance_fair + ride_wait_time_fair

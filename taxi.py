import os
import time
from taxi_ride import TaxiRide
from calculations import FareCalculator, Numbers


class TaxiMeterApp:
    ride_time = 0

    def __init__(self):
        self.speed = TaxiRide()
        self.fare_calculator = FareCalculator()

    def get_results(self):
        self.ride_time += Numbers.TIME_PASSED.value
        total_distance = self.fare_calculator.get_distance(self.speed.get_speed(), self.ride_time)
        total_fare= self.fare_calculator.get_fare(total_distance, self.ride_time)
        wait_time = self.fare_calculator.get_wait_time(self.speed.get_speed())
        taxi_meter_app.print_results(total_distance, total_fare, wait_time)

    def print_results(self, total_distance, total_fare, wait_time):
        print(f'Ride Time: {round(self.ride_time)} Seconds')
        print(f'Distance : {round(total_distance/Numbers.KILOMETER.value)} KM {round(total_distance)} M')
        print(f'Speed: {round(self.speed.get_speed())} KPH')
        print(f'Fare: {round(total_fare)} Rs')
        print(f'Wait Time: {round(wait_time)} Seconds')


taxi_meter_app = TaxiMeterApp()
while True:
    taxi_meter_app.get_results()
    TaxiRide.get_taxi_state()
    os.system('clear')


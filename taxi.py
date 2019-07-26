import os

from taxi_ride import TaxiRide
from calculations import RideFareCalculations, Numbers


class TaxiMeterApp:
    ride_time = 0

    def __init__(self):
        self.speed = TaxiRide()
        self.fare_calculator = RideFareCalculations()

    def taxi_ride(self):
        self.ride_time += Numbers.TIME_PASSED.value
        total_distance = self.fare_calculator.get_distance(self.speed.get_speed(), self.ride_time)
        total_fare, wait_time = self.fare_calculator.get_fare(self.speed.get_speed(), total_distance)
        taxi_meter_app.output(total_distance, total_fare, wait_time)
        TaxiRide.get_taxi_state()

    def output(self, total_distance, total_fare, wait_time):
        print("Ride Time: %d Seconds:" % self.ride_time)
        print("Distance : %d KM %d Meters" % (total_distance/Numbers.KILOMETER.value, total_distance))
        print("Speed: %.2f KPM" % self.speed.get_speed())
        print("Fare: %d Rs" % total_fare)
        print("Wait Time: %d Seconds" % wait_time)


taxi_meter_app = TaxiMeterApp()
while True:
    taxi_meter_app.taxi_ride()
    os.system('clear')

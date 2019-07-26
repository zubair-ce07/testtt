import os
import time
import keyboard
import psutil

from taxi_ride import TaxiRide
from calculations import RideFareCalculations


class TaxiMeterApp:
    ride_time = 0

    def __init__(self):
        self.speed = TaxiRide()
        self.fare_calculator = RideFareCalculations()

    def output(self):
        self.ride_time += 0.002
        total_distance, kilometer = self.fare_calculator.get_distance(self.speed.speed_state(),
                                                                      self.ride_time)
        total_fare, wait_time = self.fare_calculator.get_fare(total_distance)
        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            p = psutil.Process()
            p.suspend()
        print("Ride Time: %d Seconds:" % self.ride_time)
        print("Distance : %d KM %d Meters" % (kilometer, total_distance))
        print("Speed: %.2f KPH" % self.speed.speed_state())
        print("Fare: %d Rs" % total_fare)
        print("Wait Time: %d Seconds" % wait_time)


taxi_meter_app = TaxiMeterApp()
while True:
    taxi_meter_app.output()
    os.system('clear')

import keyboard
from os import system
import time
import psutil
from speed import Speed
from calculations import DataCalculator

class TaxiMeterApp:
    wait_time = 0
    ride_time = 0
    total_distance = 0
    base_fare = 80
    total_fare = base_fare
    kilometer = 0

    def __init__(self):

        self.speed = Speed()
        self.data_calculator = DataCalculator()

    def output(self):
        total_distance, total_fare, ride_time, wait_time = self.data_calculator.ride_fare_calculation(
            self.speed.speed_state())
        if self.wait_time > 15:
            self.wait_time = 0.0
            self.total_fare += 16

        if total_distance > 1000:
            total_distance = 0
            self.kilometer += 1
        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            p = psutil.Process()
            p.suspend()

        print("Ride Time: %d Seconds:" % ride_time)
        print("Distance : %d KM %d Meters" % (self.kilometer, total_distance))
        print("Speed: %.2f KPH" % self.speed.speed_state())
        print("Fare: %d Rs" % total_fare)
        print("Wait Time: %.2f" % wait_time)


taxi_meter_app = TaxiMeterApp()

while True:
    taxi_meter_app.output()
    system('clear')
import keyboard
from os import system
import time
import psutil
from speed import Speed


class TaxiMeterApp:
    wait_time = 0
    ride_time = 0
    total_distance = 0
    base_fare = 80
    total_fare = base_fare
    kilometer = 0

    def __init__(self):
        self.speed = Speed()

    def ride_fare_calculation(self):
        self.ride_time += 0.002

        total_speed = self.speed.speed_state()

        if total_speed <= 15:
            self.wait_time = self.wait_time + 0.01

        if self.wait_time > 15:
            self.wait_time = 0.0
            self.total_fare += 16


        self.total_distance = self.total_distance + (total_speed * self.ride_time) / 5000
        self.total_fare = self.total_fare + (self.total_distance/15000)


        if self.total_distance > 1000:
            self.total_distance = 0;
            self.kilometer += 1

        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            p = psutil.Process()
            p.suspend()

    def output(self):
        print("Ride Time: %d Seconds" % self.ride_time)
        print("Distance : %d KM %d Meters" % (self.kilometer, self.total_distance))
        print("Speed: %.2f KPH" % self.speed.speed_state())
        print("Fare: %d Rs" % self.total_fare)
        print("Wait Time: %.2f" % self.wait_time)


taxi_meter_app = TaxiMeterApp()

while True:

    taxi_meter_app.ride_fare_calculation()
    taxi_meter_app.output()
    system('clear')
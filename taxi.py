import keyboard
from os import system
import time
import psutil
import os


class TaxiMeterApp:
    total_fare = total_speed = wait_time = ride_time = total_distance = 0
    moving_car_fare = 0.00001


    if keyboard.is_pressed('p'):
             time.sleep(5)
    if keyboard.is_pressed('e'):
            p = psutil.Process()
            p.suspend()


    def output(self):
        print("Ride Time: %.2f" % self.ride_time)
        print("Distance : %.2f Meters" % self.total_distance)
        print("Speed: %.2f KPM" % self.total_speed)
        print("Fare: %.2f" % self.total_fare)
        print("Wait Time: %.2f" % self.wait_time)


t1 = TaxiMeterApp()

while True:
    t1.fare_calculation()
    t1.output()
    system('clear')
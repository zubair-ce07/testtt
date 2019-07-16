import keyboard
from os import system
import time
import psutil


class TaxiMeterApp:
    total_speed = wait_time = ride_time = total_distance = 0
    base_fare = 80
    total_fare = base_fare

    def ride_fare_calculation(self):
        self.ride_time += 0.01

        if keyboard.is_pressed('up'):

            self.total_speed = self.total_speed + 0.2

        elif keyboard.is_pressed('down'):
            self.total_speed -= 0.1

            if self.total_speed < 0:
                self.total_speed = 0

        if self.total_speed <= 15:
            self.wait_time = self.wait_time + 0.01

        if self.wait_time > 15:
            self.wait_time = 0.0
            self.total_fare += 16

        self.total_distance = self.total_distance + (self.total_speed * self.ride_time) / 5000
        self.total_fare = self.total_fare + (self.total_distance/15000)

        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            p = psutil.Process()
            p.suspend()

    def output(self):
        print("Ride Time: %.2f" % self.ride_time)
        print("Distance : %.2f Meters" % self.total_distance)
        print("Speed: %.2f KPH" % self.total_speed)
        print("Fare: %.2f" % self.total_fare)
        print("Wait Time: %.2f" % self.wait_time)


t1 = TaxiMeterApp()


while True:
    t1.ride_fare_calculation()
    t1.output()
    system('clear')
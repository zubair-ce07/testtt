import keyboard
from math import trunc
from os import system

from datetime import datetime


class TaxiMeter:
    pause_status = False
    total_time = datetime.now()
    speed = 0
    total_distance = 0
    ride_duration = 0
    wait_duration = 0
    ride_fare = 0.03
    wait_fare = 0.01

    def calculate_fare(self):
        if self.pause_status:
            self.wait_duration += 0.01

            if keyboard.is_pressed('r'):
                self.pause_status = False
            elif keyboard.is_pressed('e'):
                return True
        else:
            if keyboard.is_pressed('up'):
                self.speed += 0.01
            elif keyboard.is_pressed('down') and self.speed > 0:
                self.speed -= 0.01

            self.ride_duration += 0.01
            self.total_distance += self.speed * 0.01

            if keyboard.is_pressed('p'):
                self.pause_status = False

        return True

    def display_speed_and_distance(self):
        print(f"Speed: {trunc(self.speed)} m/s")
        print(f"Distance: {trunc(self.total_distance)} m")

    def show_fare(self):
        time = (datetime.now() - self.total_time).total_seconds()
        time_ratio = time / (self.ride_duration + self.wait_duration)
        fare = (trunc(self.total_distance) * self.ride_fare) + \
               (trunc(time_ratio * self.wait_duration) * self.wait_fare)

        print(f"Total Time: {trunc(time)} s")
        print(f"Distance: {trunc(self.total_distance)} m")
        print(f"Wait Duration:  {trunc(time_ratio * self.wait_duration)} s")
        print(f"Fare {fare} Rs")


def main():
    if __name__ == '__main__':
        main()


taxi_meter = TaxiMeter()
ride_status = True

while ride_status:
    ride_status = taxi_meter.calculate_fare()
    taxi_meter.display_speed_and_distance()
    system('clear')
    if not ride_status:
        taxi_meter.show_fare()


import keyboard
import time

from taxi import TaxiMeterApp


class TaxiRide:
    def __init__(self):
        self.fare_calculations = TaxiMeterApp()
        self.speed_increment_factor = 8
        self.ride_finished = False

    def process_user_input(self):
        if keyboard.is_pressed('up'):
            self.increase_speed()
        elif keyboard.is_pressed('down'):
            self.decrease_speed()

    def increase_speed(self):
        self.fare_calculations.taxi_speed += self.speed_increment_factor

    def decrease_speed(self):
        self.fare_calculations.taxi_speed -= self.speed_increment_factor
        self.fare_calculations.taxi_speed = max(0, self.fare_calculations.taxi_speed)

    def ride_status(self):
        if keyboard.is_pressed('e'):
            print(f'Ride Finished')
            self.ride_finished = True
        if keyboard.is_pressed('p'):
            print(f'Ride Paused')
            time.sleep(5)

    def calculate_fare(self):
        self.fare_calculations.fare_calculator()

    def print_results(self):
        self.fare_calculations.print_results()

import keyboard
import time

from taxi import TaxiMeterApp


class TaxiRide:
    def __init__(self):
        self.meter_calculations = TaxiMeterApp()
        self.speed_increment_factor = 8
        self.ride_finished = False
        self.wait_state = False

    def process_user_input(self):
        if keyboard.is_pressed('up'):
            self.increase_speed()
        elif keyboard.is_pressed('down'):
            self.decrease_speed()
        elif keyboard.is_pressed('e'):
            print(f'Ride Finished')
            self.ride_finished = True
        elif keyboard.is_pressed('p'):
            print(f'Ride Paused')
            time.sleep(5)

    def increase_speed(self):
        self.meter_calculations.taxi_speed += self.speed_increment_factor

    def decrease_speed(self):
        self.meter_calculations.taxi_speed -= self.speed_increment_factor
        self.meter_calculations.taxi_speed = max(0, self.meter_calculations.taxi_speed)

    def calculate_fare(self):
        self.meter_calculations.fare_calculator()

    def print_results(self):
        self.meter_calculations.print_results()

    def get_taxi_state(self):
        if self.meter_calculations.taxi_speed < 10:
            self.wait_state = True
        else:
            self.wait_state = False
            self.meter_calculations.calculate_ride_time()

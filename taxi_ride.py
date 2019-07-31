import keyboard

from taxi import TaxiMeterApp


class TaxiRide:
    def __init__(self):
        self.fare_calculations = TaxiMeterApp()
        self.speed_increment_factor = 8

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

    def calculate_fare(self):
        self.fare_calculations.fare_calculator()

    def print_results(self):
        self.fare_calculations.print_results()

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
        self.fare_calculations.taxi_speed += self.speed_increment_factor

    def fare_calculator(self):
        self.fare_calculations.calculate_ride_time()
        self.fare_calculations.calculate_wait_time()
        self.fare_calculations.calculate_fair()
        self.fare_calculations.calculate_distance()

    def print_results(self):
        self.fare_calculations.print_results()

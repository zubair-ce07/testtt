import os

from ride_keys_control import RideKeyControl
from taxi_meter import TaxiMeter


class TaxiRide:
    def __init__(self):
        self.taxi_meter_calc = TaxiMeter()

        self.is_ride_resumed = False
        self.is_ride_ended = False
        self.speed_increment_factor = 5

        self.ride_controls_map = {
            RideKeyControl.UP.value: self.set_increase_speed_essentials,
            RideKeyControl.DOWN.value: self.set_decrease_speed_essentials,
            RideKeyControl.END.value: self.set_end_ride_essentials,
            RideKeyControl.RESUME.value: self.set_resume_ride_essentials,
            RideKeyControl.PAUSE.value: self.set_pause_ride_essentials,
        }

    def set_increase_speed_essentials(self):
        print('Increasing Speed')
        self.increase_taxi_speed()
        self.is_ride_resumed = True

    def set_decrease_speed_essentials(self):
        print('Decreasing Speed')
        self.is_ride_resumed = self.decrease_taxi_speed()

    def set_end_ride_essentials(self):
        print('\nRide Ended')
        self.is_ride_ended = True

    def set_resume_ride_essentials(self):
        if not self.is_ride_resumed:
            print('Ride Resumed')
            self.increase_taxi_speed()
            self.is_ride_resumed = True

    def set_pause_ride_essentials(self):
        print('Ride Paused')
        self.is_ride_resumed = False
        self.set_taxi_state_idle()

    def on_key_press_action(self, event):
        if self.ride_controls_map.get(event.name):
            self.ride_controls_map.get(event.name)()

    def display_taxi_meter(self):
        os.system('clear')
        print(f'Ride Time: {self.taxi_meter_calc.ride_time//60} '
              f'Minutes {self.taxi_meter_calc.ride_time % 60} Seconds')

        print(f'Distance: {self.taxi_meter_calc.ride_distance//1000} KM '
              f'{self.taxi_meter_calc.ride_distance % 1000} Meters')

        print(f'Speed: {self.taxi_meter_calc.taxi_speed} Meter per Second')
        print(f'Fare: {self.taxi_meter_calc.ride_fare} Rs')

        print(f'Wait Time: {self.taxi_meter_calc.ride_wait_time//60} '
              f'Minutes {self.taxi_meter_calc.ride_wait_time % 60} Seconds')

    def set_taxi_state_idle(self):
        self.taxi_meter_calc.taxi_speed = 0

    def increase_taxi_speed(self):
        self.taxi_meter_calc.taxi_speed += self.speed_increment_factor

    def decrease_taxi_speed(self):
        max_speed = max(0, self.taxi_meter_calc.taxi_speed - self.speed_increment_factor)
        self.taxi_meter_calc.taxi_speed = max_speed
        return self.taxi_meter_calc.taxi_speed > 0

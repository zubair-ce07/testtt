import keyboard

from calculate_taxi_meter import TaxiMeterCalculator
from ride_keys_control import RideKeyControl


class TaxiRide:
    def __init__(self):
        self.taxi_meter_calculator = TaxiMeterCalculator()
        self.driving_state = True
        self.ride_ended = False

        self.ride_controls_map = {
            RideKeyControl.UP.value: self.set_increase_speed_essentials,
            RideKeyControl.DOWN.value: self.set_decrease_speed_essentials,
            RideKeyControl.END.value: self.set_end_ride_essentials,
            RideKeyControl.RESUME.value: self.set_resume_ride_essentials,
            RideKeyControl.PAUSE.value: self.set_pause_ride_essentials,
        }

    def set_increase_speed_essentials(self):
        print('Increasing Speed')
        self.taxi_meter_calculator.increase_taxi_speed()
        self.driving_state = True

    def set_decrease_speed_essentials(self):
        print('Decreasing Speed')
        self.taxi_meter_calculator.decrease_taxi_speed()

    def set_end_ride_essentials(self):
        print('\nRide Ended')
        self.ride_ended = True

    def set_resume_ride_essentials(self):
        print('Ride Resumed')
        self.driving_state = True

    def set_pause_ride_essentials(self):
        self.driving_state = False
        print('Ride Paused')

    def on_key_press_action(self, event):
        if self.ride_controls_map.get(event.name):
            self.ride_controls_map.get(event.name)()

        self.taxi_meter_calculator.display_taxi_meter()


if __name__ == '__main__':
    taxi_ride = TaxiRide()
    taxi_ride.taxi_meter_calculator.display_taxi_meter()
    keyboard.on_press(taxi_ride.on_key_press_action)

    while not taxi_ride.ride_ended:
        taxi_ride.taxi_meter_calculator.increment_ride_time(taxi_ride.driving_state)
        taxi_ride.taxi_meter_calculator.calculate_ride_fair()
        taxi_ride.taxi_meter_calculator.calculate_ride_distance()

import keyboard

from calculate_taxi_meter import TaxiMeterCalculator
from ride_keys_controller import RideKeyController


class TaxiDrive:

    def __init__(self):
        self.taxi_meter_calculator = TaxiMeterCalculator()
        self.driving_state = True
        self.ride_end = False

    def on_key_press_action(self, event):
        if event.name == RideKeyController.UP.value:
            print("Increasing Speed")
            self.taxi_meter_calculator.increase_taxi_speed()
            self.driving_state = True
        elif event.name == RideKeyController.DOWN.value:
            print("Decreasing Speed")
            self.taxi_meter_calculator.decrease_taxi_speed()
        elif event.name == RideKeyController.END.value:
            print("\nRide Ended")
            self.ride_end = True
        elif event.name == RideKeyController.RESUME.value:
            print("Ride Resumed")
            self.driving_state = True
        elif event.name == RideKeyController.PAUSE.value:
            self.driving_state = False
            print("Ride Paused")

        self.taxi_meter_calculator.display_taxi_meter()


if __name__ == "__main__":
    taxi_drive = TaxiDrive()
    taxi_drive.taxi_meter_calculator.display_taxi_meter()
    keyboard.on_press(taxi_drive.on_key_press_action)
    while not taxi_drive.ride_end:
        taxi_drive.taxi_meter_calculator.increment_ride_time(
            taxi_drive.driving_state)
        taxi_drive.taxi_meter_calculator.calculate_ride_fair()
        if taxi_drive.driving_state:
            taxi_drive.taxi_meter_calculator.calculate_ride_distance()
        else:
            taxi_drive.taxi_meter_calculator.set_taxi_state_idle()

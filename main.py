
import keyboard

from compute_taxi_meter import ComputeTaxiMeter
from keys_constants import KeyConstant


class Main:

    def __init__(self):
        self.compute_taxi_meter = ComputeTaxiMeter()
        self.driving_state = True
        self.ride_end = False

    def on_key_press_action(self, event):
        if event.name == KeyConstant.UP.value:
            print("Increasing Speed")
            self.compute_taxi_meter.increase_taxi_speed()
            self.driving_state = True
        elif event.name == KeyConstant.DOWN.value:
            print("Decreasing Speed")
            self.compute_taxi_meter.decrease_taxi_speed()
        elif event.name == KeyConstant.END.value:
            print("\nRide Ended")
            self.ride_end = True
        elif event.name == KeyConstant.RESUME.value:
            print("Ride Resumed")
            self.driving_state = True
        elif event.name == KeyConstant.PAUSE.value:
            self.driving_state = False
            print("Ride Paused")
        self.compute_taxi_meter.display_taxi_meter()


if __name__ == "__main__":
    main_obj = Main()
    main_obj.compute_taxi_meter.display_taxi_meter()
    keyboard.on_press(main_obj.on_key_press_action)
    while not main_obj.ride_end:
        if main_obj.driving_state:
            main_obj.compute_taxi_meter.increment_ride_time()
        else:
            main_obj.compute_taxi_meter.increment_wait_time()

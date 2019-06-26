import keyboard

from ride_keys_control import RideKeyControl
from taxi_ride import TaxiRide


def set_increase_speed_essentials():
    print('Increasing Speed')
    taxi_ride.increase_taxi_speed()
    taxi_ride.is_ride_paused = True


def set_decrease_speed_essentials():
    print('Decreasing Speed')
    taxi_ride.is_ride_paused = taxi_ride.decrease_taxi_speed()


def set_end_ride_essentials():
    print('\nRide Ended')
    taxi_ride.is_ride_ended = True


def set_resume_ride_essentials():
    if not taxi_ride.is_ride_paused:
        print('Ride Resumed')
        taxi_ride.increase_taxi_speed()
        taxi_ride.is_ride_paused = True


def set_pause_ride_essentials():
    taxi_ride.is_ride_paused = False
    taxi_ride.set_taxi_state_idle()
    print('Ride Paused')


def on_key_press_action(event):
    if ride_controls_map.get(event.name):
        ride_controls_map.get(event.name)()


if __name__ == '__main__':
    ride_controls_map = {
        RideKeyControl.UP.value: set_increase_speed_essentials,
        RideKeyControl.DOWN.value: set_decrease_speed_essentials,
        RideKeyControl.END.value: set_end_ride_essentials,
        RideKeyControl.RESUME.value: set_resume_ride_essentials,
        RideKeyControl.PAUSE.value: set_pause_ride_essentials,
    }

    taxi_ride = TaxiRide()
    keyboard.on_press(on_key_press_action)

    while not taxi_ride.is_ride_ended:
        taxi_ride.display_taxi_meter()
        taxi_ride.taxi_meter_calc.calculate_ride_time(taxi_ride.is_ride_paused, taxi_ride.taxi_meter)
        taxi_ride.taxi_meter_calc.calculate_ride_fair(taxi_ride.taxi_meter)
        taxi_ride.taxi_meter_calc.calculate_ride_distance(taxi_ride.taxi_meter)

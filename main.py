import keyboard

from taxi_ride import TaxiRide

if __name__ == '__main__':
    taxi_ride = TaxiRide()
    keyboard.on_press(taxi_ride.on_key_press_action)

    while not taxi_ride.is_ride_ended:
        taxi_ride.display_taxi_meter()
        taxi_ride.taxi_meter_calc.calculate_ride_essentials(taxi_ride.is_ride_resumed)

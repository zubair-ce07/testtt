import os
import time
import keyboard

from taxi_ride import TaxiRide

if __name__ == '__main__':
    taxi_ride = TaxiRide()
    while True:
        if keyboard.is_pressed('p'):
            time.sleep(4)
        if keyboard.is_pressed('e'):
            break
        taxi_ride.check_speed()
        taxi_ride.fare_calculator()
        taxi_ride.print_results()
        time.sleep(0.25)
        os.system('clear')

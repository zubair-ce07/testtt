import os
import time
import keyboard

from taxi_ride import TaxiRide

if __name__ == '__main__':
    taxi_ride = TaxiRide()
    while not taxi_ride.ride_finished:
        taxi_ride.process_user_input()
        taxi_ride.ride_status()
        taxi_ride.calculate_fare()
        taxi_ride.print_results()
        time.sleep(0.1)
        os.system('clear')

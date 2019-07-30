import time
import keyboard
import psutil


class TaxiRide:
    def __init__(self):
        self.total_speed = 0
        self.speed_increment_decrement = 0.02
        self.delay = 0.1

    def get_speed(self):
        if keyboard.is_pressed('up'):
            self.increase_speed()
        elif keyboard.is_pressed('down'):
            self.decrease_speed()
        return self.total_speed

    def increase_speed(self):
        self.total_speed += self.speed_increment_decrement
        return self.total_speed

    def decrease_speed(self):
        self.total_speed -= self.speed_increment_decrement
        return self.total_speed

    @staticmethod
    def get_taxi_state():
        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            stop_ride = psutil.Process()
            stop_ride.suspend()

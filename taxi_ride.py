import time
import keyboard
import psutil


class TaxiRide:
    def __init__(self):
        self.total_speed = 0
        self.speed_increment_decrement = 1
        self.delay = 0.1

    def get_speed(self):
        if keyboard.is_pressed('up'):
            self.total_speed = self.total_speed + self.speed_increment_decrement
            time.sleep(self.delay)
        elif keyboard.is_pressed('down'):
            self.total_speed -= self.speed_increment_decrement
            time.sleep(self.delay)
            if self.total_speed < 0:
                self.total_speed = 0
        return self.total_speed

    @staticmethod
    def get_taxi_state():
        if keyboard.is_pressed('p'):
            time.sleep(5)
        if keyboard.is_pressed('e'):
            stop_ride = psutil.Process()
            stop_ride.suspend()

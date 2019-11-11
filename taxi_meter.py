#! usr/bin/python3
import math
import time

import keyboard

TIME_INTERVAL = 1
CHANGE_IN_SPEED = 1
SLEEPING_INTERVAL = 1
RIDE_MOVING_FARE_COST = 3
RIDE_WAITING_FARE_COST = 1
RIDE_MOVING_STATE = 'MOVING'
RIDE_PAUSE_STATE = 'PAUSE'
RIDE_END_STATE = 'END'


class SpeedMeter(object):

    def __init__(self, *args, **kwargs):
        super(SpeedMeter, self).__init__()
        self.current_speed = 0

    def increase_speed(self):
        self.current_speed += CHANGE_IN_SPEED
        print('\rSpeed increased to {speed}m/sec'.format(speed=self.current_speed))

    def decrease_speed(self):
        if self.current_speed <= 0:
            print('Speed can not be less then 0m/sec')
            return

        self.current_speed -= CHANGE_IN_SPEED
        print('\rSpeed decreased to {speed}m/sec'.format(speed=self.current_speed))


class DistanceMeter(object):

    def __init__(self, *args, **kwargs):
        super(DistanceMeter, self).__init__()
        self.total_distance_in_meters = 0

    def increment_in_distance(self, distance=1):
        self.total_distance_in_meters += distance

    def distance_in_kilometer(self):
        return math.ceil(self.total_distance_in_meters / 1000)


class Ride(SpeedMeter, DistanceMeter):

    def __init__(self, *args, **kwargs):
        super(Ride, self).__init__(*args, **kwargs)

        self.riding_time_in_sec = 0
        self.waiting_time_in_sec = 0
        self.ride_state = RIDE_PAUSE_STATE

    def update_ride_time(self):

        if self.ride_state == RIDE_PAUSE_STATE:
            self.increment_waiting_time()
        elif self.ride_state == RIDE_MOVING_STATE:
            self.increment_riding_time()
            self.increment_in_distance(self.current_speed)

    def pause_ride(self):
        if self.ride_state == RIDE_PAUSE_STATE:
            print('\rAlready in pause state!')
            return

        print('\rRide is now Paused!')
        self.ride_state = RIDE_PAUSE_STATE

    def resume_ride(self):
        if self.ride_state == RIDE_MOVING_STATE:
            print('\rAlready Moving!')
            return

        print('\rRide is now Moving!')
        self.ride_state = RIDE_MOVING_STATE

    def end_ride(self):
        print('\rRide is now ended!')
        self.ride_state = RIDE_END_STATE

    def increment_riding_time(self, seconds=TIME_INTERVAL):
        self.riding_time_in_sec += seconds

    def increment_waiting_time(self, seconds=TIME_INTERVAL):
        self.waiting_time_in_sec += seconds

    def decrease_speed(self):
        super(Ride, self).decrease_speed()
        if self.current_speed == 0:
            self.pause_ride()

    def increase_speed(self):
        super(Ride, self).increase_speed()
        if self.ride_state == RIDE_PAUSE_STATE:
            self.resume_ride()

    def calculate_fare(self):
        return (self.distance_in_kilometer() * RIDE_MOVING_FARE_COST) \
               + (self.waiting_time_in_minutes() * RIDE_WAITING_FARE_COST)

    def waiting_time_in_minutes(self):
        return math.ceil(self.waiting_time_in_sec / 60)

    def display_ride_stats(self):
        print('\r\nRide Time : {time} seconds'.format(time=self.riding_time_in_sec))
        print('\rDistance : {distance}'.format(distance=self.distance_in_kilometer()))
        print('\rSpeed : {speed}m/sec'.format(speed=self.total_distance_in_meters // self.riding_time_in_sec))
        print('\rFare : {fare} Rs'.format(fare=self.calculate_fare()))
        print('\rWait Time : {time} Minutes'.format(time=self.waiting_time_in_minutes()))


def attatch_listeners_to_keystroke(ride):
    keyboard.add_hotkey('e', ride.end_ride)
    keyboard.add_hotkey('shift+e', ride.end_ride)
    keyboard.add_hotkey('p', ride.pause_ride)
    keyboard.add_hotkey('shift+p', ride.pause_ride)
    keyboard.add_hotkey('r', ride.resume_ride)
    keyboard.add_hotkey('shift+r', ride.resume_ride)
    keyboard.add_hotkey('up', ride.increase_speed)
    keyboard.add_hotkey('down', ride.decrease_speed)


def main():
    input('Press any key to start the ride.')
    take_ride = Ride()
    take_ride.resume_ride()
    attatch_listeners_to_keystroke(take_ride)

    while True:
        time.sleep(SLEEPING_INTERVAL)
        take_ride.update_ride_time()
        if take_ride.ride_state == RIDE_END_STATE:
            break

    take_ride.display_ride_stats()
    keyboard.wait('esc')


if __name__ == '__main__':
    main()

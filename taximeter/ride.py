import math

from config import Configurations as Config
from distance_meter import DistanceMeter
from speed_meter import SpeedMeter


class Ride(SpeedMeter, DistanceMeter):
    def __init__(self, *args, **kwargs):
        super(Ride, self).__init__(*args, **kwargs)

        self.riding_time_in_sec = 0
        self.waiting_time_in_sec = 0
        self.ride_state = Config.RIDE_PAUSE_STATE

    def update_ride_time(self):

        if self.ride_state == Config.RIDE_PAUSE_STATE:
            self.increment_waiting_time()
        elif self.ride_state == Config.RIDE_MOVING_STATE:
            self.increment_riding_time()
            self.increment_in_distance(self.current_speed)

    def pause_ride(self):
        if self.ride_state == Config.RIDE_PAUSE_STATE:
            print('\rAlready in pause state!')
            return

        print('\rRide is now Paused!')
        self.ride_state = Config.RIDE_PAUSE_STATE

    def resume_ride(self):
        if self.ride_state == Config.RIDE_MOVING_STATE:
            print('\rAlready Moving!')
            return

        print('\rRide is now Moving!')
        self.ride_state = Config.RIDE_MOVING_STATE

    def end_ride(self):
        print('\rRide is now ended!')
        self.ride_state = Config.RIDE_END_STATE

    def increment_riding_time(self, seconds=Config.TIME_INTERVAL):
        self.riding_time_in_sec += seconds

    def increment_waiting_time(self, seconds=Config.TIME_INTERVAL):
        self.waiting_time_in_sec += seconds

    def decrease_speed(self):
        super(Ride, self).decrease_speed()

        if self.current_speed == 0:
            self.pause_ride()

    def increase_speed(self):
        super(Ride, self).increase_speed()
        if self.ride_state == Config.RIDE_PAUSE_STATE:
            self.resume_ride()

    def calculate_fare(self):
        return (self.distance_in_kilometer() * Config.RIDE_MOVING_FARE_COST) \
               + (self.waiting_time_in_minutes() * Config.RIDE_WAITING_FARE_COST)

    def waiting_time_in_minutes(self):
        return math.ceil(self.waiting_time_in_sec / 60)

    def display_ride_stats(self):
        print('\r\nRide Time : {time} seconds'.format(time=self.riding_time_in_sec))
        print('\rDistance : {distance}'.format(distance=self.distance_in_kilometer()))
        print('\rSpeed : {speed}m/sec'.format(speed=self.total_distance_in_meters // self.riding_time_in_sec))
        print('\rFare : {fare} Rs'.format(fare=self.calculate_fare()))
        print('\rWait Time : {time} Minutes'.format(time=self.waiting_time_in_minutes()))

import math


class DistanceMeter(object):
    def __init__(self, *args, **kwargs):
        super(DistanceMeter, self).__init__()
        self.total_distance_in_meters = 0

    def increment_in_distance(self, distance=1):
        self.total_distance_in_meters += distance

    def distance_in_kilometer(self):
        return math.ceil(self.total_distance_in_meters / 1000)

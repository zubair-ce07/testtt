from taxi_ride import TaxiRide


class RideFareCalculations:
    def __init__(self):
        self.total_distance = 0
        self.total_fare = 80
        self.kilometer = 0
        self.wait_time = 0
        self.speed = TaxiRide()

    def get_distance(self, speed, ride_time):
        self.total_distance += (speed * ride_time) / 5000
        if self.total_distance > 1000:
            self.total_distance = 0
            self.kilometer += 1
        return self.total_distance, self.kilometer

    def get_fare(self, total_distance):
        self.total_fare += (total_distance/15000)
        if self.speed.speed_state() <= 15:
            self.wait_time = self.wait_time + 0.002
        if self.wait_time > 5:
            self.total_fare += 16
            self.wait_time = 0.0
        return self.total_fare, self.wait_time

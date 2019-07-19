class DataCalculator:
    def __init__(self):
        self.total_distance = 0
        self.total_fare = 80
        self.ride_time = 0
        self.wait_time = 0

    def ride_fare_calculation(self, speed):
        self.ride_time += 0.002

        if speed <= 15:
            self.wait_time = self.wait_time + 0.01

        self.total_distance = self.total_distance + (speed * self.ride_time) / 5000
        self.total_fare = self.total_fare + (self.total_distance / 15000)

        return self.total_distance, self.total_fare, self.ride_time, self.wait_time
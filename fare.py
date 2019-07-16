import keyboard


def fare_calculation(self):
    self.ride_time += 0.01

    if self.total_speed <= 14:
        self.wait_time = self.wait_time + 0.01

    if self.wait_time > 10:
        self.wait_time = 0.0
        self.total_fare += 4.0

    if keyboard.is_pressed('up'):

        self.total_speed = self.total_speed + 0.05
        self.total_fare = self.total_fare + (self.moving_car_fare * self.total_distance)

    elif keyboard.is_pressed('down') and self.total_speed != 0:
        if self.total_speed <= 0.05:
            self.total_speed = 0

            self.total_fare = self.total_fare + (self.moving_car_fare * self.total_distance)
        else:
            self.total_speed -= 0.05

            self.total_fare = self.total_fare + (self.moving_car_fare * self.total_distance)

    self.total_distance += (self.total_speed * self.ride_time) / 100000
    self.total_fare += (self.moving_car_fare * self.total_distance)

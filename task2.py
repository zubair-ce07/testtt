import keyboard
from os import system


class TaxiMeter:
    total_fare = 0
    speed = 0
    moving_car_fare = 0.0005
    cumulative_ideal_time = 0.0

    def calculate_fare(self):

        if keyboard.is_pressed('1'):
            self.speed += 0.01
            self.total_fare += (self.moving_car_fare * self.speed)
        elif keyboard.is_pressed('0') and self.speed != 0:

            if self.speed <= 0.01:
                self.speed = 0
            else:
                self.speed -= 0.01
                self.total_fare += (self.moving_car_fare * self.speed)
        else:

            if self.speed == 0:
                self.cumulative_ideal_time += 0.01

                if self.cumulative_ideal_time > 15:
                    self.cumulative_ideal_time = 0.0
                    self.total_fare += 0.5
            else:
                self.total_fare += (self.moving_car_fare * self.speed)

    def display_fare(self):
        print(f'Speed: {self.speed}')
        print(f'Total fare: {self.total_fare}')
        print(f'Idle Time: {self.cumulative_ideal_time}')


def main():
    taxi_meter = TaxiMeter()

    while True:
        taxi_meter.calculate_fare()
        taxi_meter.display_fare()
        system('clear')


if __name__ == '__main__':
    main()


import keyboard
from os import system


class TaxiMeter:
    total_fare = 0
    speed = 0
    fare = 0.0005
    cumulative_ideal_time = 0.0

    def calculate_fare(self):
        if keyboard.is_pressed('up'):
            self.speed += 0.01
        elif keyboard.is_pressed('down') and self.speed > 0.1:
            self.speed -= 0.01
        elif self.speed <= 0.1:
            self.cumulative_ideal_time += 0.01

        if self.cumulative_ideal_time > 15:
            self.cumulative_ideal_time = 0.0
            self.total_fare += 0.5

        self.total_fare += (self.fare * self.speed)

    def display_fare(self):
        print("Speed: %.1f m/s" % self.speed)
        print("Total fare: %.2f Rs" % self.total_fare)
        print("Idle Time: %.2f s" % self.cumulative_ideal_time)


def main():
    if __name__ == '__main__':
        main()


taxi_meter = TaxiMeter()

while True:
    taxi_meter.calculate_fare()
    taxi_meter.display_fare()
    system('clear')


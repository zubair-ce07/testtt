import keyboard
from os import system



class TaxiMeter:
    def __init__(self):
        self.TotalFare = 0
        self.Speed = 0
        self.FareRunning = 0.0005
        self.CumulativeIdealTime = 0.0

    def calculate_fare(self):
        if keyboard.is_pressed('1'):  # if key 'q' is pressed
            self.Speed += 0.01
            self.TotalFare += (self.FareRunning * self.Speed)

        elif keyboard.is_pressed('0') and self.Speed != 0:
            if self.Speed <= 0.01:
                self.Speed = 0
            else:
                self.Speed -= 0.01
                self.TotalFare += (self.FareRunning * self.Speed)

        else:

            if self.Speed == 0:
                self.CumulativeIdealTime += 0.01
                if self.CumulativeIdealTime > 15:
                    self.CumulativeIdealTime = 0.0
                    self.TotalFare += 0.5

            else:
                self.TotalFare += (self.FareRunning * self.Speed)

            pass

    def display_fare(self):
        print("Speed:", '%.2f' % self.Speed)
        print("Total fare ", '%.2f' % self.TotalFare)
        print("Idle Time", '%.2f' % self.CumulativeIdealTime)


meter = TaxiMeter()

while True:
    meter.calculate_fare()
    meter.display_fare()
    system('clear')

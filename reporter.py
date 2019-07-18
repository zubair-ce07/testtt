class ReportGenerator:

    low = "\033[1;34m+"
    high = "\033[1;31m+"

    def monthly_average(self, data):
        print(f"Highest Average: {round(data[0])}")
        print(f"Lowest Average: {round(data[1])}")
        print(f"Average Mean Humidity:{round(data[2])}%")

    def print_max_min(self, data):
        print(f"Highest: {data[0].highest_temp}C on {data[0].date.strftime('%b')} "
              f"{data[0].date.day}")
        print(f"Lowest: {data[1].lowest_temp}C on {data[2].date.strftime('%b')} "
              f"{data[1].date.day}")
        print(f"Humidity: {data[2].highest_humidity}% on {data[2].date.strftime('%b')} "
              f"{data[2].date.day}")

    def print_chart(self, data):
        for i in data:
            print(f"{self.low * i.lowest_temp}"
                  f" {i.lowest_temp} C \n {self.high * i.highest_temp}"
                  f" {i.highest_temp} C")

    def bonus_chart(self, data):
        for i in data:
            print(f"{self.low * i.lowest_temp}"
                  f"{self.high * (i.highest_temp - i.lowest_temp)}"
                  f" {i.lowest_temp} C - {i.highest_temp} C")



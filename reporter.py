class ReportGenerator:

    def yearly(self, yearly):
        print(f"Highest: {yearly[0].highest_temp}C on {yearly[0].date.day}"
              f" {yearly[0].date.strftime('%b')}")
        print(f"Lowest: {yearly[1].lowest_temp}C on {yearly[1].date.day}"
              f" {yearly[2].date.strftime('%b')}")
        print(f"Humidity: {yearly[2].highest_humidity}% on {yearly[2].date.day}"
              f" {yearly[2].date.strftime('%b')}\n")

    def monthly(self, results):
        print(f"Highest Average: {results[0]}")
        print(f"Lowest Average: {results[1]}")
        print(f"Average Mean Humidity:{results[2]}%\n")



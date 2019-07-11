class ReportGenerator:


    red_stars = '\33[34m'
    blue_stars = '\33[4m'

    def yearly(self, filtered_records):
        print(f"Highest: {filtered_records[0].highest_temp}C on {filtered_records[0].date.day}"
              f" {filtered_records[0].date.strftime('%b')}")
        print(f"Lowest: {filtered_records[1].lowest_temp}C on {filtered_records[1].date.day}"
              f" {filtered_records[2].date.strftime('%b')}")
        print(f"Humidity: {filtered_records[2].highest_humidity}% on {filtered_records[2].date.day}"
              f" {filtered_records[2].date.strftime('%b')}\n")

    def monthly(self, results):
        print(f"Highest Average: {results[0]}")
        print(f"Lowest Average: {results[1]}")
        print(f"Average Mean Humidity:{results[2]}%\n")



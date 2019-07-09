class ReportGenerator:

    blue_stars = '\033[1;34m*\033[1;m'
    red_stars = '\033[1;31m*\033[1;m'

    def generate_monthly_report(self, results):
        print(f"Highest Average: {round(results[0])}")
        print(f"Lowest Average: {round(results[1])}")
        print(f"Average Mean Humidity:{round(results[2])}%\n")

    def generate_yearly_report(self, results):
        print(f"Highest: {results[0].max_temp}C on {results[0].date.day}"
              f" {results[0].date.strftime('%b')}")
        print(f"Lowest: {results[1].min_temp}C on {results[1].date.day}"
              f" {results[2].date.strftime('%b')}")
        print(f"Humidity: {results[2].max_humidity}% on {results[2].date.day}"
              f" {results[2].date.strftime('%b')}\n")

    def generate_chart_report(self, records, bonus=None):
        for record in records:
            print(f"{self.blue_stars * record.min_temp}", end='')

            if bonus:
                print(f"{self.red_stars * (record.max_temp - record.min_temp)}"
                      f" {record.min_temp} C - {record.max_temp} C\n")
            else:
                print(f" {record.min_temp} C \n"
                      f"{self.red_stars * record.max_temp}"
                      f" {record.max_temp} C\n")

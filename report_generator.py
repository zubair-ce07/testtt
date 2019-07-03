import calendar


class ReportGenerator:

    Blue = '\033[1;34m*\033[1;m'
    Red = '\033[1;31m*\033[1;m'

    def generate_monthly_report(self, avg_high_temp,
                                avg_min_temp, avg_mean_humid):

        print(f"Highest Average: {round(avg_high_temp)}")
        print(f"Lowest Average: {round(avg_min_temp)}")
        print(f"Average Mean Humidity: "
              f"{round(avg_mean_humid)}%\n")

    def generate_yearly_report(self, yearly_highest_temp_date,
                               yearly_highest_temp, yearly_lowest_temp_date,
                               yearly_lowest_temp, yearly_most_humid_day,
                               yearly_most_humid_value):

        print(f"Highest: {yearly_highest_temp}C on "
              f"{yearly_highest_temp_date.day}"
              f" {calendar.month_abbr[yearly_highest_temp_date.month]}")

        print(f"Lowest: {yearly_lowest_temp}C on "
              f"{ yearly_lowest_temp_date.day}"
              f" {calendar.month_abbr[yearly_lowest_temp_date.month]}")

        print(f"Humidity: {yearly_most_humid_value}% on "
              f"{yearly_most_humid_day.day}"
              f" {calendar.month_abbr[yearly_most_humid_day.month]}")

    def generate_bonus_report(self, weather_files, date):

        row_count = 0
        for entry in weather_files:
            if entry.date.year == date.year and \
                    entry.date.month == date.month:
                row_count += 1
                maximum = entry.maximum_temp
                minimum = entry.minimum_temp
                difference = maximum - minimum
                print(row_count, " ", end='')
                for values in range(minimum):
                    print(self.Blue, end='')
                for values in range(difference):
                    print(self.Red, end='')
                print(" ", minimum, "C - ", maximum, "C\n")

    def generate_chart_report(self, weather_files, date):

        row_count = 0
        for entry in weather_files:
            if entry.date.year == date.year and \
                    entry.date.month == date.month:
                row_count += 1
                maximum = entry.maximum_temp
                minimum = entry.minimum_temp
                print(row_count, " ", end='')
                for values in range(minimum):
                    print(self.Blue, end='')
                print(f" {minimum} C")
                print(row_count, " ", end='')
                for values in range(maximum):
                    print(self.Red, end='')
                print(f" {maximum} C")

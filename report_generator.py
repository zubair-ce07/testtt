import calendar


class ReportGenerator:

    blue_stars = '\033[1;34m*\033[1;m'
    red_stars = '\033[1;31m*\033[1;m'

    def generate_monthly_report(self, avg_high_temp,
                                avg_min_temp, avg_mean_humid):
        print(f"Highest Average: {round(avg_high_temp)}")
        print(f"Lowest Average: {round(avg_min_temp)}")
        print(f"Average Mean Humidity: "
              f"{round(avg_mean_humid)}%\n")

    def generate_yearly_report(self, yearly_list):
        print(f"Highest: {yearly_list[0].maximum_temp}C on "
              f"{yearly_list[0].date.day}"
              f" {calendar.month_abbr[yearly_list[0].date.month]}")
        print(f"Lowest: {yearly_list[1].minimum_temp}C on "
              f"{ yearly_list[1].date.day}"
              f" {calendar.month_abbr[yearly_list[1].date.month]}")
        print(f"Humidity: {yearly_list[2].maximum_humidity}% on "
              f"{yearly_list[2].date.day}"
              f" {calendar.month_abbr[yearly_list[2].date.month]}\n")

    def generate_bonus_report(self, bonus_records):
        for record in bonus_records:
            maximum_temp = record.maximum_temp
            minimum_temp = record.minimum_temp
            difference = maximum_temp - minimum_temp
            print(" ", end='')
            for values in range(minimum_temp):
                print(self.blue_stars, end='')
            for values in range(difference):
                print(self.red_stars, end='')
            print(" ", minimum_temp, "C - ", maximum_temp, "C\n")

    def generate_chart_report(self, chart_records):
        for record in chart_records:
            maximum_temp = record.maximum_temp
            minimum_temp = record.minimum_temp
            print(" ", end='')
            for values in range(minimum_temp):
                print(self.blue_stars, end='')
            print(f" {minimum_temp} C")
            print(" ", end='')
            for values in range(maximum_temp):
                print(self.red_stars, end='')
            print(f" {maximum_temp} C\n")

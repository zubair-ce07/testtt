import calendar


class WeatherReportGenerator:
    def generate_yearly_report(self, yearly_result):
        highest_temperature, lowest_temperature, highest_humidity = yearly_result
        print(
            f"Highest: {highest_temperature.high_temperature}C on {calendar.month_name[highest_temperature.date.month]}"
            f" {highest_temperature.date.day}")
        print(f"Lowest: {lowest_temperature.low_temperature}C on {calendar.month_name[lowest_temperature.date.month]} "
              f"{lowest_temperature.date.day}")
        print(f"Humidity: {highest_humidity.humidity}% on {calendar.month_name[highest_humidity.date.month]} "
              f"{highest_humidity.date.day}")

    def generate_monthly_avg_report(self, result_avgs):
        high_avg_temperature, low_avg_temperature, avg_mean_humidity = result_avgs
        print(f"Highest Average: {high_avg_temperature}C")
        print(f"Lowest Average: {low_avg_temperature}C")
        print(f"Average Mean Humidity: {avg_mean_humidity}%")

    def generate_monthly_temperatures_report(self, readings):
        for day_reading in readings:
            high_temperature = '\033[31m' + '+' * int(day_reading.high_temperature) + '\033[30m'
            low_temperature = '\033[34m' + '+' * int(day_reading.low_temperature) + '\033[30m'
            print(f"{day_reading.date.day} {high_temperature}{day_reading.high_temperature}C")
            print(f"{day_reading.date.day} {low_temperature}{day_reading.low_temperature}C")

    def generate_monthly_temperatures_report_bonus(self, readings):
        for day_reading in readings:
            high_temperature = '\033[31m' + '+' * int(day_reading.high_temperature) + '\033[30m'
            low_temperature = '\033[34m' + '+' * int(day_reading.low_temperature) + '\033[30m'
            print(f"{day_reading.date.day} {high_temperature}"f"{low_temperature}"
                  f"{day_reading.high_temperature}C - {day_reading.low_temperature}C ")

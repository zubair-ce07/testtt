class ReportGenerator:

    low = "\033[1;34m+"
    high = "\033[1;31m+"
    red = "\033[1;31m"
    blue = "\033[1;34m"

    @staticmethod
    def print_yearly(data):
        print(f"Highest: {data.max_temp.max_temp}C" + " on " 
              f"{data.max_temp.date:%B %d}")
        print(f"Lowest: {data.min_temp.min_temp}C" + " on "
              f"{data.min_temp.date:%B %d}")
        print(f"Humidity: {data.max_humidity.max_humidity}%" + " on " 
              f"{data.max_humidity.date:%B %d}")

    @staticmethod
    def print_monthly(data):
        print(f"Highest Average: {data.max_avg_temp.mean_temp}C")
        print(f"Lowest Average: {data.min_avg_temp.mean_temp}C")
        print(f"Average Mean Humidity: {data.mean_humidity:.0f}%")

    @staticmethod
    def print_double_chart(data):
        for weather_reading in data.monthly_temp:
            max_temp = weather_reading.max_temp
            min_temp = weather_reading.min_temp
            red = ReportGenerator.red
            blue = ReportGenerator.blue
            print(f"{red}{weather_reading.date.day} {ReportGenerator.high * max_temp} {max_temp}C")
            print(f"{blue}{weather_reading.date.day} {ReportGenerator.low * min_temp} {min_temp}C")

    @staticmethod
    def print_bonus_chart(data):
        for weather_reading in data.monthly_temp:
            max_temp = weather_reading.max_temp
            min_temp = weather_reading.min_temp
            print(f"{ReportGenerator.low * min_temp}{ReportGenerator.high * max_temp}"
                  f" {ReportGenerator.blue}{min_temp}C - {ReportGenerator.red}{max_temp}C")

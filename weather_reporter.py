class ReportGenerator:

    blue_plus_sign = "\033[1;34m+"
    red_plus_sign = "\033[1;31m+"
    red_color_code = "\033[1;31m"
    purple_color_code = "\033[1;35m"
    blue_color_code = "\033[1;34m"

    @staticmethod
    def print_yearly_report(data):
        print(f"Highest: {data.max_temp.max_temp}C" + " on " 
              f"{data.max_temp.date:%B %d}")
        print(f"Lowest: {data.min_temp.min_temp}C" + " on "
              f"{data.min_temp.date:%B %d}")
        print(f"Humidity: {data.max_humidity.max_humidity}%" + " on " 
              f"{data.max_humidity.date:%B %d}")

    @staticmethod
    def print_monthly_report(data):
        print(f"Highest Average: {data.max_avg_temp.mean_temp}C")
        print(f"Lowest Average: {data.min_avg_temp.mean_temp}C")
        print(f"Average Mean Humidity: {data.mean_humidity:.0f}%")

    @staticmethod
    def print_double_chart(data):
        for weather_reading in data.monthly_temp:
            max_temp = weather_reading.max_temp
            min_temp = weather_reading.min_temp
            red_color = ReportGenerator.red_color_code
            blue_color = ReportGenerator.blue_color_code
            purple_color = ReportGenerator.purple_color_code
            print(f"{purple_color}{weather_reading.date:%d}"
                  f" {red_color}{ReportGenerator.red_plus_sign * max_temp}"
                  f"{purple_color} {max_temp}C")
            print(f"{purple_color}{weather_reading.date:%d}"
                  f" {blue_color}{ReportGenerator.blue_plus_sign * min_temp}"
                  f"{purple_color} {min_temp}C")

    @staticmethod
    def print_bonus_chart(data):
        for weather_reading in data.monthly_temp:
            max_temp = weather_reading.max_temp
            min_temp = weather_reading.min_temp
            purple_color = ReportGenerator.purple_color_code
            print(f"{purple_color}{weather_reading.date:%d} "
                  f"{ReportGenerator.blue_plus_sign * min_temp}"
                  f"{ReportGenerator.red_plus_sign * max_temp}"
                  f" {purple_color}{min_temp}C - {max_temp}C")

import datetime
from calculations import Calculations

class Report:
    
    @staticmethod
    def show_yearly_report (weather_readings):
        highest_temp_record = Calculations.calculate_max("Max TemperatureC", weather_readings)
        lowest_temp_record = Calculations.calculate_min("Min TemperatureC", weather_readings)
        max_humidity_record = Calculations.calculate_max("Max Humidity", weather_readings)

        highest_temp_PKT = datetime.datetime.strptime(highest_temp_record.get("PKT"), "%Y-%m-%d").strftime("%B %d")
        lowest_temp_PKT = datetime.datetime.strptime(lowest_temp_record.get("PKT"), "%Y-%m-%d").strftime("%B %d")
        max_humidity_PKT = datetime.datetime.strptime(max_humidity_record.get("PKT"), "%Y-%m-%d").strftime("%B %d")

        print(f"Highest: {highest_temp_record.get('Max TemperatureC')}C on {highest_temp_PKT}")
        print(f"Lowest: {lowest_temp_record.get('Min TemperatureC')}C on {lowest_temp_PKT}")
        print(f"Most Humid Day: {max_humidity_record.get('Max Humidity')}% on {max_humidity_PKT}")

    @staticmethod
    def show_monthly_report (weather_readings):
        print(f"Highest Average: {Calculations.calculate_average('Max TemperatureC', weather_readings)}C")
        print(f"Lowest Average: {Calculations.calculate_average('Min TemperatureC', weather_readings)}C")
        print(f"Average Mean Humidity: {Calculations.calculate_average('Max Humidity', weather_readings)}%")

    @staticmethod
    def show_chart_report(readings):
        print(datetime.datetime.strptime(readings[0].get("PKT"), "%Y-%m-%d").strftime("%B %Y"))
        for reading in readings:
            max_temperature = reading.get("Max TemperatureC")
            min_temperature = reading.get("Min TemperatureC")
            date = reading.get("PKT").split('-')[2]

            if max_temperature:
                print(f"{date} ", end="")
                for i in range(int(max_temperature)):
                    print("\x1b[91m+\x1b[00m", end="")
                print(f" {max_temperature}C")

            if min_temperature:
                print(f"{date} ", end="")
                for i in range(int(min_temperature)):
                    print("\x1b[34m+\x1b[00m", end="")
                print(f" {min_temperature}C")
    
    @staticmethod
    def show_one_liner_chart_report(readings):
        print(datetime.datetime.strptime(readings[0].get("PKT"), "%Y-%m-%d").strftime("%B %Y"))
        
        for reading in readings:
            max_temperature = reading.get("Max TemperatureC")
            min_temperature = reading.get("Min TemperatureC")
            date = reading.get("PKT").split('-')[2]
            if max_temperature and min_temperature:
                print(f"{date} " , end="")
                for i in range(int(min_temperature)):
                    print("\x1b[34m+\x1b[00m", end="")
                for i in range(int(max_temperature)):
                    print("\x1b[91m+\x1b[00m", end="")
                print(f" {min_temperature}C - {max_temperature}C")

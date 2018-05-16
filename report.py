import datetime

class Report:
    
    @staticmethod
    def show_yearly_report (results):
        highest_temp = results["Highest Temperature"]["Max TemperatureC"]
        highest_temp_PKT = datetime.datetime.strptime(results["Highest Temperature"]["PKT"], "%Y-%m-%d").strftime("%B %d")
        lowest_temp = results["Lowest Temperature"]["Min TemperatureC"]
        lowest_temp_PKT = datetime.datetime.strptime(results["Lowest Temperature"]["PKT"], "%Y-%m-%d").strftime("%B %d")
        max_humidity = results["Max Humidity"]["Max Humidity"]
        max_humidity_PKT = datetime.datetime.strptime(results["Max Humidity"]["PKT"], "%Y-%m-%d").strftime("%B %d")
        print(f"Highest: {highest_temp}C on {highest_temp_PKT}")
        print(f"Lowest: {lowest_temp}C on {lowest_temp_PKT}")
        print(f"Most Humid Day: {max_humidity}% on {max_humidity_PKT}")

    @staticmethod
    def show_monthly_report (results):
        highest_average = results["Highest Average"]
        lowest_average = results["Lowest Average"]
        average_mean_humidity = results["Average Mean Humidity"]
        print(f"Highest Average: {highest_average}C")
        print(f"Lowest Average: {lowest_average}C")
        print(f"Average Mean Humidity: {average_mean_humidity}%")

    @staticmethod
    def show_chart_report(readings):
        print(datetime.datetime.strptime(readings[0]["PKT"], "%Y-%m-%d").strftime("%B %Y"))
        for reading in readings:
            max_temperature = reading["Max TemperatureC"]
            min_temperature = reading["Min TemperatureC"]
            date = reading["PKT"].split('-')[2]

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
        print(datetime.datetime.strptime(readings[0]["PKT"], "%Y-%m-%d").strftime("%B %Y"))
        
        for reading in readings:
            max_temperature = reading["Max TemperatureC"]
            min_temperature = reading["Min TemperatureC"]
            date = reading["PKT"].split('-')[2]
            if max_temperature and min_temperature:
                print(f"{date} " , end="")
                for i in range(int(min_temperature)):
                    print("\x1b[34m+\x1b[00m", end="")
                for i in range(int(max_temperature)):
                    print("\x1b[91m+\x1b[00m", end="")
                print(f" {min_temperature}C - {max_temperature}C")

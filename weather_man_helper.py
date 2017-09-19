import enum
import csv
from dateutil import parser


class ReportType(enum.Enum):
    YEAR, YEAR_MONTH, TWO_BAR_CHART = range(1,4)


class ChartType(enum.Enum):
    ONE_LINE, TWO_LINE = range(1,3)


class Weather:
    max_temp = 0
    min_temp = 0
    max_humidity = 0
    mean_humidity = 0
    date = ""


class WeatherManFileParser:

    def __init__(self):
        self.__weather_readings = list()

    def read_weather_values(self, line):
        if line["Max TemperatureC"] and line["Min TemperatureC"] and line["Max Humidity"] and line["Mean Humidity"]:
            weather = Weather()
            weather.date = line.get("PKT", line.get("PKST"))
            weather.max_temp = float(line["Max TemperatureC"])
            weather.min_temp = float(line["Min TemperatureC"])
            weather.max_humidity = float(line["Max Humidity"])
            weather.mean_humidity = float(line["Mean Humidity"])
            self.__weather_readings.append(weather)

    def read_weather_file(self, weather_file):

        with open(weather_file, 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for line in reader:
                self.read_weather_values(line)

    def populate_weather_readings(self, weather_files):
        for weather_file in weather_files:
            self.read_weather_file(weather_file)
        return self.__weather_readings


class WeatherManResultCalculator:

    def __init__(self):
        self.__results = dict()

    def calculate_highest_temperature(self, readings):
        high_temp_reading = max(readings, key=lambda x: x.max_temp)
        return high_temp_reading

    def calculate_lowest_temperature(self, readings):
        low_temp_reading = min(readings, key=lambda x: x.min_temp)
        return low_temp_reading

    def calculate_highest_humidity(self, readings):
        high_humid_reading = max(readings, key=lambda x: x.max_humidity)
        return high_humid_reading

    def calculate_average_high_temp(self, readings):
        temp_sum = sum(c.max_temp for c in readings)
        temp_length = len(readings)
        avg_temp = round(temp_sum/temp_length)
        return avg_temp

    def calculate_average_low_temp(self, readings):
        temp_sum = sum(c.min_temp for c in readings)
        temp_length = len(readings)
        avg_temp = round(temp_sum / temp_length)
        return avg_temp

    def calculate_average_mean_humidity(self, readings):
        humid_sum = sum(c.mean_humidity for c in readings)
        humid_length = len(readings)
        avg_humid = round(humid_sum / humid_length)
        return avg_humid

    def compute_result(self, weather_readings, result_type):

        if result_type == ReportType.YEAR:
            self.__results["Highest"] = self.calculate_highest_temperature(weather_readings)
            self.__results["Humidity"] = self.calculate_highest_humidity(weather_readings)
            self.__results["Lowest"] = self.calculate_lowest_temperature(weather_readings)

        elif result_type == ReportType.YEAR_MONTH:
            self.__results["Highest Average"] = self.calculate_average_high_temp(weather_readings)
            self.__results["Lowest Average"] = self.calculate_average_low_temp(weather_readings)
            self.__results["Average Mean Humidity"] = self.calculate_average_mean_humidity(weather_readings)

        else:
            self.__results = weather_readings

        return self.__results

    def __del__(self):
        self.__results.clear()


class WeatherManReportGenerator:

    BLACK = "\033[1;30m"
    BLUE = "\033[1;34m"
    PINK = "\033[1;35m"
    RED = "\033[1;31m"

    def draw_chart(self, temperature_readings, chart_type):

        for temperature in temperature_readings:

            day = temperature.date.split('-')[2]

            high_temp_point = round(abs(temperature.max_temp))
            high_temp_value = str(round(temperature.max_temp))

            low_temp_point = round(abs(temperature.min_temp))
            low_temp_value = str(round(temperature.min_temp))

            high_temp_line = self.RED + "" + "+" * high_temp_point
            low_temp_line = self.BLUE + "" + "+" * low_temp_point

            if chart_type == ChartType.TWO_LINE:

                print(self.PINK + day + " " + high_temp_line + self.PINK + " " + high_temp_value + "C")
                print(self.PINK + day + " " + low_temp_line + self.PINK + " " + low_temp_value + "C")

            else:
                print(self.PINK + day + " " + low_temp_line + high_temp_line + " "
                      + self.PINK + low_temp_value + "C" + "-" + high_temp_value + "C")

    def populate_year_report(self, weather_man_results):

        max_temp = weather_man_results["Highest"]
        min_temp = weather_man_results["Lowest"]
        max_humid = weather_man_results["Humidity"]

        print("Highest: "+str(max_temp.max_temp)+"C on "+ parser.parse(max_temp.date).strftime("%b %d"))
        print("Lowest: " + str(min_temp.min_temp) + "C on " + parser.parse(min_temp.date).strftime("%b %d"))
        print("Humidity: " + str(max_humid.max_humidity) + "% on " + parser.parse(max_humid.date).strftime("%b %d"))

    def populate_year_month_report(self, weather_man_results):
        avg_highest_temp = weather_man_results["Highest Average"]
        avg_lowest_temp = weather_man_results["Lowest Average"]
        avg_mean_humid = weather_man_results["Average Mean Humidity"]

        print("Highest Average: "+str(avg_highest_temp)+"C")
        print("Lowest Average: " + str(avg_lowest_temp) + "C")
        print("Average Mean Humidity: " + str(avg_mean_humid) + "%")

    def populate_bar_chart_report(self, temperature_readings, year, month):

        print("\nTwo Line Bar Chart:-\n")
        print(month + " " + year)

        self.draw_chart(temperature_readings,ChartType.TWO_LINE)

        print("\nSingle Line Bar Chart:-\n\n")
        print(month + " " + year)

        self.draw_chart(temperature_readings, ChartType.ONE_LINE)

    def generate_report(self, weather_man_results, report_type, year="", month=""):

        if report_type == ReportType.TWO_BAR_CHART:
            print("\n\n")
            self.populate_bar_chart_report(weather_man_results, year, month)
        elif report_type == ReportType.YEAR:
            print("\n\n")
            self.populate_year_report(weather_man_results)
        else:
            print("\n\n")
            self.populate_year_month_report(weather_man_results)





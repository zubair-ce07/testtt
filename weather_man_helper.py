import sys
import enum
import csv
from datetime import datetime
from collections import OrderedDict


class ReportType(enum.Enum):

    Year, YearMonth, TwoBarCharts = range(1, 4)


class WeatherManFileParser:
    """
    WeatherManFileParser takes the weather files and read values of specific parameters/filters provided.

    """

    def __init__(self):
        self.__weather_readings = list()
        self.__weather_reading_filters = [
            "Max TemperatureC",
            "Min TemperatureC",
            "Max Humidity",
            "Mean Humidity"
        ]

    def read_weather_man_file(self, weather_file):

        with open(weather_file, 'r') as file:
            reader = csv.DictReader(file)
            for line in reader:
                self.__weather_readings.append(line)

    def populate_weather_man_readings(self, weather_files):

        for weather_file in weather_files:
            self.read_weather_man_file(weather_file)
        return self.__weather_readings

    def __del__(self):
        self.__weather_readings.clear()  # clear readings data on readings fetched
        self.__weather_reading_filters.clear()  # clear filters when readings fetched


class WeatherManResultCalculator:
    """
    WeatherManResultCalculator handles calculation performs on weather readings
    """

    def __init__(self):
        self.__results = OrderedDict()

    def read_filtered_weather_readings(self, weather_readings, reading_filter):
        filtered_readings = OrderedDict()
        filtered_reading_values = list()
        filtered_reading_parameters = list()

        for weather_reading in weather_readings:
            filtered_reading_parameters.append(weather_reading["PKT"])
            value = weather_reading.get(""+reading_filter+"", 0.0)
            filtered_reading_values.append(float(value) if value else 0.0)

        filtered_readings = OrderedDict(zip(filtered_reading_parameters,filtered_reading_values))
        return filtered_readings

    def calculate_highest_reading(self, readings, reading_filter):

        reading_values = list(readings.values())
        reading_dates = list(readings.keys())

        max_reading_value = max(reading_values)

        reading_date = reading_dates[reading_values.index(max_reading_value)]

        reading_day = datetime(year=int(reading_date.split('-')[0]), month=int(reading_date.split('-')[1]),
                               day=int(reading_date.split('-')[2]))
        if reading_filter == "Temperature":
            max_reading_value_with_day = str(round(max_reading_value)) + "C on " + reading_day.strftime("%b %d")
        elif reading_filter == "Humidity":
            max_reading_value_with_day = str(round(max_reading_value)) + "% on " + reading_day.strftime("%b %d")
        else:
            max_reading_value_with_day = str(round(max_reading_value)) + reading_day.strftime("%b %d")

        return max_reading_value_with_day

    def calculate_lowest_reading(self, min_readings, reading_filter):
        """
        calculate_lowest_reading calculates lowest reading value based on provided filter
        :param min_readings:
        :param reading_filter:
        :return:
        """

        reading_values = list(min_readings.values())
        reading_dates = list(min_readings.keys())

        min_reading_value = min(reading_values)

        reading_date = reading_dates[reading_values.index(min_reading_value)]

        reading_day = datetime(year=int(reading_date.split('-')[0]), month=int(reading_date.split('-')[1]),
                               day=int(reading_date.split('-')[2]))

        if reading_filter == "Temperature":
            min_reading_value_with_day = str(round(min_reading_value)) + "C on " + reading_day.strftime("%b %d")
        elif reading_filter == "Humidity":
            min_reading_value_with_day = str(round(min_reading_value)) + "% on " + reading_day.strftime("%b %d")
        else:
            min_reading_value_with_day = str(round(min_reading_value)) + reading_day.strftime("%b %d")

        return min_reading_value_with_day

    def calculate_weather_readings_average(self, readings, reading_filter):
        """
        calculate_weather_readings_average calculates average reading value based on provided filter
        :param readings:
        :param reading_filter:
        :return:
        """

        reading_values = list(readings.values())
        average_of_reading = sum(reading_values)/float(len(reading_values))
        if reading_filter == "Temperature":
            average_of_reading = str(round(average_of_reading))+"C"
        elif reading_filter == "Humidity":
            average_of_reading = str(round(average_of_reading))+"%"
        else:
            average_of_reading = str(round(average_of_reading))
        return average_of_reading

    def compute_result(self, weather_readings, result_type):
        """
        compute_result compute provided types of result of weather readings
        :param weather_readings:
        :param result_type:
        :return:
        """

        if result_type == ReportType.Year:
            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Max TemperatureC")
            max_temp_with_day = self.calculate_highest_reading(filtered_readings, "Temperature")

            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Min TemperatureC")
            min_temp_with_day = self.calculate_lowest_reading(filtered_readings, "Temperature")

            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Max Humidity")
            max_humidity_with_day = self.calculate_highest_reading(filtered_readings, "Humidity")

            self.__results["Highest"] = max_temp_with_day
            self.__results["Lowest"] = min_temp_with_day
            self.__results["Humidity"] = max_humidity_with_day

        elif result_type == ReportType.YearMonth:
            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Max TemperatureC")
            highest_average = self.calculate_weather_readings_average(filtered_readings, "Temperature")

            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Min TemperatureC")
            lowest_average = self.calculate_weather_readings_average(filtered_readings, "Temperature")

            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Mean Humidity")
            average_mean_humidity = self.calculate_weather_readings_average(filtered_readings, "Humidity")

            self.__results["Highest Average"] = highest_average
            self.__results["Lowest Average"] = lowest_average
            self.__results["Average Mean Humidity"] = average_mean_humidity

        else:
            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Max TemperatureC")
            highest_temperature_with_day = filtered_readings

            filtered_readings = self.read_filtered_weather_readings(weather_readings, "Min TemperatureC")
            lowest_temperature_with_day = filtered_readings

            self.__results["Highest Temperature Each Day"] = highest_temperature_with_day
            self.__results["Lowest Temperature Each Day"] = lowest_temperature_with_day

        return self.__results

    def __del__(self):
        self.__results.clear()


class WeatherManReportGenerator:
    """
    WeatherManReportGenerator manage and populate reports based on weather readings
    """

    def populate_report(self, weather_man_results):
        """
        populate_report takes weather readings result and populate it's report to the user
        :param weather_man_results:
        :return:
        """

        for reading_parameter, reading_value in weather_man_results.items():
            print(reading_parameter + ": " + reading_value)


    def populate_bar_chart_report(self, weather_man_results, year, month):
        """
        populate_bar_chart_report takes weather readings result and populate it's bar chart report to the user

        :param weather_man_results:
        :param year:
        :param month:
        :return:
        """

        weather_man_low_temperature = weather_man_results.popitem()
        weather_man_high_temperature = weather_man_results.popitem()
        print(month + " " + year)
        for key, value in weather_man_high_temperature[1].items():
            print("\033[1;35m" + key.split('-')[2] + "\033[1;31m" + " " + "+" * round(
                weather_man_high_temperature[1][key]) + "\033[1;35m" + " " + str(
                round(weather_man_high_temperature[1][key])) + "C")
            print("\033[1;35m" + key.split('-')[2] + "\033[1;34m" + " " + "+" * round(
                weather_man_low_temperature[1][key]) + "\033[1;35m" + " " + str(
                round(weather_man_low_temperature[1][key])) + "C")
        # reset color
        sys.stdout.write("\033[1;30m")  # black color
        print("\n\n\nBonus Task:-\n\n")
        # Bonus task
        print(month + " " + year)
        for key, value in weather_man_high_temperature[1].items():
            sys.stdout.write("\033[1;35m" + key.split('-')[2] + "\033[1;34m" + " " + "+" * round(
                weather_man_low_temperature[1][key]) + "\033[1;31m" + (
                             "+" * round(weather_man_high_temperature[1][key])) + " " +
                             "\033[1;35m" + str(round(weather_man_low_temperature[1][key])) + "C" + "-" +
                             str(round(weather_man_high_temperature[1][key])) + "C" + "\n")  # red color

        # reset color
        sys.stdout.write("\033[1;30m")  # black color

    def generate_report(self, weather_man_results, report_type, year="", month=""):
        """
        generate_report generate report for weather readings
        and give generate report to appropriate populate method to show report

        :param weather_man_results:
        :param report_type:
        :param year:
        :param month:
        :return:
        """

        if report_type == ReportType.TwoBarCharts:
            print("\n\n")
            self.populate_bar_chart_report(weather_man_results, year, month)
        else:
            print("\n\n")
            self.populate_report(weather_man_results)

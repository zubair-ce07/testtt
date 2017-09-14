import sys
import enum
from collections import OrderedDict
from datetime import datetime


class ReportType(enum.Enum):
    """

    """
    Year = 1
    YearMonth = 2
    TwoBarCharts = 3


class WeatherManFileParser:
    """

    """

    def __init__(self):
        self.__weather_readings = OrderedDict()

    def populate_weather_readings(self,weather_files):
        """

        :param weather_files:
        :return:
        """
        for weather_file in weather_files:
            reading_columns = []
            readings = []
            weather_reading = OrderedDict()
            with open(weather_file,'r') as f:
                for line in f:

                    current_weather_reading=line.split(",")

                    if current_weather_reading and (not reading_columns):  # clm name in file, serve as key in code
                        reading_columns = current_weather_reading
                    else:
                        readings.append(current_weather_reading)

                for key_index in range(0, reading_columns.__len__()):
                    for value_row_index in range(0, readings.__len__()):
                        for value_clm_index in range(key_index, key_index+1):
                            if reading_columns[key_index].strip() == "Max TemperatureC"\
                                    or reading_columns[key_index].strip() == "Min TemperatureC"\
                                    or reading_columns[key_index].strip() == "Max Humidity"\
                                    or reading_columns[key_index].strip() == "Mean Humidity":

                                    if reading_columns[key_index] in self.__weather_readings:
                                        try:
                                            weather_reading[readings[value_row_index][0]] = float(readings[value_row_index][value_clm_index])

                                            self.__weather_readings[reading_columns[key_index].strip()].append(weather_reading)
                                        except ValueError:
                                            weather_reading[readings[value_row_index][0]] = 0.0

                                            self.__weather_readings[reading_columns[key_index].strip()].append(weather_reading)
                                    else:
                                        try:
                                            weather_reading[readings[value_row_index][0]] = float(readings[value_row_index][value_clm_index])

                                            self.__weather_readings[reading_columns[key_index].strip()]=[weather_reading]
                                        except ValueError:
                                            weather_reading[readings[value_row_index][0]] = 0.0

                                            self.__weather_readings[reading_columns[key_index].strip()] = [weather_reading]

                                    weather_reading=OrderedDict()
        return self.__weather_readings

    def weather_man_readings(self):
        """

        :return:
        """
        return self.__weather_readings

    def __del__(self):
        self.__weather_readings.clear()


class WeatherManResultCalculator:
    """

    """

    def __init__(self):
        self.__results = OrderedDict()

    def read_filtered_weather_readings(self, weather_readings, reading_filter):
        """

        :param weather_readings:
        :param filter_:
        :return:
        :return:
        """
        filtered_readings = OrderedDict()
        for reading in weather_readings[""+reading_filter+""]:
            for reading_parameter, reading_value in reading.items():
                filtered_readings[reading_parameter] = reading_value
        return filtered_readings

    def calculate_highest_reading(self, max_readings, reading_filter):
        """

        :param max_readings:
        :param filter_:
        :return:
        """
        reading_values = list(max_readings.values())
        reading_dates = list(max_readings.keys())

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

        :param min_readings:
        :param filter_:
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

        :param readings:
        :param filter_:
        :return:
        """
        reading_values = list(readings.values())
        average_of_reading= sum(reading_values)/float(len(reading_values))
        if reading_filter == "Temperature":
            average_of_reading = str(round(average_of_reading))+"C"
        elif reading_filter == "Humidity":
            average_of_reading = str(round(average_of_reading))+"%"
        else:
            average_of_reading = str(round(average_of_reading))
        return average_of_reading

    def compute_result(self, weather_readings, result_type):
        """

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

    """

    def populate_report(self, weather_man_results):
        """

        :param weather_man_results:
        :return:
        """

        for reading_parameter, reading_value in weather_man_results.items():
            print(reading_parameter + ": " + reading_value)

    def populate_bar_chart_report(self, weather_man_results, year, month):
        """

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

        :param weather_man_results:
        :param report_type:
        :param year:
        :param month:
        :return:
        """

        if report_type == ReportType.TwoBarCharts:
            print("\n\n")
            self.populate_bar_chart_report(weather_man_results,year,month)
        else:
            print("\n\n")
            self.populate_report(weather_man_results)



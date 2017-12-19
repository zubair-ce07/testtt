import calendar
import argparse
from reports import WeatherReport
from populatedata import PopulateWeatherData
from operator import itemgetter
import constants


class WeatherCalculation():

    def __init__(self, weather_list, output_format, type_specifier):
        self.calculated_data = {}
        self.output_format = output_format
        self.list_of_weather_details = weather_list
        self.type_specifier = type_specifier

    def calculate_weather(self):
        if self.list_of_weather_details:
            if self.output_format == self.type_specifier["year"]:
                self.calculate_yearly_weather()
            elif self.output_format == self.type_specifier["chart"]:
                self.calculate_detailed_weather()
            else:
                self.calculate_monthly_weather()

    def calculate_monthly_weather(self):
        filtered_list = [int(weather_report[constants.MAX_TEMPERATURE])
                         for weather_report in self.list_of_weather_details
                         if constants.MAX_TEMPERATURE in weather_report
                            and weather_report[constants.MAX_TEMPERATURE] != None]
        if filtered_list:
            self.calculated_data[constants.AVERAGE_MAX_TEMPERATURE] = sum(filtered_list) / len(filtered_list)

        else:
            self.calculated_data[constants.AVERAGE_MAX_TEMPERATURE] = 0

        filtered_list = [int(weather_report[constants.MIN_TEMPERATURE])
                         for weather_report in self.list_of_weather_details
                         if constants.MIN_TEMPERATURE in weather_report
                            and weather_report[constants.MIN_TEMPERATURE] != None]
        if filtered_list:
            self.calculated_data[constants.AVERAGE_MIN_TEMPERATURE] = sum(filtered_list) / len(filtered_list)

        else:
            self.calculated_data[constants.AVERAGE_MIN_TEMPERATURE] = 0

        filtered_list = [int(weather_report[constants.MEAN_HUMIDITY])
                         for weather_report in self.list_of_weather_details
                         if constants.MEAN_HUMIDITY in weather_report
                            and weather_report[constants.MEAN_HUMIDITY] != None]
        if filtered_list:
            self.calculated_data[constants.AVERAGE_MEAN_HUMIDITY] = sum(filtered_list) / len(filtered_list)

        else:
            self.calculated_data[constants.AVERAGE_MEAN_HUMIDITY] = 0

    def calculate_detailed_weather(self):
        filtered_list = [weather_report[constants.MAX_TEMPERATURE]
                         for weather_report in self.list_of_weather_details
                         if constants.MAX_TEMPERATURE in weather_report]

        filtered_list = ['0' if max_temp is None else max_temp for max_temp in filtered_list]
        integer_list = list(map(int, filtered_list))

        if integer_list:
            self.calculated_data[constants.MAX_TEMPERATURE_LIST] = integer_list
        else:
            self.calculated_data[constants.MAX_TEMPERATURE_LIST] = []

        filtered_list = [weather_report[constants.MIN_TEMPERATURE]
                         for weather_report in self.list_of_weather_details
                         if constants.MIN_TEMPERATURE in weather_report]

        filtered_list = ['0' if min_temp is None else min_temp for min_temp in filtered_list]
        integer_list = list(map(int, filtered_list))

        if integer_list:
            self.calculated_data[constants.MIN_TEMPERATURE_LIST] = integer_list
        else:
            self.calculated_data[constants.MIN_TEMPERATURE_LIST] = []

    def calculate_yearly_weather(self):
        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if constants.MAX_TEMPERATURE in weather_report
                            and weather_report[constants.MAX_TEMPERATURE] != None]
        if filtered_list:
            selected_dictionary = max(filtered_list, key=itemgetter(constants.MAX_TEMPERATURE))
            self.calculated_data[constants.MAX_TEMPERATURE] = int(selected_dictionary[constants.MAX_TEMPERATURE])
            self.calculated_data[constants.MAX_TEMPERATURE_DATE] = selected_dictionary[constants.PKT]
        else:
            self.calculated_data[constants.MAX_TEMPERATURE] = 0
            self.calculated_data[constants.MAX_TEMPERATURE_DATE] = "0"

        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if constants.MIN_TEMPERATURE in weather_report
                            and weather_report[constants.MIN_TEMPERATURE] != None]
        if filtered_list:
            selected_dictionary = min(filtered_list, key=itemgetter(constants.MIN_TEMPERATURE))
            self.calculated_data[constants.MIN_TEMPERATURE] = int(selected_dictionary[constants.MIN_TEMPERATURE])
            self.calculated_data[constants.MIN_TEMPERATURE_DATE] = selected_dictionary[constants.PKT]
        else:
            self.calculated_data[constants.MIN_TEMPERATURE] = 0
            self.calculated_data[constants.MIN_TEMPERATURE_DATE] = "0"

        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if constants.MAX_HUMIDITY in weather_report
                            and weather_report[constants.MAX_HUMIDITY] != None]
        if filtered_list:
            selected_dictionary = max(filtered_list, key=itemgetter(constants.MAX_HUMIDITY))
            self.calculated_data[constants.MAX_HUMIDITY] = int(selected_dictionary[constants.MAX_HUMIDITY])
            self.calculated_data[constants.MAX_HUMIDITY_DATE] = selected_dictionary[constants.PKT]
        else:
            self.calculated_data[constants.MAX_HUMIDITY] = 0
            self.calculated_data[constants.MAX_HUMIDITY_DATE] = "0"


class ComputeWeather:

    def __init__(self, args):
        self.args = args
        self.type_specifier = {"year": "-e", "month": "-a", "chart": "-c"}

    def calculate_and_print(self, directory_path, output_format, year, month = "*"):
        populate_data = PopulateWeatherData(directory_path, year, month)
        populate_data.populate()

        calculate_data = WeatherCalculation(populate_data.list_of_weather_details, output_format, self.type_specifier)
        calculate_data.calculate_weather()

        print_report = WeatherReport(calculate_data.calculated_data, output_format, self.type_specifier)
        print_report.print_report()

    def compute(self):
        if self.args.year:
            year = self.args.year
            self.calculate_and_print(self.args.directory_path, self.type_specifier["year"], year)

        if self.args.month:
            input = str(self.args.month).split('/')
            year = input[0]
            month = int(input[1])

            if not month < 1 or month > 12:
                month = calendar.month_abbr[int(input[1])]
                self.calculate_and_print(self.args.directory_path, self.type_specifier["month"], year, month)

        if self.args.chart:
            input = str(self.args.chart).split('/')
            year = input[0]
            month = int(input[1])

            if not month < 1 or month > 12:
                month = calendar.month_abbr[int(input[1])]
                self.calculate_and_print(self.args.directory_path, self.type_specifier["chart"], year, month)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("directory_path", type=str, help="Directory path of weather files")
    parser.add_argument("-e", "--year", help="input year value only")
    parser.add_argument("-a", "--month", help="input year and month value only")
    parser.add_argument("-c", "--chart", help="input year and month value to display charts representation")
    args = parser.parse_args()

    compute_args = ComputeWeather(args)
    compute_args.compute()

if __name__ == "__main__":
    main()
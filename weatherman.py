import calendar
import argparse
from reports import WeatherReport
from populatedata import PopulateWeatherData
from operator import itemgetter


class WeatherCalculation():

    MAX_TEMPERATURE = "Max TemperatureC"
    MIN_TEMPERATURE = "Min TemperatureC"
    MEAN_HUMIDITY = " Mean Humidity"
    MAX_HUMIDITY = "Max Humidity"
    PKT = "PKT"
    AVERAGE_MAX_TEMPERATURE = "Avg_Max_Temp"
    AVERAGE_MIN_TEMPERATURE = "Avg_Min_Temp"
    AVERAGE_MEAN_HUMIDITY = "Avg_Mean_Temp"
    MAX_TEMPERATURE_LIST = "Max_Temp_List"
    MIN_TEMPERATURE_LIST = "Min_Temp_List"
    MAX_TEMPERATURE_DATE = "Max_Temp_Date"
    MIN_TEMPERATURE_DATE = "Min_Temp_Date"
    MAX_HUMIDITY_DATE = "Mean_Humidity_Date"

    def __init__(self, weather_list, type, type_specifier):
        self.calculated_data = {}
        self.output_type = type
        self.list_of_weather_details = weather_list
        self.type_specifier = type_specifier

    # Calculates the weather details according to the type specified.
    def calculate_weather(self):

        if self.list_of_weather_details:
            if self.output_type == self.type_specifier["year"]:
                self.calculate_yearly_weather()
            elif self.output_type == self.type_specifier["chart"]:
                self.calculate_detailed_weather()
            else:
                self.calculate_monthly_weather()

    # Calculates average min, max, and mean monthly temperature.
    def calculate_monthly_weather(self):

        filtered_list = [int(weather_report[WeatherCalculation.MAX_TEMPERATURE]) for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MAX_TEMPERATURE in weather_report and weather_report[WeatherCalculation.MAX_TEMPERATURE] != None]
        try:
            self.calculated_data[WeatherCalculation.AVERAGE_MAX_TEMPERATURE] = sum(filtered_list) / len(filtered_list)

        except ZeroDivisionError:
            self.calculated_data[WeatherCalculation.AVERAGE_MAX_TEMPERATURE] = 0

        filtered_list = [int(weather_report[WeatherCalculation.MIN_TEMPERATURE]) for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MIN_TEMPERATURE in weather_report and weather_report[WeatherCalculation.MIN_TEMPERATURE] != None]
        try:
            self.calculated_data[WeatherCalculation.AVERAGE_MIN_TEMPERATURE] = sum(filtered_list) / len(filtered_list)

        except ZeroDivisionError:
            self.calculated_data[WeatherCalculation.AVERAGE_MIN_TEMPERATURE] = 0

        filtered_list = [int(weather_report[WeatherCalculation.MEAN_HUMIDITY]) for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MEAN_HUMIDITY in weather_report and weather_report[WeatherCalculation.MEAN_HUMIDITY] != None]
        try:
            self.calculated_data[WeatherCalculation.AVERAGE_MEAN_HUMIDITY] = sum(filtered_list) / len(filtered_list)

        except ZeroDivisionError:
            self.calculated_data[WeatherCalculation.AVERAGE_MEAN_HUMIDITY] = 0

    # Calculates min and max of every day of a month.
    def calculate_detailed_weather(self):
        filtered_list = [weather_report[WeatherCalculation.MAX_TEMPERATURE] for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MAX_TEMPERATURE in weather_report]
        filtered_list = ['0' if max_temp is None else max_temp for max_temp in filtered_list]
        integer_list = list(map(int, filtered_list))

        if integer_list:
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE_LIST] = integer_list
        else:
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE_LIST] = []
        filtered_list = [weather_report[WeatherCalculation.MIN_TEMPERATURE] for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MIN_TEMPERATURE in weather_report]
        filtered_list = ['0' if min_temp is None else min_temp for min_temp in filtered_list]
        integer_list = list(map(int, filtered_list))

        if integer_list:
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE_LIST] = integer_list
        else:
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE_LIST] = []

    # Calculates min, max, and mean of a day in specified year.
    def calculate_yearly_weather(self):

        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MAX_TEMPERATURE in weather_report and weather_report[WeatherCalculation.MAX_TEMPERATURE] != None]
        if filtered_list:
            selected_dictionary = max(filtered_list, key=itemgetter(WeatherCalculation.MAX_TEMPERATURE))
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE] = int(selected_dictionary[WeatherCalculation.MAX_TEMPERATURE])
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE_DATE] = selected_dictionary[WeatherCalculation.PKT]
        else:
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE] = 0
            self.calculated_data[WeatherCalculation.MAX_TEMPERATURE_DATE] = "0"

        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MIN_TEMPERATURE in weather_report and weather_report[WeatherCalculation.MIN_TEMPERATURE] != None]
        if filtered_list:
            selected_dictionary = min(filtered_list, key=itemgetter(WeatherCalculation.MIN_TEMPERATURE))
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE] = int(selected_dictionary[WeatherCalculation.MIN_TEMPERATURE])
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE_DATE] = selected_dictionary[WeatherCalculation.PKT]
        else:
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE] = 0
            self.calculated_data[WeatherCalculation.MIN_TEMPERATURE_DATE] = "0"

        filtered_list = [weather_report for weather_report in self.list_of_weather_details
                         if WeatherCalculation.MAX_HUMIDITY in weather_report and weather_report[WeatherCalculation.MAX_HUMIDITY] != None]
        if filtered_list:
            selected_dictionary = max(filtered_list, key=itemgetter(WeatherCalculation.MAX_HUMIDITY))
            self.calculated_data[WeatherCalculation.MAX_HUMIDITY] = int(selected_dictionary[WeatherCalculation.MAX_HUMIDITY])
            self.calculated_data[WeatherCalculation.MAX_HUMIDITY_DATE] = selected_dictionary[WeatherCalculation.PKT]
        else:
            self.calculated_data[WeatherCalculation.MAX_HUMIDITY] = 0
            self.calculated_data[WeatherCalculation.MAX_HUMIDITY_DATE] = "0"


class ComputeWeather:

    def __init__(self, args):
        self.args = args
        self.type_specifier = {"year": "-e", "month": "-a", "chart": "-c"}

    # Populates weather data from files and calculates temperatures according to specified type
    def calculate_and_print(self, directory_path, type, year, month = "*"):

        populate_data = PopulateWeatherData(directory_path, year, month)
        populate_data.populate()

        calculate_data = WeatherCalculation(populate_data.list_of_weather_details, type, self.type_specifier)
        calculate_data.calculate_weather()

        print_report = WeatherReport(calculate_data.calculated_data, type, self.type_specifier)
        print_report.print_report()

    # This method reads the command arguments and perform calculations
    def compute(self):
        if self.args.year:
            year = self.args.year
            self.calculate_and_print(self.args.directory_path, self.type_specifier["year"], year)

        if self.args.month:
            input = str(self.args.month).split('/')
            year = input[0]
            month = int(input[1])

            try:
                if month < 1 or month > 12:
                    raise ValueError
                else:
                    month = calendar.month_abbr[int(input[1])]
                    self.calculate_and_print(self.args.directory_path, self.type_specifier["month"], year, month)
            except ValueError:
                print("{} is not a month".format(input[1]))

        if self.args.chart:
            input = str(self.args.chart).split('/')
            year = input[0]
            month = int(input[1])

            try:
                if month < 1 or month > 12:
                    raise ValueError
                else:
                    month = calendar.month_abbr[int(input[1])]
                    self.calculate_and_print(self.args.directory_path, self.type_specifier["chart"], year, month)

            except ValueError:
                print("{} is not a month".format(input[1]))


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
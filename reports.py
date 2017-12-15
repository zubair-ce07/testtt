import datetime


class WeatherReport:

    AVERAGE_MAX_TEMPERATURE = "Avg_Max_Temp"
    AVERAGE_MIN_TEMPERATURE = "Avg_Min_Temp"
    AVERAGE_MEAN_HUMIDITY = "Avg_Mean_Temp"
    MAX_TEMPERATURE_LIST = "Max_Temp_List"
    MIN_TEMPERATURE_LIST = "Min_Temp_List"
    MAX_TEMPERATURE_DATE = "Max_Temp_Date"
    MIN_TEMPERATURE_DATE = "Min_Temp_Date"
    MAX_HUMIDITY_DATE = "Mean_Humidity_Date"
    MAX_TEMPERATURE = "Max TemperatureC"
    MIN_TEMPERATURE = "Min TemperatureC"
    MAX_HUMIDITY = "Max Humidity"

    def __init__(self, calculated_weather_values, type, type_specifier):
        self.calculated_weather_values = calculated_weather_values
        self.output_type = type
        self.type_specifier = type_specifier

    # Converts and returns the integer value of day, month, and year in datetime format
    def getDate(self, date):
        date_str = str(date).split('-')
        return datetime.datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    # Prints out weather details according to specified type.
    def print_report(self):

        if self.calculated_weather_values:

            if self.output_type == self.type_specifier["year"]:
                weather_date = self.getDate(self.calculated_weather_values[WeatherReport.MAX_TEMPERATURE_DATE])
                print("\nHighest: %sC on %s" % (self.calculated_weather_values[WeatherReport.MAX_TEMPERATURE],
                                                weather_date.strftime('%B %Y')))

                weather_date = self.getDate(self.calculated_weather_values[WeatherReport.MIN_TEMPERATURE_DATE])
                print("Lowest: %sC on %s" % (self.calculated_weather_values[WeatherReport.MIN_TEMPERATURE],
                                             weather_date.strftime('%B %Y')))

                weather_date = self.getDate(self.calculated_weather_values[WeatherReport.MAX_HUMIDITY_DATE])
                print("Humidity: %s%% on %s" % (self.calculated_weather_values[WeatherReport.MAX_HUMIDITY],
                                                weather_date.strftime('%B %Y')))
            elif self.output_type == self.type_specifier["chart"]:

                max_temp_list = self.calculated_weather_values[WeatherReport.MAX_TEMPERATURE_LIST]
                min_temp_list = self.calculated_weather_values[WeatherReport.MIN_TEMPERATURE_LIST]
                if max_temp_list and min_temp_list:
                    count = 0
                    print("\n")
                    for value in min_temp_list:
                        print("%02d" % (count + 1), end=" ")
                        print("\033[0;36;2m+" * value, end="")
                        print("\033[0;31;2m+" * max_temp_list[count], end="")
                        print("\033[0;30;2m {}C - {}C".format(value, max_temp_list[count]))
                        count += 1
            else:
                print("\nHighest Average: %dC" % self.calculated_weather_values[WeatherReport.AVERAGE_MAX_TEMPERATURE])
                print("Lowest Average: %dC" % self.calculated_weather_values[WeatherReport.AVERAGE_MIN_TEMPERATURE])
                print("Average Mean Humidity: %d%%" % self.calculated_weather_values[WeatherReport.AVERAGE_MEAN_HUMIDITY])
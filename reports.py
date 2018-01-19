import datetime
import constants


class WeatherReport:

    def __init__(self, calculated_weather_values, output_format, type_specifier):
        self.calculated_weather_values = calculated_weather_values
        self.output_format = output_format
        self.type_specifier = type_specifier

    def getDate(self, date):
        date_str = str(date).split('-')
        return datetime.datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    def print_report(self):
        if self.calculated_weather_values:
            if self.output_format == self.type_specifier["year"]:
                weather_date = self.getDate(self.calculated_weather_values[constants.MAX_TEMPERATURE_DATE])
                print("\nHighest: {}C on {}".format(self.calculated_weather_values[constants.MAX_TEMPERATURE],
                                                weather_date.strftime('%B %Y')))

                weather_date = self.getDate(self.calculated_weather_values[constants.MIN_TEMPERATURE_DATE])
                print("Lowest: {}C on {}".format(self.calculated_weather_values[constants.MIN_TEMPERATURE],
                                             weather_date.strftime('%B %Y')))

                weather_date = self.getDate(self.calculated_weather_values[constants.MAX_HUMIDITY_DATE])
                print("Humidity: {}% on {}".format(self.calculated_weather_values[constants.MAX_HUMIDITY],
                                                weather_date.strftime('%B %Y')))

            elif self.output_format == self.type_specifier["chart"]:
                max_temp_list = self.calculated_weather_values[constants.MAX_TEMPERATURE_LIST]
                min_temp_list = self.calculated_weather_values[constants.MIN_TEMPERATURE_LIST]
                if max_temp_list and min_temp_list:
                    count = 0
                    print("\n")
                    for value in min_temp_list:
                        print("{:02d}".format(count + 1), end=" ")
                        print("\033[0;36;2m+" * value, end="")
                        print("\033[0;31;2m+" * max_temp_list[count], end="")
                        print("\033[0;30;2m {}C - {}C".format(value, max_temp_list[count]))
                        count += 1
            else:
                print("\nHighest Average: {}C".format(int(self.calculated_weather_values[constants.AVERAGE_MAX_TEMPERATURE])))
                print("Lowest Average: {}C".format(int(self.calculated_weather_values[constants.AVERAGE_MIN_TEMPERATURE])))
                print("Average Mean Humidity: {}%".format(int(self.calculated_weather_values[constants.AVERAGE_MEAN_HUMIDITY])))
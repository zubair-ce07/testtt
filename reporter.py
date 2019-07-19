import calendar

class WeatherReporter():
    """Pretty prints weather information on the console"""

    def __init__(self):
        """Define ASCII terminal colors and list of full month names"""
        self.blue = '\033[94m'
        self.red = '\033[91m'
        self.white = '\033[00m'

    def report_year_extremes(self, highest_temperature_day, lowest_temperature_day, most_humid_day):
        """Print year extremes to the console"""
        report_hottest = "Highest: {}C on {} {}".format(
            highest_temperature_day.max_temperature,
            calendar.month_name[highest_temperature_day.date.month],
            highest_temperature_day.date.day)

        report_coldest = "Lowest: {}C on {} {}".format(
            lowest_temperature_day.min_temperature,
            calendar.month_name[lowest_temperature_day.date.month],
            lowest_temperature_day.date.day)

        report_humid = "Humidity: {}% on {} {}".format(
            most_humid_day.max_humidity,
            calendar.month_name[most_humid_day.date.month],
            most_humid_day.date.day)
        print(report_hottest, report_coldest,
              report_humid, sep="\n", end="\n\n")

    def report_month_averages(self, avg_highest_temperature, avg_lowest_temperature, avg_mean_humidity):
        """Print month averages to the console"""
        report_avg_highest_temp = "Highest Average: {}C".format(
            avg_highest_temperature)

        report_avg_lowest_temp = "Lowest Average: {}C".format(
            avg_lowest_temperature)

        report_avg_mean_humidity = "Average Mean Humidity: {}%".format(
            avg_mean_humidity)

        print(report_avg_highest_temp, report_avg_lowest_temp,
              report_avg_mean_humidity, sep="\n", end="\n\n")

    def report_month_temperatures(self, max_temperatures, min_temperatures, single_line=False):
        """Print bar chart for highest and lowest temperatures for a month. Optionally on a single line"""
        if len(max_temperatures) != len(min_temperatures):
            raise AttributeError(
                "Number of readings for max and min temperatures do not match.")
        for i in range(len(max_temperatures)):
            max_temp = max_temperatures[i]
            min_temp = min_temperatures[i]

            if single_line:
                report = "{:02d} {}{} {}C - {}C".format(i+1, self.__get_colored_plus(
                    max_temp, "red"), self.__get_colored_plus(min_temp, "blue"), max_temp, min_temp)
                print(report)
            else:
                report_max = "{:02d} {} {}C".format(
                    i+1, self.__get_colored_plus(max_temp, "red"), max_temp)
                report_min = "{:02d} {} {}C".format(
                    i+1, self.__get_colored_plus(min_temp, "blue"), min_temp)
                print(report_max, report_min, sep="\n")
        print("")

    def __get_colored_plus(self, times, color):
        """Print colored +++ to the console"""
        if color == "blue":
            xxx = self.blue
        elif color == "red":
            xxx = self.red
        xxx = xxx + "+" * times + self.white
        return xxx

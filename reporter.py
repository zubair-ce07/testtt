import calendar


class WeatherReporter():
    """Pretty prints weather information on the console"""

    BLUE = '\033[94M'
    RED = '\033[91M'
    WHITE = '\033[00m'

    def report_year_extremes(self, highest_temperature_day, lowest_temperature_day, most_humid_day):
        """Print year extremes to the console"""
        hottest_day_report = f"Highest: {highest_temperature_day.max_temperature}C" \
            f" on {calendar.month_name[highest_temperature_day.date.month]} " \
            f" {highest_temperature_day.date.day}"

        coldest_day_report = f"Lowest: {lowest_temperature_day.min_temperature}C" \
            f" on {calendar.month_name[lowest_temperature_day.date.month]}" \
            f" {lowest_temperature_day.date.day}"

        humid_day_report = f"Humidity: {most_humid_day.max_humidity}%" \
            f" on {calendar.month_name[most_humid_day.date.month]}" \
            f" {most_humid_day.date.day}"

        print(hottest_day_report, coldest_day_report,
              humid_day_report, sep="\n", end="\n\n")

    def report_month_averages(self, avg_highest_temperature, avg_lowest_temperature, avg_mean_humidity):
        """Print month averages to the console"""
        avg_highest_temp_report = f"Highest Average: {avg_highest_temperature}C"

        avg_lowest_temp_report = f"Lowest Average: {avg_lowest_temperature}C"

        avg_mean_humidity_report = f"Average Mean Humidity: {avg_mean_humidity}%"

        print(avg_highest_temp_report, avg_lowest_temp_report,
              avg_mean_humidity_report, sep="\n", end="\n\n")

    def report_month_temperatures(self, max_temperatures, min_temperatures, single_line=False):
        """Print bar chart for highest and lowest temperatures for a month. Optionally on a single line"""
        if len(max_temperatures) != len(min_temperatures):
            raise AttributeError(
                "Number of readings for max and min temperatures do not match.")
        for i in range(len(max_temperatures)):
            max_temp = max_temperatures[i]
            min_temp = min_temperatures[i]

            if single_line:
                report = f"{i+1:02d}" \
                    f" {self.__get_colored_plus(max_temp, self.RED)}" \
                    f"{self.__get_colored_plus(min_temp, self.BLUE)}" \
                    f" {max_temp}C - {min_temp}C"
                print(report)
            else:
                report_max = f"{i+1:02d}" \
                    f" {self.__get_colored_plus(max_temp, self.RED)}" \
                    f" {max_temp}C"
                report_min = f"{i+1:02d}" \
                    f" {self.__get_colored_plus(min_temp, self.BLUE)}" \
                    f" {min_temp}C"
                print(report_max, report_min, sep="\n")
        print("")

    def __get_colored_plus(self, times, color):
        """Print colored +++ to the console"""
        selected_color = f"{color}{'+' * times}{self.WHITE}"
        return selected_color

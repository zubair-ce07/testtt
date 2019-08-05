import calendar


class WeatherReporter:
    """Pretty prints weather information on the console"""
    _BLUE = '\033[94m'
    _RED = '\033[91m'
    _WHITE = '\033[00m'

    def report_year_extremes(self, max_temp_day, min_temp_day, most_humid_day):
        """Print year extremes to the console"""
        hottest_day_report = (
            f"Highest: {max_temp_day.max_temperature}C"
            f" on {calendar.month_name[max_temp_day.date.month]} "
            f" {max_temp_day.date.day}"
        )

        coldest_day_report = (
            f"Lowest: {min_temp_day.min_temperature}C"
            f" on {calendar.month_name[min_temp_day.date.month]}"
            f" {min_temp_day.date.day}"
        )

        humid_day_report = (
            f"Humidity: {most_humid_day.max_humidity}%"
            f" on {calendar.month_name[most_humid_day.date.month]}"
            f" {most_humid_day.date.day}"
        )

        print(hottest_day_report, coldest_day_report,
              humid_day_report, sep="\n", end="\n\n")

    def report_month_avgs(self, avg_max_temp, avg_min_temp, avg_mean_humidity):
        """Print month averages to the console"""
        avg_max_temp_report = f"Highest Average: {avg_max_temp}C"

        avg_min_temp_report = f"Lowest Average: {avg_min_temp}C"

        avg_mean_humidity_report = f"Average Mean Humidity: {avg_mean_humidity}%"

        print(avg_max_temp_report, avg_min_temp_report,
              avg_mean_humidity_report, sep="\n", end="\n\n")

    def report_month_temps(self, max_temps, min_temps, single_line=False):
        """
            Print bar chart for highest and lowest temperatures for a month
            Optionally on a single line
        """

        for day, (max_temp, min_temp) in enumerate(zip(max_temps, min_temps)):
            single_line_report = (
                f"{day+1:02d}"
                f" {self._get_colored_bar(max_temp, self._RED)}"
                f"{self._get_colored_bar(min_temp, self._BLUE)}"
                f" {max_temp}C - {min_temp}C"
            )

            dual_line_report = (
                f"{day+1:02d}"
                f" {self._get_colored_bar(max_temp, self._RED)}"
                f" {max_temp}C"
                f"\n{day+1:02d}"
                f" {self._get_colored_bar(min_temp, self._BLUE)}"
                f" {min_temp}C"
            )

            if single_line:
                print(single_line_report)
            else:
                print(dual_line_report)
        print("")

    def _get_colored_bar(self, bar_length, color):
        """Get colored bar (+++) of specified length"""
        return f"{color}{'+' * bar_length}{self._WHITE}"

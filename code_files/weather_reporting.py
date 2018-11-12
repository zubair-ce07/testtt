import calendar


class WeatherReporting:
    color_blue = "\033[0;34;48m"
    colour_default = "\033[0m"
    color_red = "\033[0;31;48m"

    def display_year_report(self, report):
        print(
            f"Highest: {report['highest']['max_temp']}C on"
            f" {calendar.month_name[report['highest']['pkt'].month]}"
            f" {report['highest']['pkt'].day}"
        )

        print(
            f"Lowest: {report['lowest']['min_temp']}C on"
            f" {calendar.month_name[report['lowest']['pkt'].month]}"
            f" {report['lowest']['pkt'].day}"
        )

        print(
            f"Humidity: {report['humidity']['max_humidity']}% on"
            f" {calendar.month_name[report['humidity']['pkt'].month]}"
            f" {report['humidity']['pkt'].day}"
        )
        print('-------------------------------------\n')

    def display_month_report(self, report):
        print(f"Highest Average: {report['average_max_temp']}C")

        print(f"Lowest Average: {report['average_min_temp']}C")

        print(f"Average Mean Humidity: {report['average_mean_humidity']}%")

        print('-------------------------------------\n')

    def display_month_bar_chart(self, month_record):
        for record in month_record:
            lowest_temp_bar = f"{self.color_blue}{'+'*abs(record['min_temp'])}{self.colour_default}"
            highest_temp_bar = f"{self.color_red}{'+'*abs(record['max_temp'])}{self.colour_default}"
            highest_temp = f"{record['max_temp']} C"
            lowest_temp = f"{record['min_temp']} C"

            print(record['pkt'].day, lowest_temp_bar,
                  highest_temp_bar, lowest_temp, highest_temp)

        print('-------------------------------------\n')

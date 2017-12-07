class bcolors:
    PURLPLE = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ITL = '\033[3m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Report:

    def print_yearly(self, yearly_weather):
        template = "Highest: {max_temp}C on {max_month} {max_date}\n"
        template += "Lowest: {min_temp}C on {min_month} {min_date}\n"
        template += "Humidity: {humidity}% on {humid_month} {humid_date}\n"

        hottest_day_information = yearly_weather.hottest_day_information()
        coolest_day_information = yearly_weather.coolest_day_information()
        humid_day_information = yearly_weather.most_humid_day_information()
        report = template.format(
            max_temp=hottest_day_information["temp"],
            max_month=hottest_day_information["month"],
            max_date=hottest_day_information["day"],
            min_temp=coolest_day_information["temp"],
            min_month=coolest_day_information["month"],
            min_date=coolest_day_information["day"],
            humidity=humid_day_information["humidity"],
            humid_month=coolest_day_information["month"],
            humid_date=coolest_day_information["day"],
        )

        print(report)

    def print_monthly(self, monthly_weather):
        report_template = "Highest Average: {max_temp:{prec}}C\n"
        report_template += "Lowest Average: {min_temp:{prec}}C\n"
        report_template += "Average Mean Humidity: {humidity:{prec}}%\n"

        max_average = monthly_weather.highest_average_temperature()
        min_average = monthly_weather.lowest_average_temperature()
        humidity = monthly_weather.average_mean_humidity()
        report = report_template.format(
            max_temp=max_average,
            min_temp=min_average,
            humidity=humidity,
            prec='.3'
        )
        print(report)

    def print_monthly_bar_graph(self, monthly_weather, year):
        print(f"{monthly_weather.month_name()} {year}")

        for weather in monthly_weather.daily_weathers:
            day = "{day:0>2} ".format(day=weather.day())
            print(bcolors.PURLPLE+day, end="")

            for _ in range(0, weather.lowest_temperature() or 0):
                print(bcolors.BLUE+"+", end="")

            for _ in range(0, weather.highest_temperature() or 0):
                print(bcolors.FAIL+"+", end="")
            min_temp = "{min_temp:0>2}C".format(
                min_temp=str(weather.lowest_temperature()))
            max_temp = "{max_temp:0>2}C".format(
                max_temp=str(weather.highest_temperature()))
            print(f"{bcolors.PURLPLE} {min_temp} - {max_temp}", end="\n")

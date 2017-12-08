class Bcolors:
    PURLPLE = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ITL = '\033[3m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def mean(nums):
    return sum(nums, 0.0) / len(nums)


class Report:
    @staticmethod
    def print_yearly(weather_list):
        template = "Highest: {max_temp}C on {max_month} {max_date}\n"
        template += "Lowest: {min_temp}C on {min_month} {min_date}\n"
        template += "Humidity: {humidity}% on {humid_month} {humid_date}\n"

        hottest_day_information = max(weather_list, key=lambda x: x.highest_temperature())
        coolest_day_information = min(weather_list, key=lambda x: x.lowest_temperature())
        humid_day_information = max(weather_list, key=lambda x: x.max_humidity())

        report = template.format(
            max_temp=hottest_day_information.highest_temperature(),
            max_month=hottest_day_information.month_name(),
            max_date=hottest_day_information.day(),
            min_temp=coolest_day_information.lowest_temperature(),
            min_month=coolest_day_information.month_name(),
            min_date=coolest_day_information.day(),
            humidity=humid_day_information.max_humidity(),
            humid_month=coolest_day_information.month_name(),
            humid_date=coolest_day_information.day(),
        )

        print(report)

    @staticmethod
    def print_monthly(weather_list):
        report_template = "Highest Average: {max_temp:{prec}}C\n"
        report_template += "Lowest Average: {min_temp:{prec}}C\n"
        report_template += "Average Mean Humidity: {humidity:{prec}}%\n"

        highest_termperatures = [weather.highest_temperature() for weather in weather_list if
                                 weather.highest_temperature() is not None]
        lowest_termperatures = [weather.lowest_temperature() for weather in weather_list if
                                weather.lowest_temperature() is not None]
        highest_humidities = [weather.mean_humidity() for weather in weather_list if weather.max_humidity() is not None]

        max_average = mean(highest_termperatures)
        min_average = mean(lowest_termperatures)
        humidity = mean(highest_humidities)
        report = report_template.format(
            max_temp=max_average,
            min_temp=min_average,
            humidity=humidity,
            prec='.3'
        )
        print(report)

    @staticmethod
    def print_monthly_bar_graph(daily_weathers, year):
        print(f"{daily_weathers[0].month_name()} {year}")

        for weather in daily_weathers:
            day = "{day:0>2} ".format(day=weather.day())
            print(Bcolors.PURLPLE + day, end="")

            for _ in range(0, weather.lowest_temperature() or 0):
                print(Bcolors.BLUE + "+", end="")

            for _ in range(0, weather.highest_temperature() or 0):
                print(Bcolors.FAIL + "+", end="")
            min_temp = "{min_temp:0>2}C".format(
                min_temp=str(weather.lowest_temperature()))
            max_temp = "{max_temp:0>2}C".format(
                max_temp=str(weather.highest_temperature()))
            print(f"{Bcolors.PURLPLE} {min_temp} - {max_temp}", end="\n")

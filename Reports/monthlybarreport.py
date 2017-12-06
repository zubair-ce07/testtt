class bcolors:
    PURLPLE = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ITL = '\033[3m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MonthlyBarReport:

    def print(self, monthly_weather, year):
        print(monthly_weather.get_month_name() + " " + year)

        for weather in monthly_weather.daily_weathers:
            day = "{day:0>2} ".format(day=weather.get_day())
            print(bcolors.PURLPLE+day, end="")

            for _ in range(0, weather.get_lowest_temperature()):
                print(bcolors.BLUE+"+", end="")

            for _ in range(0, weather.get_highest_temperature()):
                print(bcolors.FAIL+"+", end="")
            min_temp = "{min_temp:0>2}C".format(
                min_temp=str(weather.get_lowest_temperature()))
            max_temp = "{max_temp:0>2}C".format(
                max_temp=str(weather.get_highest_temperature()))
            print(bcolors.PURLPLE+" "+min_temp+" - "+max_temp, end="\n")

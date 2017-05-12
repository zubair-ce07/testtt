from termcolor import colored

from monthweather import MonthWeatherModel


def execute_task3(file_name, components):
    month_model = MonthWeatherModel(file_name)
    print("\n")

    print(str(components.strftime("%B %Y")))

    for curr_day in month_model.daily_weather_info:
        print(str(curr_day.date.day), colored('+', 'red') * curr_day.max_temperature,
              str(curr_day.max_temperature) + 'C')
        print(str(curr_day.date.day), colored('+', 'blue') * curr_day.min_temperature,
              str(curr_day.min_temperature) + 'C')

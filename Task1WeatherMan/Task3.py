from monthweather import MonthWeatherModel


def print_highest_lowest_temperatures(file_name, components):
    month_model = MonthWeatherModel(file_name)
    print("\n")
    print(str(components.strftime("%B")), str(components.strftime("%Y")))
    month_model.print_highest_lowest_chart()

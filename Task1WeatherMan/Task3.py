from MonthWeather import MonthWeatherModel
import HelperFile
from datetime import datetime


def print_highest_lowest_temperatures(input_string):
    try:
        components = datetime.strptime(input_string, '%Y' + '/' + '%m')
    except ValueError:
        print("Data for", input_string, "is not available")
        return

    year = str(components.year)
    month = components.month
    month = HelperFile.get_month_abbreviation(month)

    file_name = "Murree_weather_" + year + "_" + month + ".txt"

    if HelperFile.does_weather_file_exist(file_name) == False:
        print("Data for", input_string, "is not available")
        return

    month_model = MonthWeatherModel(file_name)
    print("\n")
    print(str(components.strftime("%B")), str(components.strftime("%Y")))
    month_model.print_highest_and_lowest_for_whole_month()

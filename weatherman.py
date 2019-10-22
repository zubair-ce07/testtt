"""This module give weather details."""
import argparse
import constants
from file_reader import FileReader
from weather import Weather
from util import validate_path, validate_year, validate_year_month

class Weatherman:
    """Handle the weather operations"""
    def __init__(self, date, path, mode):
        self.file_reader = FileReader(date, path)
        self.mode = mode


    def year_details(self):
        """For a given year display the highest temperature and day,lowest temperature and day, most humid day
        and humidity.
        """
        max_temp_weather = None
        low_temp_weather = None
        max_hum_weather = None
        
        file_record = self.file_reader.next_record()
        weather_data = Weather(file_record)
        while file_record:
            max_temp_weather = Weather.get_by_max_temp(max_temp_weather, weather_data)
            low_temp_weather = Weather.get_by_low_temp(low_temp_weather, weather_data)
            max_hum_weather = Weather.get_by_max_humidity(max_hum_weather, weather_data)

            file_record = self.file_reader.next_record()
            weather_data = Weather(file_record)

        print(f"Highest: {max_temp_weather.max_temperaturec}C on {max_temp_weather.get_month_day()}")
        print(f"Lowest: {low_temp_weather.min_temperaturec}C on {low_temp_weather.get_month_day()}")
        print(f"Humid: {max_hum_weather.max_humidity}% on {max_hum_weather.get_month_day()}")


    def month_average_detail(self):
        """For a given month display the average highest temperature, average lowest temperature, average humidity."""
        avg_max_temp_weather = None
        avg_low_temp_weather = None
        avg_max_hum_weather = None

        file_record = self.file_reader.next_record()
        weather_data = Weather(file_record)
        while file_record:
            avg_max_temp_weather = Weather.get_by_average_max_temp(avg_max_temp_weather, weather_data)
            avg_low_temp_weather = Weather.get_by_average_low_temp(avg_low_temp_weather, weather_data)
            avg_max_hum_weather = Weather.get_by_average_max_humidity(avg_max_hum_weather, weather_data)

            file_record = self.file_reader.next_record()
            weather_data = Weather(file_record)

        print(avg_max_temp_weather.get_month_year())
        print(f"Highest: {avg_max_temp_weather.mean_temperaturec}C")
        print(f"Lowest: {avg_low_temp_weather.mean_temperaturec}C")
        print(f"Humid: {avg_max_hum_weather.mean_humidity}%")


    def month_horizontal_chart(self):
        """For a given month draw two horizontal bar charts on the console for the highest and lowest temperature on 
        each day.Highest in red and lowest in blue.
        """
        file_record = self.file_reader.next_record()
        weather_data = Weather(file_record)
        print(weather_data.get_month_year())
        while file_record:
            print(f"{weather_data.get_day()} ", end="")
            for _ in range(int(weather_data.min_temperaturec)):
                print(f"{constants.COLOR_BLUE}+{constants.COLOR_ENDC}", end="")

            if self.mode == 'c':
                print(f"{constants.COLOR_BLUE}+{constants.COLOR_ENDC}", end="")
                print(f" {weather_data.min_temperaturec}\n{weather_data.get_day()} ", end="")

            for _ in range(int(weather_data.max_temperaturec)):
                print(f"{constants.COLOR_RED}+{constants.COLOR_ENDC}", end="")

            if self.mode == 'c':
                print(f" {weather_data.max_temperaturec}")
            else:
                print(f" {weather_data.min_temperaturec}C - {weather_data.max_temperaturec}C")

            file_record = self.file_reader.next_record()
            weather_data = Weather(file_record)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=validate_path, help="Path to weather files")
    parser.add_argument("-e", type=validate_year, help="Display the highest,lowest temperature and day, most humid\
                                                        day and humidity")
    parser.add_argument("-a", type=validate_year_month, help="Display the average highest, average lowest temperature\
                                                            , average humidity")
    parser.add_argument("-c", type=validate_year_month, help="Draw two bar charts for highest in blue and lowest\
                                                             temperature in red on each day.")
    parser.add_argument("-d", type=validate_year_month, help="Draw one bar chart for highest in blue and lowest\
                                                             temperature in red on each day.")
    args = parser.parse_args()
    PATH = args.path
    if args.e:
        MODE = "e"
        DATE = args.e
    elif args.a:
        MODE = "a"
        DATE = args.a
    elif args.c:
        MODE = "c"
        DATE = args.c
    elif args.d:
        MODE = "d"
        DATE = args.d

    weatherman = Weatherman(DATE, PATH, MODE)
    TASKS = {
        "e": weatherman.year_details,
        "a": weatherman.month_average_detail,
        "c": weatherman.month_horizontal_chart,
        "d": weatherman.month_horizontal_chart,
    }
    TASKS[MODE]()

import calendar
from weather_analyser import WeatherAnalyser


class WeatherReporter:

    def __init__(self):
        self.weather_analyser = WeatherAnalyser()

    def print_yearly_weather_report(self, year, weather_files_path):
        yearly_weather_report = self.weather_analyser.calculate_weather_data_for_year_(
            year, weather_files_path
        )
        _, weather_month, weather_day = self.weather_analyser.get_weather_date(
            yearly_weather_report[0].get_date()
        )
        highest_temperature_date = weather_day
        highest_temperature_month = calendar.month_name[weather_month]
        highest_temperature = yearly_weather_report[0].get_max_temperature()
        _, weather_month, weather_day = self.weather_analyser.get_weather_date(
            yearly_weather_report[1].get_date()
        )
        lowest_temperature_date = weather_day
        lowest_temperature_month = calendar.month_name[weather_month]
        lowest_temperature = yearly_weather_report[1].get_min_temperature()
        _, weather_month, weather_day = self.weather_analyser.get_weather_date(
            yearly_weather_report[2].get_date()
        )
        most_humid_day_date = weather_day
        most_humid_day_month = calendar.month_name[weather_month]
        humidity = yearly_weather_report[2].get_humidity()
        print("Highest: {}C on {} {} ".format(
            highest_temperature,highest_temperature_month,highest_temperature_date)
        )
        print("Lowest: {}C on {} {} ".format(
            lowest_temperature, lowest_temperature_month, lowest_temperature_date)
        )
        print("Humid: {}% on {} {} ".format(
            humidity, most_humid_day_month, most_humid_day_date)
        )

    def print_monthly_average_report(self, year, month, weather_files_path):
        weather_averages = self.weather_analyser.calculate_weather_data_averages(
            year, month, weather_files_path
        )
        print("Highest Average: {}C".format(weather_averages["Highest Average"]))
        print("Lowest Average: {}C".format(weather_averages["Lowest Average"]))
        print("Average Humidity: {}%".format(weather_averages["Average Humidity"]))


    def print_daily_report(self, year, month, weather_files_path):
        bars_weather_data = self.weather_analyser.calculate_weather_data_for_bars(
            year, month, weather_files_path
        )
        print(calendar.month_name[int(month)] + " " + year)
        BLUE = "\033[96m"
        RED = "\033[91m"
        for day_weather in range(len(bars_weather_data)):
            _, _, weather_day = self.weather_analyser.get_weather_date(
                bars_weather_data[day_weather].get_date()
            )
            date = weather_day
            max_temperature = bars_weather_data[day_weather].get_max_temperature()
            min_temperature = bars_weather_data[day_weather].get_min_temperature()
            print(self.weather_analyser.generate_daily_report_bar(date,RED,max_temperature))
            print(self.weather_analyser.generate_daily_report_bar(date, BLUE, min_temperature))

    def print_daily_report_bonus(self, year, month, weather_files_path):
        bars_weather_data = self.weather_analyser.calculate_weather_data_for_bars(
            year, month, weather_files_path
        )
        print(calendar.month_name[int(month)] + " " + year)
        for day_weather in range(len(bars_weather_data)):
            _, _, weather_day = self.weather_analyser.get_weather_date(
                bars_weather_data[day_weather].get_date()
            )
            date = weather_day
            max_temperature = bars_weather_data[day_weather].get_max_temperature()
            min_temperature = bars_weather_data[day_weather].get_min_temperature()
            print(self.weather_analyser.generate_daily_report_bounas_bar(date,max_temperature,min_temperature))
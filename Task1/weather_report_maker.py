class WeatherReporter:
    RED_COLOR_CODE = '\033[91m{}\033[0m'
    BLUE_COLOR_CODE = '\33[94m{}\033[0m'

    @staticmethod
    def print_annual_report(weather_result):
        weather_report = f"Highest: {weather_result.max_temperature_record.highest_temperature}C " \
                         f"{weather_result.max_temperature_record.date:%B %d}\n" \
                         f"Lowest: {weather_result.min_temperature_record.lowest_temperature}C " \
                         f"{weather_result.min_temperature_record.date:%B %d}\n" \
                         f"Humidity: {weather_result.max_humidity_record.max_humidity}% " \
                         f"{weather_result.max_humidity_record.date:%B %d}\n\n"

        print(weather_report)

    @staticmethod
    def print_monthly_report(weather_result):
        weather_report = f"Highest Average: {weather_result.max_avg_temperature_record.mean_temperature}C\n" \
                         f"Lowest Average: {weather_result.min_avg_temperature_record.mean_temperature}C\n" \
                         f"Average Mean Humidity: {weather_result.mean_humidity:.0f}%\n\n"

        print(weather_report)

    @staticmethod
    def print_charts_for_extremes(weather_result):
        weather_report = ""
        for temperatures in weather_result.daily_temperatures:
            record_date = temperatures.date

            if record_date:
                max_temp = temperatures.highest_temperature
                min_temp = temperatures.lowest_temperature
                red_stars = WeatherReporter.RED_COLOR_CODE.format('+' * abs(max_temp))
                blue_stars = WeatherReporter.BLUE_COLOR_CODE.format('+' * abs(min_temp))

                weather_report += f"{record_date.day:02} {red_stars} {max_temp}\n"
                weather_report += f"{record_date.day:02} {blue_stars} {min_temp}\n"

        print(weather_report)

    @staticmethod
    def print_mixed_chart_for_extremes(weather_result):
        weather_report = ""
        for temperatures in weather_result.daily_temperatures:
            record_date = temperatures.date

            if record_date:
                max_temp = temperatures.highest_temperature
                min_temp = temperatures.lowest_temperature
                red_stars = WeatherReporter.RED_COLOR_CODE.format('+' * abs(max_temp))
                blue_stars = WeatherReporter.BLUE_COLOR_CODE.format('+' * abs(min_temp))

                weather_report += f"{record_date.day:02} {red_stars}{blue_stars} {max_temp} {min_temp}\n"

        print(weather_report)

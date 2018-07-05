class WeatherReportMaker:
    # The variables defined for displaying colored output
    RED_COLOR_CODE = '\033[91m{}\033[0m'
    BLUE_COLOR_CODE = '\33[94m{}\033[0m'

    @staticmethod
    def print_report_for_e(weather_result):
        if weather_result:
            weather_report = f"Highest: {weather_result.highest_temperature}C " \
                             f"{weather_result.highest_temperature_day:%B %d}\n" \
                             f"Lowest: {weather_result.lowest_temperature}C " \
                             f"{weather_result.lowest_temperature_day:%B %d}\n" \
                             f"Humidity: {weather_result.highest_humidity}% " \
                             f"{weather_result.most_humid_day:%B %d}\n\n"

            print(weather_report)

    @staticmethod
    def print_report_for_a(weather_result):
        if weather_result:
            weather_report = f"Highest Average: {weather_result.highest_temperature}C\n" \
                             f"Lowest Average: {weather_result.lowest_temperature}C\n" \
                             f"Average Mean Humidity: {weather_result.mean_humidity:.0f}%\n\n"

            print(weather_report)

    @staticmethod
    def print_report_for_c(weather_result):
        if weather_result:
            weather_report = ""
            for idx, temperatures in enumerate(weather_result.daily_temperatures):
                max_temp, min_temp = temperatures[0], temperatures[1]

                if max_temp != "":
                    red_stars = WeatherReportMaker.RED_COLOR_CODE.format(
                        ''.join(['+' for _ in range(abs(max_temp))])
                    )
                else:
                    red_stars = ""
                    max_temp = "NA"

                if min_temp != "":
                    blue_stars = WeatherReportMaker.BLUE_COLOR_CODE.format(
                        ''.join(['+' for _ in range(abs(min_temp))])
                    )
                else:
                    blue_stars = ""
                    min_temp = "NA"

                weather_report += f"{idx+1:02} {red_stars} {max_temp}\n"
                weather_report += f"{idx+1:02} {blue_stars} {min_temp}\n"

            print(weather_report)

    @staticmethod
    def print_report_for_c_bonus(weather_result):
        if weather_result:
            weather_report = ""
            for idx, temperatures in enumerate(weather_result.daily_temperatures):
                max_temp, min_temp = temperatures[0], temperatures[1]

                if max_temp != "":
                    red_stars = WeatherReportMaker.RED_COLOR_CODE.format(
                        ''.join(['+' for _ in range(abs(max_temp))])
                    )
                else:
                    red_stars = ""
                    max_temp = "NA"

                if min_temp != "":
                    blue_stars = WeatherReportMaker.BLUE_COLOR_CODE.format(
                        ''.join(['+' for _ in range(abs(min_temp))])
                    )
                else:
                    blue_stars = ""
                    min_temp = "NA"

                weather_report += f"{idx+1:02} {red_stars}{blue_stars} {max_temp} {min_temp}\n"

            print(weather_report)

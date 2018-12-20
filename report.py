import colors


class Report:

    def year_peak_report(self, year_weather_data):
        max_day = year_weather_data["max_temp_day"]
        min_day = year_weather_data["min_temp_day"]
        max_humidity_day = year_weather_data["max_humidity_day"]

        print(f"Highest temperature: {max_day.max_temp} on {max_day.date.strftime('%B %d')}")
        print(f"Lowest temperature: {min_day.min_temp} on {min_day.date.strftime('%B %d')}")
        print(f"Maximum Humidity: {max_humidity_day.max_humidity} on {max_humidity_day.date.strftime('%B %d')}")

    def month_average_report(self, month_data):
        print(f"Highest Average: {month_data['highest_temp']}")
        print(f"Lowest Average: {month_data['lowest_temp']}")
        print(f"Average Mean Humidity: {month_data['highest_humidity']}%")

    def bar_chart_report(self, month_data):
        max_day = month_data['max_day']
        min_day = month_data['min_day']

        print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
              f"{colors.RED}{('+' * int(max_day.max_temp))} {colors.RESET}{max_day.max_temp}C")
        print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
              f"{colors.BLUE}{('+' * int(max_day.min_temp))} {colors.RESET}{max_day.min_temp}C")

        print(f"Lowest High temperature: on {min_day.date.strftime('%B %d')} "
              f"{colors.RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
              f"{colors.RESET}{min_day.max_temp if min_day.max_temp else 0}C")
        print(f"Lowest Low temperature: on {min_day.date.strftime('%B %d')} "
              f"{colors.BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)} "
              f"{colors.RESET}{min_day.min_temp if min_day.min_temp else 0}C")

    def bar_chart_report_bonus(self, month_data):
        max_day = month_data['max_day']
        min_day = month_data['min_day']

        print(f"Highest temperature: {max_day.date.strftime('%B %d')} {colors.BLUE}{('+' * int(max_day.min_temp))} "
              f"{colors.RED}{('+' * int(max_day.max_temp))} {colors.RESET}{max_day.min_temp}C- {max_day.max_temp}C")
        print(f"Highest temperature: {min_day.date.strftime('%B %d')} "
              f"{colors.BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)}"
              f"{colors.RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
              f"{colors.RESET}{min_day.min_temp if min_day.min_temp else 0}C - "
              f"{min_day.max_temp if min_day.max_temp else 0}C")

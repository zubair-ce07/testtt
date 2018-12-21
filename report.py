import color


class Report:

    def year_peak_report(self, year_weather_data):
        max_temp_day = year_weather_data["max_temp_day"]
        min_temp_day = year_weather_data["min_temp_day"]
        max_humid_day = year_weather_data["max_humidity_day"]

        print(f"Highest temperature: {max_temp_day.max_temp} on {max_temp_day.date.strftime('%B %d')}")
        print(f"Lowest temperature: {min_temp_day.min_temp} on {min_temp_day.date.strftime('%B %d')}")
        print(f"Maximum Humidity: {max_humid_day.max_humidity} on {max_humid_day.date.strftime('%B %d')}")

    def month_average_report(self, month_data):
        print(f"Highest Average: {month_data['highest_temp']}")
        print(f"Lowest Average: {month_data['lowest_temp']}")
        print(f"Average Mean Humidity: {month_data['highest_humidity']}%")

    def bar_chart_report(self, month_data, bonus=0):
        max_day = month_data['max_day']
        min_day = month_data['min_day']
        if bonus:
            print(bonus)
            print(
                f"{max_day.date.strftime('%B %d')} \n"
                f"{color.BLUE}{('+' * int(max_day.min_temp))} "
                f"{color.RED}{('+' * int(max_day.max_temp))} {color.RESET}{max_day.min_temp}C - {max_day.max_temp}C")
            print(
                f"{color.BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)}"
                f"{color.RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
                f"{color.RESET}{min_day.min_temp if min_day.min_temp else 0}C - "
                f"{min_day.max_temp if min_day.max_temp else 0}C")
        else:
            print(bonus)
            print(
                f"{max_day.date.strftime('%B %d')} \n"
                f"{color.RED}{('+' * int(max_day.max_temp))} {color.RESET}{max_day.max_temp}C \n"
                f"{color.BLUE}{('+' * int(max_day.min_temp))} {color.RESET}{max_day.min_temp}C")
            print(
                f"{color.RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
                f"{color.RESET}{min_day.max_temp if min_day.max_temp else 0}C \n"
                f"{color.BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)} "
                f"{color.RESET}{min_day.min_temp if min_day.min_temp else 0}C")

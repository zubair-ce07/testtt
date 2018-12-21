import color


class Report:

    def generate_peak_values(self, weather_record, month=0):
        if month:
            print(f"Highest Average: {weather_record['highest_temp']}")
            print(f"Lowest Average: {weather_record['lowest_temp']}")
            print(f"Average Mean Humidity: {weather_record['highest_humidity']}%")
        else:
            max_temp_day = weather_record["max_temp_day"]
            min_temp_day = weather_record["min_temp_day"]
            max_humid_day = weather_record["max_humidity_day"]
            print(f"Highest temperature: {max_temp_day.max_temp} on {max_temp_day.date.strftime('%B %d')}")
            print(f"Lowest temperature: {min_temp_day.min_temp} on {min_temp_day.date.strftime('%B %d')}")
            print(f"Maximum Humidity: {max_humid_day.max_humidity} on {max_humid_day.date.strftime('%B %d')}")

    def generate_bar_chart(self, month_data, bonus=0):
        max_day = month_data['max_day']
        min_day = month_data['min_day']
        if bonus:
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
            print(
                f"{max_day.date.strftime('%B %d')} \n"
                f"{color.RED}{('+' * int(max_day.max_temp))} {color.RESET}{max_day.max_temp}C \n"
                f"{color.BLUE}{('+' * int(max_day.min_temp))} {color.RESET}{max_day.min_temp}C")
            print(
                f"{color.RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
                f"{color.RESET}{min_day.max_temp if min_day.max_temp else 0}C \n"
                f"{color.BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)} "
                f"{color.RESET}{min_day.min_temp if min_day.min_temp else 0}C")

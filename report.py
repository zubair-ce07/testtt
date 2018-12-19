RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'


def year_peak_report(year_weather_data):
    max_day = year_weather_data[0]
    min_day = year_weather_data[0]
    max_humidity_day = year_weather_data[0]

    print(f"Highest temperature: {max_day.max_temp} on {max_day.date.strftime('%B %d')}")
    print(f"Lowest temperature: {min_day.min_temp} on {min_day.date.strftime('%B %d')}")
    print(f"Maximum Humidity: {max_humidity_day.max_humidity} on {max_humidity_day.date.strftime('%B %d')}")


def month_average_report(month_data):
    highest_temp = month_data[0]
    lowest_temp = month_data[1]
    highest_humidity = month_data[2]

    print(f"Highest Average: {(sum(highest_temp) // len(highest_temp))}")
    print(f"Lowest Average: {(sum(lowest_temp) // len(lowest_temp))}")
    print(f"Average Mean Humidity: {(sum(highest_humidity) // len(highest_humidity))}%")


def bar_chart_report(month_data):
    max_day = month_data[0]
    min_day = month_data[0]

    print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
          f"{RED}{('+' * int(max_day.max_temp))} {RESET}{max_day.max_temp}C")
    print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
          f"{BLUE}{('+' * int(max_day.min_temp))} {RESET}{max_day.min_temp}C")
    print(f"Lowest High temperature: on {min_day.date.strftime('%B %d')} "
          f"{RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
          f"{RESET}{min_day.max_temp if min_day.max_temp else 0}C")
    print(f"Lowest Low temperature: on {min_day.date.strftime('%B %d')} "
          f"{BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)} "
          f"{RESET}{min_day.min_temp if min_day.min_temp else 0}C")


def bar_chart_report_bonus(month_data):
    max_day = month_data[0]
    min_day = month_data[0]

    print(f"Highest temperature: {max_day.date.strftime('%B %d')} {BLUE}{('+' * int(max_day.min_temp))} "
          f"{RED}{('+' * int(max_day.max_temp))} {RESET}{max_day.min_temp}C- {max_day.max_temp}C")
    print(f"Highest temperature: {min_day.date.strftime('%B %d')} "
          f"{BLUE}{('+' * int(min_day.min_temp) if min_day.min_temp else 0)}"
          f"{RED}{('+' * int(min_day.max_temp) if min_day.max_temp else 0)} "
          f"{RESET}{min_day.min_temp if min_day.min_temp else 0}C - "
          f"{min_day.max_temp if min_day.max_temp else 0}C")

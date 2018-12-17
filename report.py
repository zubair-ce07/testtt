from colr import Colr


def yearly_lowest_highest_values(year_data):
    max_day = year_data[0][0]
    min_day = year_data[0][0]
    max_humidity_day = year_data[0][0]

    for month_num in range(len(year_data)):
        for day in range(len(year_data[month_num])):
            if max_day.max_temp < year_data[month_num][day].max_temp:
                max_day = year_data[month_num][day]
            if min_day.min_temp > year_data[month_num][day].min_temp:
                min_day = year_data[month_num][day]
            if max_humidity_day.max_humidity < year_data[month_num][day].max_humidity:
                max_humidity_day = year_data[month_num][day]

    print(f"Highest temperature: {max_day.max_temp} on {max_day.date.strftime('%B %d')}")
    print(f"Lowest temperature: {min_day.min_temp} on {min_day.date.strftime('%B %d')}")
    print(f"Maximum Humidity: {max_humidity_day.max_humidity} on {max_humidity_day.date.strftime('%B %d')}")


def monthly_average_values(month_data):
    highest_temp = [float(day.max_temp) if day.max_temp else 0 for day in month_data]
    lowest_temp = [float(day.min_temp) if day.min_temp else 0 for day in month_data]
    highest_humidity = [float(day.max_humidity) if day.max_humidity else 0 for day in month_data]

    print(f"Highest Average: {(sum(highest_temp) / len(highest_temp)).__round__()}")
    print(f"Lowest Average: {(sum(lowest_temp) / len(lowest_temp)).__round__()}")
    print(f"Average Mean Humidity: {(sum(highest_humidity) / len(highest_humidity)).__round__()}%")


def horizontal_bar_for_given_month(month_data):
    max_day = month_data[0]
    min_day = month_data[0]

    for day in month_data:
        if max_day.max_temp < day.max_temp:
            max_day = day
        if min_day.min_temp > day.min_temp:
            min_day = day

    print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(max_day.max_temp), fore='red')} {max_day.max_temp}")
    print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(max_day.min_temp), fore='blue')} {max_day.min_temp}")
    print(f"Lowest High temperature: on {min_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(min_day.max_temp) if min_day.max_temp else 0, fore='red')} "
          f"{min_day.max_temp if min_day.max_temp else 0}")
    print(f"Lowest Low temperature: on {min_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(min_day.min_temp) if min_day.min_temp else 0, fore='blue')} "
          f"{min_day.min_temp if min_day.min_temp else 0}")


def mixed_bar_for_given_month(month_data):
    max_day = month_data[0]
    min_day = month_data[0]

    for day in month_data:
        if max_day.max_temp < day.max_temp:
            max_day = day
        if min_day.min_temp > day.min_temp:
            min_day = day

    print(f"Highest temperature: on {max_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(max_day.min_temp), fore='blue')}"
          f"{Colr('+' * int(max_day.max_temp), fore='red')} "
          f"{max_day.min_temp}C- {max_day.max_temp}C")
    print(f"Highest temperature: on {min_day.date.strftime('%B %d')} "
          f"{Colr('+' * int(min_day.min_temp) if min_day.min_temp else 0, fore='blue')}"
          f"{Colr('+' * int(min_day.max_temp) if min_day.max_temp else 0, fore='red')} "
          f"{min_day.min_temp if min_day.min_temp else 0}C - "
          f"{min_day.max_temp if min_day.max_temp else 0}C")

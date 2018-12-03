
import statistics
from termcolor import colored, cprint
from colr import Colr as C


# task 1 Calculation
def yearly_lowest_highest_values(required_year, all_data_list, months_list):

    global sentinel_temperature_value
    this_year_months_list = []

    record_of_required_year = all_data_list[required_year]

    for i in record_of_required_year.keys():
        this_year_months_list.append(i)

    for month in months_list:
        if month in record_of_required_year.keys():
            sentinel_temperature_value = record_of_required_year[month][0]
            break

    time_being_max_temperature = sentinel_temperature_value
    time_being_min_temperature = sentinel_temperature_value
    time_being_max_humidity = sentinel_temperature_value

    for month_number in this_year_months_list:
        for day_number in record_of_required_year[month_number]:
            if time_being_max_temperature.max_temp < day_number.max_temp:
                time_being_max_temperature = day_number
            if time_being_min_temperature.min_temp > day_number.min_temp:
                time_being_min_temperature = day_number
            if time_being_max_humidity.max_humidity < day_number.max_humidity:
                time_being_max_humidity = day_number

    print('\n')
    print("======================================")
    print(f"Highest temperature: {time_being_max_temperature.max_temp} on "
          f"{time_being_max_temperature.date.strftime('%B %d')}")
    print(f"Lowest temperature: {time_being_min_temperature.min_temp} on "
          f"{time_being_min_temperature.date.strftime('%B %d')}")
    print(f"Maximum Humidity: {time_being_max_humidity.max_humidity} on "
          f"{time_being_max_humidity.date.strftime('%B %d')}")
    print("======================================")
    print('\n')


# Task 2 Calculation
def monthly_average_values(required_year, required_month, all_data_list, months_list):
    print(all_data_list.keys())
    record_of_required_year = all_data_list[required_year]
    record_of_required_month = record_of_required_year[months_list[required_month-1]]

    highest_temp_values = [float(max_T.max_temp) if max_T.max_temp else 0 for max_T in record_of_required_month]
    lowest_temp_values = [float(min_T.min_temp) if min_T.min_temp else 0 for min_T in record_of_required_month]
    highest_humidity_values = [float(max_T.max_humidity) if max_T.max_humidity else 0
                               for max_T in record_of_required_month]

    print('\n')
    print("=====================================")
    print(f"Highest Average: {statistics.mean(highest_temp_values).__round__()}")
    print(f"Lowest Average: {statistics.mean(lowest_temp_values).__round__()}")
    print(f"Average Mean Humidity: {statistics.mean(highest_humidity_values).__round__()}%")
    print("=====================================")
    print('\n')


# Task 3 Calculation
def horizontal_bar_for_given_month(required_year, required_month, all_data_list, months_list):
    global sentinel_temperature_value
    this_year_months_list = []

    record_of_required_year = all_data_list[required_year]
    record_of_required_month = record_of_required_year[months_list[required_month-1]]

    for i in record_of_required_year.keys():
        this_year_months_list.append(i)

    for month in months_list:
        if month in record_of_required_year.keys():
            sentinel_temperature_value = record_of_required_year[month][0]
            break

    time_being_max_temp_day = sentinel_temperature_value
    time_being_min_temp_day = sentinel_temperature_value

    for day_number in record_of_required_month:
        if time_being_max_temp_day.max_temp < day_number.max_temp:
            time_being_max_temp_day = day_number
        if time_being_min_temp_day.min_temp > day_number.min_temp:
            time_being_min_temp_day = day_number

    print('\n')
    print("===============================================")
    print(f"Highest temperature: on {time_being_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_max_temp_day.max_temp), fore='red')} "
          f"{time_being_max_temp_day.max_temp}")
    print(f"Highest temperature: on {time_being_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_max_temp_day.min_temp), fore='blue')} {time_being_max_temp_day.min_temp}")
    print('\n')
    print(f"Lowest High temperature: on {time_being_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_min_temp_day.max_temp) if time_being_min_temp_day.max_temp else 0, fore='red')} "
          f"{time_being_min_temp_day.max_temp if time_being_min_temp_day.max_temp else 0}")
    print(f"Lowest Low temperature: on {time_being_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_min_temp_day.min_temp) if time_being_min_temp_day.min_temp else 0, fore='blue')} "
          f"{time_being_min_temp_day.min_temp if time_being_min_temp_day.min_temp else 0}")
    print("===============================================")
    print('\n')


# Task 5 Calculation BONUS task
def mixed_bar_for_given_month(required_year, required_month, all_data_list, months_list):
    global sentinel_temperature_value
    this_year_months_list = []

    record_of_required_year = all_data_list[required_year]
    record_of_required_month = record_of_required_year[months_list[required_month-1]]

    for i in record_of_required_year.keys():
        this_year_months_list.append(i)

    for month in months_list:
        if month in record_of_required_year.keys():
            sentinel_temperature_value = record_of_required_year[month][0]
            break

    time_being_max_temp_day = sentinel_temperature_value
    time_being_min_temp_day = sentinel_temperature_value

    for day_number in record_of_required_month:
        if time_being_max_temp_day.max_temp < day_number.max_temp:
            time_being_max_temp_day = day_number
        if time_being_min_temp_day.min_temp > day_number.min_temp:
            time_being_min_temp_day = day_number

    print('\n')
    print("=============================================")
    print(f"Highest temperature: on {time_being_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_max_temp_day.min_temp), fore='blue')}"
          f"{C('+' * int(time_being_max_temp_day.max_temp), fore='red')} "
          f"{time_being_max_temp_day.min_temp}C- {time_being_max_temp_day.max_temp}C")
    print('\n')
    print(f"Highest temperature: on {time_being_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(time_being_min_temp_day.min_temp) if time_being_min_temp_day.min_temp else 0, fore='blue')}"
          f"{C('+' * int(time_being_min_temp_day.max_temp) if time_being_min_temp_day.max_temp else 0, fore='red')} "
          f"{time_being_min_temp_day.min_temp if time_being_min_temp_day.min_temp else 0}C - "
          f"{time_being_min_temp_day.max_temp if time_being_min_temp_day.max_temp else 0}C")
    print("=============================================")
    print('\n')

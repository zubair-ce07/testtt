
import statistics
from colr import Colr as C


# task 1 Calculation
def yearly_lowest_highest_values(this_year_data_list):

    temporary_max_temperature_day = this_year_data_list[0][0]
    temporary_min_temperature_day = this_year_data_list[0][0]
    temporary_max_humidity_day = this_year_data_list[0][0]

    for month_number in range(len(this_year_data_list)):
        for day_number in range(len(this_year_data_list[month_number])):
            if temporary_max_temperature_day.max_temp < this_year_data_list[month_number][day_number].max_temp:
                temporary_max_temperature_day = this_year_data_list[month_number][day_number]
            if temporary_min_temperature_day.min_temp > this_year_data_list[month_number][day_number].min_temp:
                temporary_min_temperature_day = this_year_data_list[month_number][day_number]
            if temporary_max_humidity_day.max_humidity < this_year_data_list[month_number][day_number].max_humidity:
                temporary_max_humidity_day = this_year_data_list[month_number][day_number]

    print('\n')
    print("======================================")
    print(f"Highest temperature: {temporary_max_temperature_day.max_temp} on "
          f"{temporary_max_temperature_day.date.strftime('%B %d')}")
    print(f"Lowest temperature: {temporary_min_temperature_day.min_temp} on "
          f"{temporary_min_temperature_day.date.strftime('%B %d')}")
    print(f"Maximum Humidity: {temporary_max_humidity_day.max_humidity} on "
          f"{temporary_max_humidity_day.date.strftime('%B %d')}")
    print("======================================")
    print('\n')


# Task 2 Calculation
def monthly_average_values(required_month, this_year_data_list):

    record_of_required_month = this_year_data_list[required_month-1]

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
def horizontal_bar_for_given_month(required_month, this_year_data_list):

    record_of_required_month = this_year_data_list[required_month - 1]

    temporary_max_temp_day = record_of_required_month[0]
    temporary_min_temp_day = record_of_required_month[0]

    for day_number in record_of_required_month:
        if temporary_max_temp_day.max_temp < day_number.max_temp:
            temporary_max_temp_day = day_number
        if temporary_min_temp_day.min_temp > day_number.min_temp:
            temporary_min_temp_day = day_number

    print('\n')
    print("===============================================")
    print(f"Highest temperature: on {temporary_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_max_temp_day.max_temp), fore='red')} "
          f"{temporary_max_temp_day.max_temp}")
    print(f"Highest temperature: on {temporary_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_max_temp_day.min_temp), fore='blue')} {temporary_max_temp_day.min_temp}")
    print('\n')
    print(f"Lowest High temperature: on {temporary_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_min_temp_day.max_temp) if temporary_min_temp_day.max_temp else 0, fore='red')} "
          f"{temporary_min_temp_day.max_temp if temporary_min_temp_day.max_temp else 0}")
    print(f"Lowest Low temperature: on {temporary_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_min_temp_day.min_temp) if temporary_min_temp_day.min_temp else 0, fore='blue')} "
          f"{temporary_min_temp_day.min_temp if temporary_min_temp_day.min_temp else 0}")
    print("===============================================")
    print('\n')


# Task 5 Calculation BONUS task
def mixed_bar_for_given_month(required_month, this_year_data_list):

    record_of_required_month = this_year_data_list[required_month - 1]

    temporary_max_temp_day = record_of_required_month[0]
    temporary_min_temp_day = record_of_required_month[0]

    for day_number in record_of_required_month:
        if temporary_max_temp_day.max_temp < day_number.max_temp:
            temporary_max_temp_day = day_number
        if temporary_min_temp_day.min_temp > day_number.min_temp:
            temporary_min_temp_day = day_number

    print('\n')
    print("=============================================")
    print(f"Highest temperature: on {temporary_max_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_max_temp_day.min_temp), fore='blue')}"
          f"{C('+' * int(temporary_max_temp_day.max_temp), fore='red')} "
          f"{temporary_max_temp_day.min_temp}C- {temporary_max_temp_day.max_temp}C")
    print('\n')
    print(f"Highest temperature: on {temporary_min_temp_day.date.strftime('%B %d')} "
          f"{C('+' * int(temporary_min_temp_day.min_temp) if temporary_min_temp_day.min_temp else 0, fore='blue')}"
          f"{C('+' * int(temporary_min_temp_day.max_temp) if temporary_min_temp_day.max_temp else 0, fore='red')} "
          f"{temporary_min_temp_day.min_temp if temporary_min_temp_day.min_temp else 0}C - "
          f"{temporary_min_temp_day.max_temp if temporary_min_temp_day.max_temp else 0}C")
    print("=============================================")
    print('\n')

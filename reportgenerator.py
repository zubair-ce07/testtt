RED = "\033[1;31m"
BLUE = "\033[1;34m"
RESET = "\033[0;0m"


def generate_year_info_report(results):
    highest_temp_result = results[0]
    lowest_temp_result = results[1]
    most_humidity_result = results[2]

    print('Highest: {temp}C on {month} {day}'.format(temp=highest_temp_result[0],
                                                     month=highest_temp_result[1],
                                                     day=highest_temp_result[2]
                                                     ))
    print('Lowest: {temp}C on {month} {day}'.format(temp=lowest_temp_result[0],
                                                    month=lowest_temp_result[1],
                                                    day=lowest_temp_result[2]
                                                    ))
    print('Humidity: {humidity}% on {month} {day}\n'.format(humidity=most_humidity_result[0],
                                                            month=most_humidity_result[1],
                                                            day=most_humidity_result[2]
                                                            ))


def generate_month_info_report(results):
    highest_average = results[0]
    lowest_average = results[1]
    average_mean_humidity = results[2]

    print('Highest Average: {highest_avg}C'.format(highest_avg=highest_average))
    print('Lowest Average: {lowest_avg}C'.format(lowest_avg=lowest_average))
    print('Average Mean Humidity: {humidity}%\n'.format(humidity=average_mean_humidity))


def generate_month_temp_detailed_report(results):
    days = results[0]
    max_temps = results[1]
    min_temps = results[2]

    row = '{day} \033[1;34m{lowest_bar}\033[1;31m{highest_bar}\033[0;0m {lowest_temp}C - {highest_temp}C'
    for i, day in enumerate(days):
        max_temp = max_temps[i]
        min_temp = min_temps[i]

        highest_bar, max_temp = ('+' * max_temp, max_temp) if max_temp is not None else ('', 'N/A ')
        lowest_bar, min_temp = ('+' * min_temp, min_temp) if min_temp is not None else ('', 'N/A ')

        print(row.format(day=day,
                         lowest_bar=lowest_bar,
                         highest_bar=highest_bar,
                         lowest_temp=min_temp,
                         highest_temp=max_temp
                         ))

    print()

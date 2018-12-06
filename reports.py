from datetime import datetime
from classes import CalculationResults


def yearly_report(data_set,  year):
    max_temp, low_temp, max_humid = 0, 0, 0
    max_temp_day, low_temp_day, max_humid_day = '', '', ''

    for item in data_set:
        item_year = datetime.strptime(item.date, '%Y-%m-%d').strftime('%Y')

        if int(item_year) == year:
            if low_temp == 0:
                if item.low_temp != '':
                    low_temp = int(item.low_temp)

            if item.max_temp != '':
                if int(item.max_temp) > max_temp:
                    max_temp = int(item.max_temp)
                    max_temp_day = item.date

            if item.low_temp != '':
                if int(item.low_temp) < low_temp:
                    low_temp = int(item.low_temp)
                    low_temp_day = item.date

            if item.max_humid != '':
                if int(item.max_humid) > max_humid:
                    max_humid = int(item.max_humid)
                    max_humid_day = item.date

    result = CalculationResults()
    if max_temp_day != '':
        result.max_temp_day = datetime.strptime(max_temp_day, '%Y-%m-%d').strftime('%B %d')

    if low_temp_day != '':
        result.low_temp_day = datetime.strptime(low_temp_day, '%Y-%m-%d').strftime('%B %d')

    if max_humid_day != '':
        result.max_humid_day = datetime.strptime(max_humid_day, '%Y-%m-%d').strftime('%B %d')

    result.max_temp = max_temp
    result.low_temp = low_temp
    result.max_humid = max_humid
    return result


def monthly_report(data_set, year, month):
    max_temp, low_temp, mean_humid, no_days = 0, 0, 0, 0

    for item in data_set:
        item_year = datetime.strptime(item.date, '%Y-%m-%d').strftime('%Y')
        item_month = datetime.strptime(item.date, '%Y-%m-%d').strftime('%b')

        if (int(item_year) == year) & (item_month == month):
            no_days += 1
            if item.max_temp != '':
                max_temp += int(item.max_temp)

            if item.low_temp != '':
                low_temp += int(item.low_temp)

            if item.mean_humid != '':
                mean_humid += int(item.mean_humid)

    result = CalculationResults()
    if max_temp > 0:
        result.average_max_temp = round(max_temp / no_days, 1)

    if low_temp > 0:
        result.average_low_temp = round(low_temp / no_days, 1)

    if mean_humid > 0:
        result.average_mean_humid = round(mean_humid / no_days, 1)

    return result


def bar_chart_report(data_set, year, month):
    output = []
    for item in data_set:
        item_year = datetime.strptime(item.date, '%Y-%m-%d').strftime('%Y')
        item_month = datetime.strptime(item.date, '%Y-%m-%d').strftime('%b')

        if (int(item_year) == year) & (item_month == month):
            day = datetime.strptime(item.date, '%Y-%m-%d').strftime('%d')
            output.append({'day':day,'max_temp':item.max_temp, 'low_temp':item.low_temp})
    return output
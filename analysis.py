import glob
from datetime import datetime
from weatherman import WeatherInformation, CalculationResults


'''
Class based data structure implementation
'''


# reading data from files and preparation data in class objects based structure
def class_structured_data(path='weatherfiles/*.txt'):
    files = glob.glob(path)
    weather_list = []

    for file in files:
        file_arr = (file.replace(".txt", "")).split('_')
        year = int(file_arr[-2])
        month = str(file_arr[-1])

        with open(file, "r") as fd:
            header_row = fd.readline().split(',')
            header_row = [x.strip() for x in header_row]

            for line in fd:
                line = line.strip().split(',')
                day_arr = {}
                for index in range(0, len(line)):
                    day_arr[header_row[index]] = line[index]

                if 'PKST' in day_arr:
                    date = day_arr['PKST']
                elif 'PKT' in day_arr:
                    date = day_arr['PKT']
                else:
                    date = ''

                weather_list.append(WeatherInformation(date, year, month, day_arr['Max TemperatureC'], day_arr['Min TemperatureC'], day_arr['Max Humidity'], day_arr['Mean Humidity']))

    return weather_list


# function for computation on data dictionary
def computation_analysis(data_set, parameters):
    output = []

    if parameters[0] == '-e':
        maximum_temp, low_temp, max_humid = 0, 0, 0
        maximum_temp_day, low_temp_day, max_humid_day = '', '', ''
        year = int(parameters[1])

        for item in data_set:
            if item.year == year:
                if low_temp == 0:
                    if item.low_temp != '':
                        low_temp = int(item.low_temp)

                if item.max_temp != '':
                    if int(item.max_temp) > maximum_temp:
                        maximum_temp = int(item.max_temp)
                        maximum_temp_day = item.date

                if item.low_temp != '':
                    if int(item.low_temp) < low_temp:
                        low_temp = int(item.low_temp)
                        low_temp_day = item.date

                if item.max_humid != '':
                    if int(item.max_humid) > max_humid:
                        max_humid = int(item.max_humid)
                        max_humid_day = item.date

        if maximum_temp_day != '':
            maximum_temp_day = datetime.strptime(maximum_temp_day, '%Y-%m-%d').strftime('%B %d')

        if low_temp_day != '':
            low_temp_day = datetime.strptime(low_temp_day, '%Y-%m-%d').strftime('%B %d')

        if max_humid_day != '':
            max_humid_day = datetime.strptime(max_humid_day, '%Y-%m-%d').strftime('%B %d')

        return CalculationResults(maximum_temp, maximum_temp_day, low_temp, low_temp_day, max_humid, max_humid_day)

    elif parameters[0] == '-a':
        date_params = parameters[1].split('/')
        year = int(date_params[0])
        month = datetime.strptime(parameters[1], '%Y/%m').strftime('%b')
        maximum_temp, low_temp, mean_humid, no_days = 0, 0, 0, 0

        for item in data_set:
            if (item.year == year) & (item.month == month):
                no_days += 1
                if item.max_temp != '':
                    maximum_temp += int(item.max_temp)

                if item.low_temp != '':
                    low_temp += int(item.low_temp)

                if item.mean_humid != '':
                    mean_humid += int(item.mean_humid)

        if maximum_temp > 0:
            maximum_temp = round(maximum_temp / no_days, 1)

        if low_temp > 0:
            low_temp = round(low_temp/no_days,1)

        if mean_humid > 0:
            mean_humid = round(mean_humid/no_days,1)

        return CalculationResults('', '', '', '', '', '', '', maximum_temp, low_temp, mean_humid,)

    elif parameters[0] == '-c':
        date_params = parameters[1].split('/')
        year = int(date_params[0])
        month = datetime.strptime(parameters[1], '%Y/%m').strftime('%b')
        complete_date = datetime.strptime(parameters[1], '%Y/%m').strftime('%B %Y')

        for item in data_set:
            if (item.year == year) & (item.month == month):
                day = datetime.strptime(item.date, '%Y-%m-%d').strftime('%d')
                max_temp, max_temp_str, low_temp, low_temp_str = '', '', '', ''

                max_temp = item.max_temp
                if max_temp != '':
                    for x in range(0, int(max_temp)):
                        max_temp_str += '+'
                else:
                    max_temp = '0'

                low_temp = item.low_temp
                if low_temp != '':
                    for x in range(0, int(low_temp)):
                        low_temp_str += '+'
                else:
                    low_temp = '0'

                output.append(CalculationResults(max_temp, '', low_temp, '', '', '', day, '', '', '', max_temp_str, low_temp_str, complete_date))

    return output


def report_generator(report, calculation_result):
    output_arr = []
    if report == '-e':
        output_arr.append('Highest: ' + str(calculation_result.max_temp) + 'C on ' + calculation_result.max_temp_day)
        output_arr.append('Lowest: ' + str(calculation_result.low_temp) + 'C on ' + calculation_result.low_temp_day)
        output_arr.append('Humidity: ' + str(calculation_result.max_humid) + '% on ' + calculation_result.max_humid_day)
    elif report == '-a':
        output_arr.append('Highest Average: ' + str(calculation_result.average_max_temp) + 'C')
        output_arr.append('Lowest Average: ' + str(calculation_result.average_low_temp) + 'C')
        output_arr.append('Average Mean Humidity: ' + str(calculation_result.average_mean_humid) + '%')
    elif report == '-c':
        for item in calculation_result:
            output_arr.append(str(item.day) + '\033[31m' + ' ' + item.max_temp_str + ' ' + item.max_temp + 'C')
            output_arr.append(str(item.day) + '\033[34m' + ' ' + item.low_temp_str + ' ' + item.low_temp + 'C')

        output_arr.append('\nBonus implementation single bar chart :')
        for item in calculation_result:
            remain_max_str = item.max_temp_str[len(item.low_temp_str):]
            output_arr.append(str(item.day) + '\033[34m' + ' ' + item.low_temp_str + '\033[31m' + ' ' + remain_max_str + '  \033[34m' + item.low_temp + 'C' + ' - \033[31m' + item.max_temp + 'C')

    print('Report Generated : \n')
    for output in output_arr:
        print(output)
    print('--------------------------------')


'''
Dictionary based data structure implementation
'''


# reading data from files and preparation data set
def data_dict_preparation(path='weatherfiles/*.txt'):
    files = glob.glob(path)
    data_set = {}

    for file in files:
        # extracting month and year from file name
        filename = file.replace(".txt", "")
        file_arr = filename.split('_')
        year = int(file_arr[-2])
        month = str(file_arr[-1])

        # setting defaults keys
        data_set.setdefault(year, {})
        data_set[year].setdefault(month, {})

        # traversing through file and storing data in data_set dictionary
        with open(file, "r") as fd:
            # read header row
            header_row = fd.readline().split(',')
            header_row = [x.strip() for x in header_row]
            # read data line by line
            month_arr = []
            for line in fd:
                line = line.strip().split(',')
                day_arr = {}
                for index in range(0, len(line)):
                    day_arr[header_row[index]] = line[index]

                month_arr.append(day_arr)

            data_set[year][month] = month_arr

    # sort data by year-wise
    sorted(data_set.keys())
    return data_set


# function for computation on data dictionary
def computation_dict_analysis(data_set, parameters):
    output_arr = {}
    if parameters[0] == '-e':
        maximum_temp, low_temp, max_humid = 0, 0, 0
        maximum_temp_day, low_temp_day, max_humid_day = '', '', ''
        data_dictionary = data_set[int(parameters[1])]

        for month in data_dictionary:
            for dict in data_dictionary[month]:
                if low_temp == 0:
                    if dict['Min TemperatureC'] != '':
                        low_temp = int(dict['Min TemperatureC'])

                if 'PKST' in dict:
                    date = dict['PKST']
                elif 'PKT' in dict:
                    date = dict['PKT']
                else:
                    date = ''

                if dict['Max TemperatureC'] != '':
                    if int(dict['Max TemperatureC']) > maximum_temp:
                        maximum_temp = int(dict['Max TemperatureC'])
                        maximum_temp_day = date

                if dict['Min TemperatureC'] != '':
                    if int(dict['Min TemperatureC']) < low_temp:
                        low_temp = int(dict['Min TemperatureC'])
                        low_temp_day = date

                if dict['Max Humidity'] != '':
                    if int(dict['Max Humidity']) > max_humid:
                        max_humid = int(dict['Max Humidity'])
                        max_humid_day = date

        maximum_temp_day = datetime.strptime(maximum_temp_day, '%Y-%m-%d').strftime('%B %d')
        low_temp_day = datetime.strptime(low_temp_day, '%Y-%m-%d').strftime('%B %d')
        max_humid_day = datetime.strptime(max_humid_day, '%Y-%m-%d').strftime('%B %d')

        output_arr['maximum_temp'] = maximum_temp
        output_arr['maximum_temp_day'] = maximum_temp_day
        output_arr['low_temp'] = low_temp
        output_arr['low_temp_day'] = low_temp_day
        output_arr['max_humid'] = max_humid
        output_arr['max_humid_day'] = max_humid_day
    elif parameters[0] == '-a':
        date_params = parameters[1].split('/')
        year = date_params[0]
        month = datetime.strptime(parameters[1], '%Y/%m').strftime('%b')
        data_dictionary = data_set[int(year)]
        maximum_temp, low_temp, mean_humid = 0, 0, 0
        no_days = len(data_dictionary[month])

        for dict in data_dictionary[month]:
            if dict['Max TemperatureC'] != '':
                maximum_temp += int(dict['Max TemperatureC'])

            if dict['Min TemperatureC'] != '':
                low_temp += int(dict['Min TemperatureC'])

            if dict['Mean Humidity'] != '':
                mean_humid += int(dict['Mean Humidity'])

        output_arr['highest_average'] = round(maximum_temp / no_days, 1)
        output_arr['lowest_average'] = round(low_temp / no_days, 1)
        output_arr['average_mean_humidity'] = round(mean_humid / no_days, 1)
    elif parameters[0] == '-c':
        date_params = parameters[1].split('/')
        year = date_params[0]
        month = datetime.strptime(parameters[1], '%Y/%m').strftime('%b')
        data_dictionary = data_set[int(year)]

        complete_date = datetime.strptime(parameters[1], '%Y/%m').strftime('%B %Y')
        output_arr['complete_date'] = complete_date

        for dict in data_dictionary[month]:
            day = datetime.strptime(dict['PKT'], '%Y-%m-%d').strftime('%d')
            maximum_temp, low_temp = '', ''

            temp = dict['Max TemperatureC']
            if temp != '':
                for x in range(0, int(temp)):
                    maximum_temp += '+'
            else:
                temp = '0'

            daily = {}
            daily['day'] = day
            daily['maximum_temp_str'] = maximum_temp
            daily['max_temp'] = temp

            temp = dict['Min TemperatureC']
            if temp != '':
                for x in range(0, int(temp)):
                    low_temp += '+'
            else:
                temp = '0'

            daily['low_temp_str'] = low_temp
            daily['low_temp'] = temp
            output_arr[int(day)] = daily

    return output_arr


# display the output
def dict_report_generator(report, result_set):
    output_arr = []
    if report == '-e':
        output_arr.append('Highest: ' + str(result_set['maximum_temp']) + 'C on ' + result_set['maximum_temp_day'])
        output_arr.append('Lowest: ' + str(result_set['low_temp']) + 'C on ' + result_set['low_temp_day'])
        output_arr.append('Humidity: ' + str(result_set['max_humid']) + '% on ' + result_set['max_humid_day'])
    elif report == '-a':
        output_arr.append('Highest Average: ' + str(result_set['highest_average']) + 'C')
        output_arr.append('Lowest Average: ' + str(result_set['lowest_average']) + 'C')
        output_arr.append('Average Mean Humidity: ' + str(result_set['average_mean_humidity']) + '%')
    elif report == '-c':
        output_arr.append(result_set['complete_date'])
        # handling the complete_date from going into loop
        result_set.pop('complete_date', None)

        for day in result_set:
            output_arr.append(str(day) + '\033[31m' + ' ' + result_set[day]['maximum_temp_str'] + ' ' + result_set[day][
                'max_temp'] + 'C')
            output_arr.append(
                str(day) + '\033[34m' + ' ' + result_set[day]['low_temp_str'] + ' ' + result_set[day]['low_temp'] + 'C')

    # display the report
    print('Report : \n')
    for output in output_arr:
        print(output)
    print('--------------------------------')

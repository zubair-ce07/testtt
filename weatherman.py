import glob
from termcolor import colored
import sys


# Function to Parse all files in the given directory path and populate them in a list of dictionaries
def parse_populate(path):
    data = []
    files = glob.glob(path)     # returns a list of all the files in the directory
    for file in files:
        with open(file, "r") as f:
            header = f.readline().split(",")

            for line in f:
                fields = line.split(",")
                entry = {}
                for index, value in enumerate(fields):
                    entry[header[index].strip()] = value.strip()

                data.append(entry)
    return data


# Function to set datatypes of multiple fields from str to int for future calculations and computations
def set_datatypes(data):
    for entry in data:
        for key in entry:
            if key == 'Max TemperatureC' or key == 'Min TemperatureC' or key == 'Max Humidity' \
                    or key == 'Min Humidity' or key == 'Mean TemperatureC' or key == 'Mean Humidity':
                if entry[key]:
                    entry[key] = int(entry[key])
    return data


# Function to extract data of the required date
def get_data(date, data):
    pkt = []
    date = date.replace('/', '-')   # in case the input date is of format yyyy/mm/dd instead of yyyy-mm-dd

    for entry in data:
        for key in entry:
            if key == 'PKT' and date in entry[key]:
                pkt.append(entry)
    return pkt


# Function to calculate the max, min Temperature and max Humidity and store them in a list
def calculate_min_max(query_data):
    max = 0
    min = 10000
    humid = 0
    result = []
    for entry in query_data:
        if entry['Max TemperatureC']:
            if entry['Max TemperatureC'] > max:
                max = entry['Max TemperatureC']
                max_date = entry['PKT']

        if entry['Min TemperatureC']:
            if entry['Min TemperatureC'] < min:
                min = entry['Min TemperatureC']
                min_date = entry['PKT']

        if entry['Max Humidity']:
            if entry['Max Humidity'] > humid:
                humid = entry['Max Humidity']
                humid_date = entry['PKT']

    result.append(max)
    result.append(max_date)
    result.append(min)
    result.append(min_date)
    result.append(humid)
    result.append(humid_date)

    return result


# Function to print out the stored calculations
def print_result(result):
    print('Highest: ' + str(result[0]) + 'C on ' + result[1])
    print('Lowest: ' + str(result[2]) + 'C on ' + result[3])
    print('Humidity: ' + str(result[4]) + '% on ' + result[5])
    print()


# Function to calculate mean averages and store the results in a list
def calculate_mean(query_data):
    mean_result = []
    max_avg_temp = 0
    min_avg_temp = 10000
    avg_humid = 0
    count = 0
    for entry in query_data:
        if entry['Mean TemperatureC']:
            if entry['Mean TemperatureC'] > max_avg_temp:
                max_avg_temp = entry['Mean TemperatureC']

        if entry['Mean TemperatureC']:
            if entry['Mean TemperatureC'] < min_avg_temp:
                min_avg_temp = entry['Mean TemperatureC']

        if entry['Mean Humidity']:
            if avg_humid == 0:
                avg_humid = entry['Mean Humidity']
                count +=1
            else:
                avg_humid = avg_humid + entry['Mean Humidity']
                count += 1

    avg_humid = avg_humid/count

    mean_result.append(max_avg_temp)
    mean_result.append(min_avg_temp)
    mean_result.append(avg_humid)

    return mean_result


# Function to print the Mean Averages
def print_mean_result(mean_result):
    print('Highest Average: ' + str(mean_result[0]) + 'C')
    print('Lowest Average: ' + str(mean_result[1]) + 'C')
    print('Average Mean Humidity: ' + str(mean_result[2]) + '%')
    print()


# Function to print horizontal bar charts of a given month
def generate_bar_chart(query_data):
    for entry in query_data:
        if entry['Max TemperatureC']:
            max_temp = entry['Max TemperatureC']

        if entry['Min TemperatureC']:
            min_temp = entry['Min TemperatureC']

        day = entry['PKT'].split(sep='-')[2]

    #     Sub-part 4
    #     print(day + ' ', end='')
    #     for i in range(max_temp):
    #         print(colored('+', 'red'), end='')
    #     print(' ' + str(max_temp) + 'C')
    #
    #     print(day + ' ', end='')
    #     for i in range(min_temp):
    #         print(colored('+', 'blue'), end='')
    #     print(' ' + str(min_temp) + 'C')

    # BONUS TASK
        print(day + ' ', end='')
        for i in range(min_temp):
            print(colored('+', 'blue'), end='')

        for i in range(max_temp):
            print(colored('+', 'red'), end='')
        print(' ' + str(min_temp) + 'C -', end='')
        print(' ' + str(max_temp) + 'C')


if __name__ == "__main__":
    num_of_inputs = len(sys.argv)
    path = sys.argv[1] + '/*.txt'

    # For testing without system arguments
    # argv = ['abc.py', 'path', '-c', '2006/8', '-a', '2006/8', '-e', '2006']
    # num_of_inputs = len(argv)
    # path = 'weatherfiles/*.txt'  #arg1

    data = parse_populate(path)
    data = set_datatypes(data)

    for i in range(2, num_of_inputs):
        if i % 2 == 0:
            report_type = sys.argv[i]   # '-e', '-a' or '-c'
            date = sys.argv[i+1]        # '2006', '2006/8'

            if '-e' in report_type:
                query_data = get_data(date, data)
                result = calculate_min_max(query_data)
                print_result(result)

            elif '-a' in report_type:
                query_data = get_data(date, data)
                mean_arr = calculate_mean(query_data)
                print_mean_result(mean_arr)

            elif '-c' in report_type:
                query_data = get_data(date, data)
                generate_bar_chart(query_data)

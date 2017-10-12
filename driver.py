import glob
import csv
from record import Record
from list import RecordList
import argparse


# Function to Parse all files in the given directory path and populate them in a list of dictionaries
def parse_populate(path):
    files = glob.glob(path)     # returns a list of all the files in the directory
    data = RecordList()
    for file in files:
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Record()
                record.add(row)
                data.add_record(record)
    return data


# Function to print out the stored calculations
def print_result(result):
    print('Highest: {}C on {}'.format(result[0], result[1]))
    print('Lowest: {}C on {}'.format(result[2], result[3]))
    print('Highest Humidity: {}% on {} \n'.format(result[4], result[5]))


# Function to print the Mean Averages
def print_mean_result(mean_result):
    print('Highest Average: {}C '.format(mean_result[0]))
    print('Lowest Average: {}C'.format(mean_result[1]))
    print('Average Mean Humidity: {} \n'.format(mean_result[2]))

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    parser.add_argument('-e', action="store", dest='date_minmax')
    parser.add_argument('-a', action="store", dest='date_mean')
    parser.add_argument('-c', action="store", dest='date_chart')
    args = parser.parse_args()
    path = args.dir + '/*.txt'

    data = parse_populate(path)

    if args.date_minmax:
        query_data = data.get_query_data(args.date_minmax)
        results = query_data.calculate_min_max()
        print_result(results)

    if args.date_mean:
        query_data = data.get_query_data(args.date_mean)
        mean_results = query_data.calculate_mean()
        print_mean_result(mean_results)

    if args.date_chart:
        query_data = data.get_query_data(args.date_chart)
        query_data.generate_bar_chart()




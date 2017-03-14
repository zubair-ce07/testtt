import csv
import glob
from datetime import date
import argparse
import sys

def main():
    #Main function to handle all the other function

    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="record the directory path for data fetching eg weather/weatherfiles"
                        )
    parser.add_argument("-y", help="display a required temperature for a year",
                        type=str)
    parser.add_argument("-m", help="display a required temperature for a month",
                        type=str)
    parser.add_argument("-d", help="display a required histogram for a month",
                        type=str)
    args = parser.parse_args()
    final_record_dict = main_record_dict()
    file_path = make_the_files_paths(args.m, args.y,sys.argv[1])
    file_reading_directory(file_path,final_record_dict)

    if args.y:
        find_the_max_min_temp_for_year(final_record_dict)
    elif args.m:
        find_the_average_temp_for_month(final_record_dict)
    elif args.d:
        file_path = make_the_files_paths(args.d, args.y,sys.argv[1])
        file_reading_directory(file_path,final_record_dict)
        histogram_charts_for_month(final_record_dict)


def main_record_dict():
    temp_matrix = {
        'PKT': [],
        'Max TemperatureC': [],
        'Min TemperatureC': [],
        'Max Humidity': [],
        'Mean Humidity': []
                    }

    return temp_matrix


def simplify_dates(temp_date):
    temp_date = temp_date.split('-')
    for x in temp_date:
        year = int(temp_date[0])
        month = int(temp_date[1])
        day = int(temp_date[2])
    return date(day=day, month=month, year=year).strftime('%A %d %B %Y')


def make_the_files_paths(month, year,directory):
    """
        Make the file path for the local directory

        Inputs:
                file_name: name and year
        Output:
                returns the path dict for further process
    """
    month_list = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    path_list = []

    if not month:
        path_list.extend(glob.glob("{}/Murree_weather_{}_*.txt".format(directory, year)))
    else:
        mon = month.split('/')
        path_list.extend(glob.glob(
            "{}/Murree_weather_{}_{}.txt" .format(directory,mon[0], month_list[int(mon[1])])))
    return path_list


def file_reading_directory(path_name,temperature_dictionary):
    """
        Get data from  weather files for max , min and humidity

        and append this data in global dictionary(temp_matrix)
        Inputs:
                file_name: path list dictionary
        Output:
                append the data in global dict.
    """
    for path in path_name:
        with open(path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temperature_dictionary['PKT'].append(row['PKT'])
                temperature_dictionary['Max TemperatureC'].append(row['Max TemperatureC'])
                temperature_dictionary['Min TemperatureC'].append(row['Min TemperatureC'])
                temperature_dictionary['Max Humidity'].append(row['Max Humidity'])
                temperature_dictionary['Mean Humidity'].append(row[' Mean Humidity'])


def find_the_max_min_temp_for_year(max_min_temperature):
    #Calculate the highest and lowest temperature with date of the day

    max_hum_date = []
    min_date_list = []
    max_date_list = []
    max_temp_list = []
    min_temp_list = []
    max_hum_list = []

    for mx_index, mx_data in enumerate(zip(max_min_temperature['Max TemperatureC'], max_min_temperature['PKT'])):
        if max_min_temperature['Max TemperatureC'][mx_index]:
            max_temp_list.append(int(mx_data[0]))
            max_date_list.append(max_min_temperature['PKT'][mx_index])

    for min_index, min_data in enumerate(zip(max_min_temperature['Min TemperatureC'], max_min_temperature['PKT'])):
        if max_min_temperature['Min TemperatureC'][min_index]:
            min_temp_list.append(int(min_data[0]))
            min_date_list.append(max_min_temperature['PKT'][min_index])

    for max_index, mx_data in enumerate(zip(max_min_temperature['Max Humidity'], max_min_temperature['PKT'])):
        if max_min_temperature['Max Humidity'][max_index]:
            max_hum_list.append(int(mx_data[0]))
            max_hum_date.append(max_min_temperature['PKT'][max_index])

    max_temperature = max(max_temp_list)
    min_temperature = min(min_temp_list)
    max_humidity = max(max_hum_list)
    max_temp_date = max_date_list[max_temp_list.index(max_temperature)]
    min_temp_date = min_date_list[min_temp_list.index(min_temperature)]
    mx_hum_date = max_hum_date[max_hum_list.index(max_humidity)]

    print '<--------------------------------------------------------->'
    print '1. Given year display the highest temperature and day,\n' \
          'lowest temperature and day, most humid day and humidity.'
    print '<--------------------------------------------------------->'

    print 'Highest: {}C On {}' .format(max_temperature, simplify_dates(max_temp_date))
    print 'Lowest :{}C On {}' .format(min_temperature, simplify_dates(min_temp_date))
    print 'Highest :{}% On {}' .format(max_humidity, simplify_dates(mx_hum_date))


def find_the_average_temp_for_month(average_temp):
    #Calculate the average highest,lowest and mean humid temperature

    mean_hum_list = []
    max_temp_list = []
    min_temp_list = []

    for mx_index, mx_data in enumerate(zip(average_temp['Max TemperatureC'], average_temp['PKT'])):
        if average_temp['Max TemperatureC'][mx_index]:
            max_temp_list.append(int(mx_data[0]))

    for min_index, min_data in enumerate(zip(average_temp['Min TemperatureC'], average_temp['PKT'])):
        if average_temp['Min TemperatureC'][min_index]:
            min_temp_list.append(int(min_data[0]))

    for mean_index, mean_data in enumerate(zip(average_temp['Mean Humidity'], average_temp['PKT'])):
        if average_temp['Mean Humidity'][mean_index]:
            mean_hum_list.append(int(mean_data[0]))

    print '2. Given month display the average highest temperature,\n' \
          'average lowest temperature, average mean humidity.'

    print '<----------------------------------------------------->'

    print 'Highest Average : {} C' .format(sum(max_temp_list) / len(max_temp_list))
    print 'Lowest Average : {} C' .format(sum(min_temp_list) / len(min_temp_list))
    print 'Average Mean Humidity :{} C'.format(sum(mean_hum_list) / len(mean_hum_list))


def histogram_charts_for_month(histogram_chart):
    #Make the histogram for the highest and lowest temperature

    print '<-------------------------------------------------------------->'
    print '3. For a given month draw two horizontal bar charts on the console \n' \
          'for the highest and lowest temperature on each day. Highest in red and lowest in blue.'

    min_date_list = []
    max_date_list = []
    max_temp_list = []
    min_temp_list = []

    for mx_index, mx_data in enumerate(zip(histogram_chart['Max TemperatureC'], histogram_chart['PKT'])):
        if histogram_chart['Max TemperatureC'][mx_index]:
            max_temp_list.append(int(mx_data[0]))
            max_date_list.append(histogram_chart['PKT'][mx_index])

    for min_index, min_data in enumerate(zip(histogram_chart['Min TemperatureC'], histogram_chart['PKT'])):
        if histogram_chart['Min TemperatureC'][min_index]:
            min_temp_list.append(int(min_data[0]))
            min_date_list.append(histogram_chart['PKT'][min_index])

    for max_date, min_date, max_value, min_value in (zip(max_date_list, min_date_list, max_temp_list, min_temp_list)):
        print max_date ,'+ '* max_value,'{}'.format(max_value),'\n',min_date,'- ' *min_value,'{}'.format(min_value)


    print '<----------------------------------------------------------------->'

    print '5. BONUS TASK. For a given month draw one horizontal bar chart on the console for \n' \
          'the highest and lowest temperature on each day. Highest in red and lowest in blue.'

    for temp_date, max_value, min_value in (zip(max_date_list, max_temp_list, min_temp_list)):
        print temp_date, '- ' * min_value, '+ ' * max_value, '{}C--{}C' .format(max_value, min_value)


if __name__ == '__main__':
    main()
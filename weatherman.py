import csv
import os
import sys
import datetime
import statistics as stat
import termcolor


def main():
    if len(sys.argv) < 4:
        print('usage: weatherman.py /path/to/files-dir flag date')
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print('Error: Incorrect folder path')
        sys.exit(1)
    valid_flags = ['-e', '-a', '-c']
    flags = sys.argv[2::2]
    dates = sys.argv[3::2]
    file_path = sys.argv[1]
    if not (correct_flags(flags, valid_flags) and
            equal_flags_and_dates(flags, dates)):
        sys.exit(1)
    all_files = [f for f in os.listdir(file_path) if
                 os.path.isfile(os.path.join(file_path, f)) and
                 f.endswith('.txt')]
    for tuple_ in zip(flags, dates):
        flag = tuple_[0]
        date = tuple_[1]
        if flag == '-e':
            year = to_int(date, None)
            if not year:
                print('\'' + date + '\' is not a valid date')
                sys.exit(1)
            month = 0
            month_alpha = ''
            if not is_valid_year(year, all_files):
                max_year, min_year = get_year_range(all_files)
                print('Error: Enter a date value between ' +
                      str(min_year) + ' and ' + str(max_year))
                sys.exit(1)
        else:
            if '/' not in date:
                print('Error: Invalid date format for \'' +
                      flag + '\' flag.')
                sys.exit(1)
            split_date = date.split('/')
            year = to_int(split_date[0], None)
            month = to_int(split_date[1], None)
            if year is None or month is None:
                print('\'' + date + '\' is not a valid date')
                sys.exit(1)
            month_alpha = get_month(month)
            if not date_supported(all_files, year, month):
                print('Error: Date not supported: ' + date)
                sys.exit(1)
        relevant_files = find_files(year, month_alpha, all_files)
        parse_files(flag, relevant_files, file_path)


def parse_files(flag, files, path):
    max_temp = {}
    min_temp = {}
    max_humid = {}
    mean_humid = {}
    for file in files:
        with open(path + '/' + file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if flag == '-a':
                    valid_key = row[get_valid_key(row, 'Max TemperatureC')]
                    populate(max_temp, flag, valid_key, '')
                    valid_key = row[get_valid_key(row, 'Min TemperatureC')]
                    populate(min_temp, flag, valid_key, '')
                    valid_key = row[get_valid_key(row, 'Mean Humidity')]
                    populate(mean_humid, flag, valid_key, '')
                else:
                    valid_key = row[get_valid_key(row, 'PKT')]
                    valid_value = row[get_valid_key(row, 'Max TemperatureC')]
                    populate(max_temp, flag, valid_key, valid_value)
                    valid_value = row[get_valid_key(row, 'Min TemperatureC')]
                    populate(min_temp, flag, valid_key, valid_value)
                    if flag == '-e':
                        valid_value = row[get_valid_key(row, 'Max Humidity')]
                        populate(max_humid, flag,
                                 valid_key, valid_value)
    if flag == '-a':
        max_temp_keys = list(max_temp.keys())
        min_temp_keys = list(min_temp.keys())
        mean_humid_keys = list(mean_humid.keys())
        print('\nHighest Average:', str(round(stat.mean(max_temp_keys))) +
              u'\u2103')
        print('Lowest Average:', str(round(stat.mean(min_temp_keys))) +
              u'\u2103')
        print('Average Mean Humidity:',
              str(round(stat.mean(mean_humid_keys))) + '%\n')
    elif flag == '-e':
        date, temp = return_val(max_temp, 'max')
        print('\nHighest:', str(temp) + u'\u2103', 'on', return_date(date))
        date, temp = return_val(min_temp, 'min')
        print('Lowest:', str(temp) + u'\u2103', 'on', return_date(date))
        date, humid = return_val(max_humid, 'max')
        print('Humidity:', str(humid) + '%', 'on', return_date(date) + '\n')
    elif flag == '-c':
        sorted_keys = sort_keys(max_temp)
        print_chart(max_temp, min_temp, sorted_keys, 'ordinary')
        print_chart(max_temp, min_temp, sorted_keys, 'special')
    return


def to_int(date, version):
    try:
        return int(date)
    except ValueError:
        return version


def get_valid_key(inp_dict, key):
    try:
        inp_dict[key]
        return key
    except KeyError:
        inp_dict[' ' + key]
        return ' ' + key


def populate(inp_dict, flag, key, value):
    if key:
        if flag == '-a':
            inp_dict[to_int(key, 0)] = value
        else:
            inp_dict[key] = to_int(value, 0)


def date_supported(all_files, year, month):
    if (is_valid_year(year, all_files) and
            is_valid_month(year, month, all_files)):
        return True
    return False


def correct_flags(flags, valid_flags):
    for flag in flags:
        if flag not in valid_flags:
            print('Invalid flag. Choose a valid flag from:' +
                  print_flags(valid_flags))
            return False
    return True


def equal_flags_and_dates(flags, dates):
    if len(flags) > len(dates):
        print('Error: Extra flag found in the input arguments.')
        return False
    elif len(flags) < len(dates):
        print('Error: Extra date found in the input arguments.')
        return False
    return True


def get_month(month):
    return datetime.date(1900, int(month), 1).strftime('%B')


def print_chart(max_bank, min_bank, sorted_keys, version):
    print('\n')
    sorted_dates = []
    split_key = []
    for key in sorted_keys:
        split_key = key.split('-')
        sorted_dates.append(split_key[2])
    print(get_month(split_key[1]), split_key[0])
    for i in range(0, len(sorted_dates)):
        date = str(sorted_dates[i])
        if len(date) == 1:
            date = '0' + date
        max_temp = max_bank[sorted_keys[i]]
        min_temp = min_bank[sorted_keys[i]]
        line_plus = '+' * max_temp
        line_minus = '+' * min_temp
        if version == 'ordinary':
            print(date, termcolor.colored(line_plus + ' ', 'red'),
                  str(max_temp) + u'\u2103')
            print(date, termcolor.colored(line_minus + ' ', 'blue'),
                  str(min_temp) + u'\u2103')
        elif version == 'special':
            print(date, termcolor.colored(line_minus, 'blue') +
                  termcolor.colored(line_plus, 'red'),
                  str(min_temp) + u'\u2103' + '  - ' + str(max_temp)
                  + u'\u2103')


def sort_keys(bank):
    keys = list(bank.keys())
    sorted_keys = []
    for key in keys:
        split_key = key.split('-')
        sorted_keys.append(int(split_key[2]))
    sorted_keys.sort()
    sorted_keys = [split_key[0] + '-' + split_key[1] + '-' + str(k)
                   for k in sorted_keys]
    return sorted_keys


def return_val(bank, version):
    val = 0
    if version == 'max':
        val = max(bank.values())
    elif version == 'min':
        val = min(bank.values())
    for key, value in bank.items():
        if val == value:
            return key, val


def return_date(date):
    date = date.split('-')
    return get_month(date[1]) + ' ' + date[2]


def find_files(year, month, files):
    relevant_files = []
    for file in files:
        if str(year) in file:
            if not month:
                relevant_files.append(file)
            elif month[:3] in file:
                relevant_files.append(file)
    return relevant_files


def print_flags(valid_flags):
    f = ''
    for flag in valid_flags:
        f += flag + ' '
    return f


def get_year_range(files):
    all_years = []
    for file in files:
        split_file = file.split('_')
        for word in split_file:
            if to_int(word, None) is not None:
                all_years.append(int(word))
    all_years.sort()
    max_year = all_years[-1]
    min_year = all_years[0]
    return max_year, min_year


def is_valid_year(year, files):
    max_year, min_year = get_year_range(files)
    if min_year <= year <= max_year:
        return True
    return False


def files_for_date(files, month, year):
    month_alpha = get_month(month)
    for file in files:
        split_file = file.split('_')
        if (split_file[2] == str(year) and
            month_alpha[:3] == split_file[3][:3]):
            return True
    return False


def is_valid_month(year, month, files):
    if 1 <= month <= 12:
        return files_for_date(files, month, year)
    return False


if __name__ == '__main__':
    main()

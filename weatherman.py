import os
import sys
import datetime
import statistics as stat
import termcolor


def main():
    valid_flags = ['-e', '-a', '-c']
    year = 0
    month_alpha = ''
    if len(sys.argv) < 4:
        print('usage: weatherman.py /path/to/files-dir flag date')
        sys.exit(1)
    elif not sys.argv[1].startswith('/'):
        print('Error: Use absolute path for directory containing files.')
        sys.exit(1)
    else:
        flags = sys.argv[2::2]
        dates = sys.argv[3::2]
        file_path = sys.argv[1]
        all_files = [f for f in os.listdir(file_path) if
                     os.path.isfile(os.path.join(file_path, f)) and
                     f.endswith('.txt')]
        for flag in flags:
            if flag not in valid_flags:
                print('Invalid flag. Choose a valid flag from:'+
                      print_flags(valid_flags))
                sys.exit(1)
        if len(flags) > len(dates):
            print('Error: Extra flag found in the input arguments.')
            sys.exit(1)
        elif len(flags) < len(dates):
            print('Error: Extra date found in the input arguments.')
            sys.exit(1)
        else:
            for i in range(0, len(flags)):
                flag = flags[i]
                if flag == '-e':
                    try:
                        year = int(dates[i])
                        month = 0
                        month_alpha = ''
                    except ValueError:
                        print('\''+dates[i]+'\' is not a valid date')
                        sys.exit(1)
                    if not is_valid_year(year, all_files):
                        max_year, min_year = get_year_range(all_files)
                        print('Error: Enter a date value between ' + 
                                str(min_year) + ' and ' + str(max_year))
                        sys.exit(1)
                elif flag == '-a' or flag == '-c':
                    if '/' not in dates[i]:
                        print('Error: Invalid date format for \''+
                              flag+'\' flag.')
                        sys.exit(1)
                    else:
                        date_ = dates[i].split('/')
                        try:
                            year = int(date_[0])
                            month = int(date_[1])
                            month_alpha = get_month(month)
                        except ValueError:
                            print('\'' + dates[i] + '\' is not a valid date')
                            sys.exit(1)
                        max_year, min_year = get_year_range(all_files)
                        if not (is_valid_year(year, all_files) and
                                is_valid_month(year, month, 
                                min_year, all_files)):
                            print('Error: Date not supported: '+dates[i])
                            sys.exit(1)
                relevant_files = find_files(year, month_alpha, all_files)
                parse_files(flag, relevant_files, file_path)


def parse_files(flag, files, path):
    max_temp = {}
    min_temp = {}
    max_humid = {}
    mean_humid = {}
    header_len = 0
    for file in files:
        in_file = open(path + '/' + file, 'r')
        lines = in_file.readlines()
        in_file.close()
        count = 1
        for line in lines:
            line_literals = line.split(',')
            if count == 1:
                header_len = len(line_literals)
                i_max_t = line_literals.index('Max TemperatureC')
                i_min_t = line_literals.index('Min TemperatureC')
                if flag == '-e':
                    humidity = ''
                    for word in line_literals:
                        if 'Mean Humidity' in word:
                            humidity = word
                    i_max_h = line_literals.index(humidity)
                elif flag == '-a':
                    humidity = ''
                    for word in line_literals:
                        if 'Mean Humidity' in word:
                            humidity = word
                    i_max_h = line_literals.index(humidity)
            else:
                if not len(line_literals) == header_len:
                    print('Some anomalous values on line', count)
                else:
                    date = line_literals[0]
                    if flag == '-a':
                        if line_literals[i_max_t]:
                            max_temp[int(line_literals[i_max_t])] = ''
                        if line_literals[i_min_t]:
                            min_temp[int(line_literals[i_min_t])] = ''
                        if line_literals[i_max_h]:
                            mean_humid[int(line_literals[i_max_h])] = ''
                    else:
                        if line_literals[i_max_t]:
                            max_temp[date] = int(line_literals[i_max_t])
                        if line_literals[i_min_t]:
                            min_temp[date] = int(line_literals[i_min_t])
                        if flag == '-e':
                            if line_literals[i_max_h]:
                                max_humid[date] = int(line_literals[i_max_h])
            count += 1
    if flag == '-a':
        max_temp_keys = list(max_temp.keys())
        min_temp_keys = list(min_temp.keys())
        mean_humid_keys = list(mean_humid.keys())
        print('\nHighest Average:', str(round(stat.mean(max_temp_keys)))+
              u'\u2103')
        print('Lowest Average:', str(round(stat.mean(min_temp_keys)))+
              u'\u2103')
        print('Average Mean Humidity:',
              str(round(stat.mean(mean_humid_keys)))+'%\n')
    elif flag == '-e':
        date, temp = return_val(max_temp, 'max')
        print('\nHighest:', str(temp)+u'\u2103', 'on', return_date(date))
        date, temp = return_val(min_temp, 'min')
        print('Lowest:', str(temp) + u'\u2103', 'on', return_date(date))
        date, humid = return_val(max_humid, 'max')
        print('Humidity:', str(humid) + '%', 'on', return_date(date)+'\n')
    elif flag == '-c':
        sorted_keys = sort_keys(max_temp)
        print_chart(max_temp, min_temp, sorted_keys, 'ordinary')
        print_chart(max_temp, min_temp, sorted_keys, 'special')
    return


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
            date = '0'+date
        max_temp = max_bank[sorted_keys[i]]
        min_temp = min_bank[sorted_keys[i]]
        line_plus = '+' * max_temp
        line_minus = '+' * min_temp
        if version == 'ordinary':
            print(date, termcolor.colored(line_plus+' ', 'red'), 
                str(max_temp) + u'\u2103')
            print(date, termcolor.colored(line_minus+' ', 'blue'), 
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
    sorted_keys = [split_key[0]+'-'+split_key[1]+'-'+str(k)
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
    month_alpha = get_month(date[1])
    return month_alpha+' '+date[2]


def find_files(year, month, files):
    relevant_files = []
    for file in files:
        if str(year) in file:
            if not month:
                relevant_files.append(file)
            else:
                if month[:3] in file:
                    relevant_files.append(file)
    return relevant_files


def print_flags(valid_flags):
    f = ''
    for flag in valid_flags:
        f += flag + ' '
    return f


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def get_year_range(files):
    all_years = []
    for file in files:
        split_file = file.split('_')
        for word in split_file:
            if is_int(word):
                all_years.append(int(word))
    all_years.sort()
    max_year = all_years[-1]
    min_year = all_years[0]
    return max_year, min_year


def is_valid_year(year, files):
    max_year, min_year = get_year_range(files)
    if year >= min_year and year <= max_year:
        return True
    return False


def files_present(files, month, year):
    all_months = []
    month_alpha = get_month(month)
    for file in files:
        split_file = file.split('_')
        if(split_file[2] == str(year)):
            if month_alpha[:3] == split_file[3][:3]:
                return True


def is_valid_month(year, month, min_year, files):
    if month >= 1 and month <= 12:
        return files_present(files, month, year)
    return False


if __name__ == '__main__':
    main()

import os
import sys
import datetime


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
                print('Invalid flag. Choose a valid flag from:'+print_flags(valid_flags))
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
                        month_alpha = ''
                    except ValueError:
                        print('\''+dates[i]+'\' is not a valid date')
                        sys.exit(1)
                    if not is_valid_year(year):
                        print('Error: Enter a date value between 2004 and 2016.')
                        sys.exit(1)
                elif flag == '-a' or flag == '-c':
                    if '/' not in dates[i]:
                        print('Error: Invalid date format for \''+flag+'\' flag.')
                        sys.exit(1)
                    else:
                        date_ = dates[i].split('/')
                        try:
                            year = int(date_[0])
                            month = int(date_[1])
                            month_alpha = datetime.date(1900, month, 1).strftime('%B')
                        except ValueError:
                            print('\'' + dates[i] + '\' is not a valid date')
                            sys.exit(1)
                        if not (is_valid_year(year) and is_valid_month(month)):
                            print('Error: Date not supported: '+dates[i])

                relevant_files = find_files(year, month_alpha, all_files)
                print(flag, year, month_alpha, 'Length: ', len(relevant_files))
                parse_files(flag, year, month_alpha, relevant_files, file_path)


def parse_files(flag, year, month, files, path):
    max_temp = {}
    min_temp = {}
    max_humid = {}
    # helper = []
    if flag == '-e':
        for file in files:
            in_file = open(path+'/'+file, 'r')
            lines = in_file.readlines()
            # print(lines)
            count = 1
            for line in lines:
                line_literals = line.split(',')
                if count == 1:
                    header_len = len(line_literals)
                    i_max_t = line_literals.index('Max TemperatureC')
                    i_min_t = line_literals.index('Min TemperatureC')
                    i_max_h = line_literals.index('Max Humidity')
                else:
                    if not len(line_literals) == header_len:
                        print('Some anomalous values on line', count)
                        # i_max_temp = line
                    else:
                        date = line_literals[0]
                        max_temp[date] = int(line_literals[i_max_t])
                        min_temp[date] = int(line_literals[i_min_t])
                        max_humid[date] = int(line_literals[i_max_h])
                count += 1
        val = max(max_temp.values())
        # print(max_temp.values())
        # print(val)
        for key, value in max_temp.items():
            if val == value:
                print(key)
    # elif flag == '-a'
    # print(type(files))
    # for
    return


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


def is_valid_year(year):
    MAX_YEAR = 2016
    MIN_YEAR = 2004
    if year >= MIN_YEAR and year <= MAX_YEAR:
        return True
    return False


def is_valid_month(month):
    if month >= 1 and month <= 12:
        return True
    return False

# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
if __name__ == '__main__':
    main()
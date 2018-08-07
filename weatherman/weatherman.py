import argparse
import glob


def arg_parse():
    """
    Two arguments are taken from the user and stored in 'report_no' and 'data_dir'.
    nargs='?' is used to prevent error in case one or no argument is provided.
    Returns:
        It returns the 'report_no' and 'data_dir'.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('report', nargs='?')
    parser.add_argument('data', nargs='?')
    args = parser.parse_args()
    report_no = args.report
    data_dir = args.data

    return report_no, data_dir


def file_list_func(data_dir):
    """
    The file_list_func() returns a sorted file list in a given directory.
    If the given directory does no exists, it returns an empty array.
    args:
        data_dir: This is the location of the files.
    return:
        file_list: This is the list of all files.
    """
    file_list = (glob.glob(data_dir + "/*.txt"))
    file_list.sort()
    return file_list


def display_report_table(report_no):
    """
    The display_report_table() displays the report table according to the 'report _no'.
    args:
        report_no: This is the report number provided by the user
    """
    if report_no is '1':
        print('\033[1m' + '\n1. Annual Max/Min Temp:\n' + '\033[0m')
        print('\tYear\tMax Temp\tMin Temp\tMax Humidity\tMin Humidity\n\t' + '-' * 68)

    elif report_no is '2':
        print('\033[1m' + '\n2. Hottest day of each year\n' + '\033[0m')
        print('\tYear\tDate\t\tTemp\n\t' + '-' * 28)


def max_temp_func(new_temp, old_temp, new_date, old_date):
    """
    The max_temp_func() compares two temperature values and returns the greater one.
    args:
        new_temp: This is the new temperature value to be compared.
        old_temp: This is currently the highest temperature value of the year.
        new_date: This is the date on which the new temperature occurred.
        old_date: This is the date of the greatest temperature.
    returns:
        new_temp: 'new_temp is returned if it is greater than 'old_temp'.
        old_temp: 'old_temp is returned if it is greater than 'new_temp'.
        new_date: This is returned with 'new_temp'.
        old_date: This is returned with 'new_temp'.
    """
    if new_temp > old_temp:
        return new_temp, new_date
    else:
        return old_temp, old_date


def min_temp_func(new_temp, old_temp):
    """
    The min_temp_func() compares two temperature values and returns the smaller one.
    args:
        new_temp: This is the new temperature value to be compared.
        old_temp: This is currently the lowest temperature value of the year.
    returns:
        new_temp: 'new_temp is returned if it is smaller than 'old_temp'.
        old_temp: 'old_temp is returned if it is smaller than 'new_temp'.
    """
    if new_temp < old_temp:
        return new_temp
    else:
        return old_temp


def max_humid_func(new_humid, old_humid):
    """
    The max_humid_func() compares two humidity values and returns the greater one.
    args:
        new_humid: This is the new humidity value to be compared.
        old_humid: This is currently the greatest humidity value of the year.
    returns:
        new_humid: 'new_humid is returned if it is greater than 'old_humid'.
        old_humid: 'old_humid is returned if it is greater than 'new_humid'.
    """
    if new_humid > old_humid:
        return new_humid
    else:
        return old_humid


def min_humid_func(new_humid, old_humid):
    """
    The min_humid_func() compares two humidity values and returns the smaller one.
    args:
        new_humid: This is the new humidity value to be compared.
        old_humid: This is currently the lowest humidity value of the year.
    returns:
        new_humid: 'new_humid is returned if it is smaller than 'old_humid'.
        old_humid: 'old_humid is returned if it is smaller than 'new_humid'.
    """
    if new_humid < old_humid:
        return new_humid
    else:
        return old_humid


def reset_val_func():
    """
    The reset_val_func() resets the value of three variables by returning certain values.
    return:
        0 is returned for maximum value, 1000 for minimum and '0' for the date.
        When date is not required to reset, the 'useless' variable is used.
    """
    return 0, 1000, '0'


def temp_calc_func(f, max_temp, min_temp, max_humid, min_humid, date):
    """
    The temp_calc_func() calculates the highest and lowest temperature and humidity in a given file.
    args:
        f: This is the file in which all values are present.
        max_temp: This is the maximum temperature.
        min_temp: This is the minimum temperature.
        max_humid: This is the maximum humidity.
        min_humid: This is the minimum humidity.
        date: This is the date on which 'max_temp' occurred.
    returns:
        max_temp: This is the updated maximum temperature.
        min_temp: This is the updated minimum temperature.
        max_humid: This is the updated maximum humidity.
        min_humid: This is the updated minimum humidity.
        date: This is the updated date on which 'max_temp' occurred.
    """
    for line in f:
        arr_line = [x for x in line.split(',')]
        if arr_line[0][0].isdigit():
            if arr_line[1].isdigit():
                max_temp, date = max_temp_func(int(arr_line[1]), max_temp, arr_line[0], date)

            if arr_line[3].isdigit():
                min_temp = min_temp_func(int(arr_line[3]), min_temp)

            if arr_line[7].isdigit():
                max_humid = max_humid_func(int(arr_line[7]), max_humid)

            if arr_line[9].isdigit():
                min_humid = min_humid_func(int(arr_line[9]), min_humid)

    return max_temp, min_temp, max_humid, min_humid, date


def display_report(report_no, max_temp, min_temp, max_humid, min_humid, date, last_year):
    if report_no is '1':
        print('\t{}\t{}\t\t{}\t\t{}\t\t{}'.format(last_year, max_temp, min_temp, max_humid,
                                                  min_humid))
    elif report_no is '2':
        format_date = [x for x in date.split('-')]
        print('\t{}\t{}/{}/{}\t{}'.format(last_year, format_date[2], format_date[1],
                                          format_date[0], max_temp))


def no_para_func():
    """
    The no_para_func() displays the programs usage information when the report number is invalid
    or the directory provided is wrong.
    :return:
    """
    print("Usage: weatherman\n<report#>\n<data_dir>\n\n[Report #]\n1 for Annual Max/Min Temperature\n"
          "2 for Hottest day of each year\n\n[data_dir]\n"
          "Directory containing weather data files\n")


def main():
    # The report number and data directory is provided by the user.
    report_no, data_dir = arg_parse()

    # All files from the directory are stored in 'file_list' in form of list.
    file_list = file_list_func(data_dir)

    # Check if the report number is valid and the directory provided is correct.
    if file_list and report_no in ('1', '2'):

        # Store the first year of the data in 'last_year' for future reference.
        last_year = file_list[0][33: 37]

        # Displays the report table according to the 'report _no'.
        display_report_table(report_no)

        # Reset the values of the variables.
        max_temp, min_temp, date = reset_val_func()
        max_humid, min_humid, useless = reset_val_func()

        # Open all files in the list.
        for file in file_list:
            with open(file) as f:

                # Store current file year in 'year'.
                year = f.name[33: 37]

                # If the next year has started, display result of previous year and reset values.
                if year not in last_year:
                    display_report(report_no, max_temp, min_temp, max_humid, min_humid, date, last_year)
                    last_year = year

                    max_temp, min_temp, date = reset_val_func()
                    max_humid, min_humid, useless = reset_val_func()

                # If it is current year, update the values.
                elif year in last_year:
                    max_temp, min_temp, max_humid, min_humid, date = temp_calc_func(f, max_temp, min_temp, max_humid,
                                                                                    min_humid, date)
    # If invalid report number or the wromg directory is provided, run no_para_func()
    else:
        no_para_func()


if __name__ == "__main__":
    main()

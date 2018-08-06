import os
import argparse


def max_value_func(new_value, old_value, new_date, old_date):
    """
    The max_value_func() compares two variables.
    Args:
        new_value: This is the new value.
        old_value: This is the currently greatest value.
        new_date:  This is the new value.
        old_date:  This is the date of th greatest value.
    Returns:
        It returns the greater value along with it's corresponding date.

    """
    if new_value > old_value:
        return new_value, new_date
    else:
        return old_value, old_date


def min_value_func(new_value, old_value):
    """
    The min_value_func() is similar to the max_value_func.
    Args:
        new_value: This is the new value.
        old_value: This is the currently minimum value.
    Returns:
        It returns the smallest value.

    """
    if new_value < old_value:
        return new_value
    else:
        return old_value


def reset_val_func():
    """
    The reset_val_func() resets the value of three variables by returning certain values.
    return:
        0 is returned for maximum value, 1000 for minimum and '0' for the date.
        When date is not required to reset, the 'useless' variable is used.
    """
    return 0, 1000, '0'


def main():
    """
    Two arguments are taken from the user and stored in 'report_no' and 'data_dir'.
    nargs='?' is used to prevent error in case one or no argument is provided.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('report', nargs='?')
    parser.add_argument('data', nargs='?')
    args = parser.parse_args()
    report_no = args.report
    data_dir = args.data

    # If no argument is provided, a random 'string value' is stored in 'data_dir'
    # as an empty string will give error when used in built-in functions.
    if data_dir is None:
        data_dir = 'string value'

    # Two arrays for month and year are declared to access files within the directory.
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]

    # Two counters for 'month' and 'year' array are declared and set to 0.
    month_count = 0
    year_count = 0

    # All values are reset using 'reset_val_func()'.
    max_temp, min_temp, useless = reset_val_func()
    max_humid, min_humid, useless = reset_val_func()
    max_temp, useless, date = reset_val_func()

    # checking if directory exists.
    if os.path.isdir(data_dir):

        # Checking the report number.
        if report_no is '1':
            print('\033[1m' + '\n1. Annual Max/Min Temp:\n' + '\033[0m')
            print('\tYear\tMax Temp\tMin Temp\tMax Humidity\tMin Humidity\n\t' + '-' * 68)

            # The size of year array is 16 so a loop is set for that limit.
            while year_count < 16:

                # The size of month array is 12.
                if month_count < 12:

                    # If current file does not exists, continue to next month.
                    if not os.path.isfile('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count],
                                                                               month[month_count])):
                        month_count += 1
                        continue

                    # If current file exists, read it line by line and store it in 'arr_line'.
                    with open('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count], month[month_count]),
                              'r') as f:
                        for line in f:
                            arr_line = [x for x in line.split(',')]

                            # Check if the first value in the line (date) is a digit. The rest of the lines are ignored.
                            if arr_line[0][0].isdigit():

                                # The maximum temperature is stored in 'max_temp'. Since date is not required
                                # in this report, it is stored in 'useless'.
                                if arr_line[1].isdigit():
                                    max_temp, useless = max_value_func(int(arr_line[1]), max_temp, useless, useless)

                                # The minimum temperature is stored in 'mim_temp'.
                                if arr_line[3].isdigit():
                                    min_temp = min_value_func(int(arr_line[3]), min_temp)

                                if arr_line[7].isdigit():
                                    max_humid, useless = max_value_func(int(arr_line[7]), max_humid, useless, useless)

                                if arr_line[9].isdigit():
                                    min_humid = min_value_func(int(arr_line[9]), min_humid)

                    # Increment month_counter to open next month's file and close this one.
                    month_count += 1
                    f.close()

                # If month_count exceeds limit, it means all the files for this year have been checked.
                # Display the values, increment year count to move to next year and reset remaining values.
                if month_count > 11:
                    print('\t{}\t{}\t\t{}\t\t{}\t\t{}'.format(year[year_count], max_temp, min_temp, max_humid,
                                                              min_humid))
                    month_count = 0
                    year_count += 1
                    max_temp, min_temp, useless = reset_val_func()
                    max_humid, min_humid, useless = reset_val_func()

        # Check report number.
        elif report_no is '2':
            print('\033[1m' + '\n2. Hottest day of each year\n' + '\033[0m')
            print('\tYear\tDate\t\tTemp\n\t' + '-' * 28)

            while year_count < 16:

                if month_count < 12:

                    if not os.path.isfile('{}/lahore_weather_{}_{}.txt'.format(data_dir, year[year_count],
                                                                               month[month_count])):
                        month_count += 1
                        continue

                    with open("{}/lahore_weather_{}_{}.txt".format(data_dir, year[year_count], month[month_count]),
                              'r') as f:
                        for line in f:
                            arr_line = [x for x in line.split(',')]

                            if arr_line[0][0].isdigit():

                                # The maximum temperature is stored in 'max_temp' and it's corresponding date in 'date'.
                                if arr_line[1].isdigit():
                                    max_temp, date = max_value_func(int(arr_line[1]), max_temp, arr_line[0], date)

                    month_count += 1
                    f.close()

                if month_count > 11:
                    format_date = [x for x in date.split('-')]
                    print('\t{}\t{}/{}/{}\t{}'.format(year[year_count], format_date[2], format_date[1], format_date[0],
                                                      max_temp))
                    month_count = 0
                    year_count += 1
                    max_temp, useless, date = reset_val_func()
    # If the directory provided does not exist, report number is invalid of fewer parameters are provided
    # then display usage information.
    if not os.path.isdir(data_dir) or report_no not in ('1', '2'):
        print("Usage: weatherman\n<report#>\n<data_dir>\n\n[Report #]\n1 for Annual Max/Min Temperature\n"
              "2 for Hottest day of each year\n\n[data_dir]\n"
              "Directory containing weather data files\n")


if __name__ == "__main__":
    main()

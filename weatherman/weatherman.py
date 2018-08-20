import argparse
import os
import csv


class Weather:
    max_temp = 0
    min_temp = 100
    max_humid = 0
    min_humid = 100
    date = '0'

    year_array = []
    year_count = 0

    def get_user_input(self):
        """
        Two arguments are taken from the user and stored in 'report_no' and 'data_dir'.
        nargs='?' is used to prevent error in case one or no argument is provided.
        If no directory is provided by the user, store a 'Random string' in 'data_dir' to avoid errors from built in
        functions.
        Returns:
            report_no: Report number entered by the user.
            data_dir: The directory of the files.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('report', nargs='?')
        parser.add_argument('data', nargs='?', default='Random string')
        args = parser.parse_args()
        report_no = args.report
        data_dir = args.data

        return report_no, data_dir

    def get_file_list(self, data_dir):
        """
        This function returns a sorted file list in a given directory.
        If the given directory does no exists, it returns an empty array.
        args:
            data_dir: Location of the files.
        return:
            file_list: List of all files.
        """

        if os.path.isdir(data_dir):
            file_list = os.listdir(data_dir)
            file_list.sort()
            return file_list

        else:
            return False

    def display_report_table(self, report_no):
        """
        Called to displays the report table according to the 'report _no'.
        args:
            report_no: Report number provided by the user.
        """
        if report_no is '1':
            print('\033[1m' + '\n1. Annual Max/Min Temp:\n' + '\033[0m')
            print('\tYear\tMax Temp\tMin Temp\tMax Humidity\tMin Humidity\n\t' + '-' * 68)

        elif report_no is '2':
            print('\033[1m' + '\n2. Hottest day of each year\n' + '\033[0m')
            print('\tYear\tDate\t\tTemp\n\t' + '-' * 28)

    def get_max_temp(self, temp, greatest_temp, date, greatest_date):
        """
        This function compares two temperature values and returns the greater one.
        args:
            temp: This is the new temperature value to be compared.
            greatest_temp: This is currently the highest temperature value of the year.
            date: This is the date on which the new temperature occurred.
            greatest_date: This is the date of the greatest temperature.
        returns:
            temp: This is returned if it is greater than 'greatest_temp'.
            greatest_temp: Else this is returned.
            date: This is returned with 'temp'.
            greatest_date: This is returned with 'greatest_temp'.
        """
        if int(temp) > greatest_temp:
            return int(temp), date
        else:
            return greatest_temp, greatest_date

    def get_min_temp(self, temp, lowest_temp):
        """
        This function compares two temperature values and returns the smaller one.
        args:
            temp: This is the new temperature value to be compared.
            lowest_temp: This is currently the lowest temperature value of the year.
        returns:
            temp: This is returned if it is smaller than 'lowest_temp'.
            lowest_temp: This is returned if it is smaller than 'temp'.
        """
        if int(temp) < lowest_temp:
            return int(temp)
        else:
            return lowest_temp

    def get_max_humid(self, humid, greatest_humid):
        """
        This function compares two humidity values and returns the greater one.
        args:
            humid: This is the new humidity value to be compared.
            greatest_humid: This is currently the greatest humidity value of the year.
        returns:
            humid: This is returned if it is greater than 'greatest_humid'.
            greatest_humid: 'This is returned if it is greater than 'humid'.
        """
        if int(humid) > greatest_humid:
            return int(humid)
        else:
            return greatest_humid

    def get_min_humid(self, humid, lowest_humid):
        """
        This function compares two humidity values and returns the smaller one.
        args:
            humid: This is the new humidity value to be compared.
            lowest_humid: This is currently the lowest humidity value of the year.
        returns:
            humid: This is returned if it is smaller than 'lowest_humid'.
            lowest_humid: This is returned if it is smaller than 'humid'.
        """
        if int(humid) < lowest_humid:
            return int(humid)
        else:
            return lowest_humid

    def reset_temp_and_humid(self):
        """
        This function resets the value of three variables by returning certain values.
        return:
            0 is returned for maximum value, 100 for minimum and '0' for the date.
            When date is not required to reset, the 'useless' variable is used.
        """
        return 0, 100, '0'

    def get_weather(self, weather_file, report_no):
        """

        calculates the highest and lowest temperature and humidity in a given file.
        args:
            weather_file: This is the file in which all values are present.
            report_no: Report number provided by the user.
        """
        for line in weather_file:
            if line:
                if 'PKT' in line:
                    year = line['PKT']
                else:
                    year = line['PKST']

                if year[0:4].isdigit():
                    # If year_array is empty, append the first year into it.
                    if not Weather.year_array:
                        Weather.year_array.append(year[0:4])

                    # If year does not exist in year_array, append it and display values of the previous year.
                    if year[0:4] not in Weather.year_array:
                        Weather.year_array.append(year[0:4])

                        Weather.display_report(self, report_no)

                        Weather.year_count += 1

                        Weather.max_temp, Weather.min_temp, Weather.date = Weather.reset_temp_and_humid(self)

                        Weather.max_humid, Weather.min_humid, Weather.useless = Weather.reset_temp_and_humid(self)

                    # If year exists in year array, calculate the temperature values.
                    else:
                        if line['Max TemperatureC']:
                            Weather.max_temp, Weather.date = Weather.get_max_temp(self, line['Max TemperatureC'],
                                                                                  Weather.max_temp, year, Weather.date)

                        if line['Min TemperatureC']:
                            Weather.min_temp = Weather.get_min_temp(self, line['Min TemperatureC'], Weather.min_temp)

                        if line['Max Humidity']:
                            Weather.max_humid = Weather.get_max_humid(self, line['Max Humidity'], Weather.max_humid)

                        if line[' Min Humidity']:
                            Weather.min_humid = Weather.get_min_humid(self, line[' Min Humidity'], Weather.min_humid)

    def display_report(self, report_no):
        """
        Display the weather report
        """
        if report_no is '1':
            print('\t{}\t{}\t\t{}\t\t{}\t\t{}'.format(Weather.year_array[Weather.year_count], Weather.max_temp,
                                                      Weather.min_temp, Weather.max_humid, Weather.min_humid))
        elif report_no is '2':
            format_date = [x for x in Weather.date.split('-')]
            print('\t{}\t{}/{}/{}\t{}'.format(Weather.year_array[Weather.year_count], format_date[2], format_date[1],
                                              format_date[0], Weather.max_temp))

    def display_usage_info(self):
        """
        The no_para_func() displays the programs usage information when the report number is invalid
        or the directory provided is wrong.
        """
        print("Usage: weatherman\n<report#>\n<data_dir>\n\n[Report #]\n1 for Annual Max/Min Temperature\n"
              "2 for Hottest day of each year\n\n[data_dir]\n"
              "Directory containing weather data files\n")


def main():
    # Make weather dictionary object.
    weatherman = Weather()

    # The report number and data directory is provided by the user.
    report_no, data_dir = weatherman.get_user_input()

    # All files from the directory are stored in 'file_list' in form of list.
    file_list = weatherman.get_file_list(data_dir)

    # Check if the report number is valid and the directory provided is correct.
    if file_list and report_no in ('1', '2'):

        # Displays the report table according to the 'report _no'.
        weatherman.display_report_table(report_no)

        # Open all files in the list.
        for file in file_list:
            with open(data_dir + '/' + file) as csv_file:
                # Move to next line as first line is empty and DictReader will not work properly.
                csv_file.seek(2)
                weather_file = csv.DictReader(csv_file)
                weatherman.get_weather(weather_file, report_no)
            csv_file.close()

        # Display report for last year as it is not shown in the loop.
        weatherman.display_report(report_no)

    # If invalid report number or the wrong directory is provided, run no_para_func()
    else:
        weatherman.display_usage_info()


if __name__ == "__main__":
    main()

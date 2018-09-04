import sys
import datetime
import calendar
import calculations
import filehandler


class OutputGenerator:
    '''
        This class provides methods to display reports on console
    '''
    dir_path = ''
    results = calculations.WeatherCalculations()
    files = filehandler.FileHandler()

    def print_e_output(self, filter):
        '''
            This method prints weather report for -e argument
        '''

        all_file_names = self.files.get_txt_files_list(self.dir_path)
        filtered_file_names = self.files.filter_list_by(
            all_file_names, filter)

        result = self.results.get_highest_temparature_recored(
            filtered_file_names)
        datee = datetime.datetime.strptime(result['PKT'], "%Y-%m-%d")
        print('Highest: {temp}C on {month} {day}'.format(
            temp=result['MaxTemperatureC'],
            month=calendar.month_name[datee.month], day=datee.day))

        result = self.results.get_lowest_temparature_recored(
            filtered_file_names)
        datee = datetime.datetime.strptime(result['PKT'], "%Y-%m-%d")
        print('Lowest: {temp}C on {month} {day}'.format(
            temp=result['MinTemperatureC'],
            month=calendar.month_name[datee.month], day=datee.day))

        result = self.results.get_highest_humidity_recored(filtered_file_names)
        datee = datetime.datetime.strptime(result['PKT'], "%Y-%m-%d")
        print('Humidity: {temp}% on {month} {day}'.format(
            temp=result['MaxHumidity'], month=calendar.month_name[datee.month],
            day=datee.day))

    def print_a_output(self, filter):
        '''
            This method prints weather report for -a argument
        '''

        all_file_names = self.files.get_txt_files_list(self.dir_path)
        filtered_file_names = self.files.filter_list_by(
            all_file_names, self.results.get_a_fiter(filter))
        if(len(filtered_file_names) > 0):
            print("Highest Average: {temp}C".format(
                temp=int(self.results.get_average_highest_temp(
                    filtered_file_names[0]))))
            print("Lowest Average: {temp}C".format(
                temp=int(self.results.get_average_lowest_temp(
                    filtered_file_names[0]))))
            print("Average Mean Humidity: {temp}C".format(
                temp=int(self.results.get_average_mean_humidity_temp(
                    filtered_file_names[0]))))

    def print_c_output(self, date):
        '''
            This method prints weather report for -c argument
        '''

        all_file_names = self.files.get_txt_files_list(self.dir_path)
        filtered_file_names = self.files.filter_list_by(
            all_file_names, self.results.get_a_fiter(date))
        if(len(filtered_file_names) > 0):
            low_temp_record = self.results.get_low_temp_record(
                all_file_names[0])
            high_temp_record = self.results.get_high_temp_record(
                all_file_names[0])

            date = datetime.datetime.strptime(date, "%Y/%m")
            print(calendar.month_name[date.month], date.year)

            for counter in range(len(high_temp_record)):
                print('\033[3;37;48m{:02d}'.format(counter+1), end=' ')
                print('\033[0;31;48m+' * high_temp_record[counter+1], end=' ')
                print('\033[3;37;48m{temp}C'.format(
                    temp=high_temp_record[counter+1]))

                print('\033[3;37;48m{:02d}'.format(counter+1), end=' ')
                print('\033[0;34;48m+' * low_temp_record[counter+1], end=' ')
                print('\033[3;37;48m{temp}C'.format(
                    temp=low_temp_record[counter+1]))
            print('\033[0;37;48m')

    def print_c_output_bounus(self, date):
        '''
            This method prints weather report for -c argument
        '''

        all_file_names = self.files.get_txt_files_list(self.dir_path)
        filtered_file_names = self.files.filter_list_by(
            all_file_names, self.results.get_a_fiter(date))
        if(len(filtered_file_names) > 0):
            low_temp_record = self.results.get_low_temp_record(
                all_file_names[0])
            high_temp_record = self.results.get_high_temp_record(
                all_file_names[0])

            date = datetime.datetime.strptime(date, "%Y/%m")
            print(calendar.month_name[date.month], date.year)

            for counter in range(len(high_temp_record)):
                print('\033[3;37;48m{:02d}'.format(counter+1), end=' ')
                print('\033[0;34;48m+' * low_temp_record[counter+1], end='')
                print('\033[0;31;48m+' * high_temp_record[counter+1], end=' ')
                print('\033[3;37;48m{templow}C {temphigh}C'.format(
                    templow=low_temp_record[counter+1],
                    temphigh=high_temp_record[counter+1]))
            print('\033[0;37;48m')

#!/usr/bin/python3

import calendar
import datetime
import filehandler as files


class WeatherCalculations:
    '''
    This class perform calculation to create weather report
    '''

    def get_highest_temparature_recored(self, file_names_list):
        '''
        This method takes list of paths and return the recordof a day
        that have highest temperature.
        '''

        max_temperature_recored = dict()
        max_temperature = -273
        temp = -273
        for file_name in file_names_list:
            with open(file_name) as current_file:
                keys = current_file.readline().rstrip()\
                    .replace(' ', '').split(',')

                for line in current_file:
                    values = line.replace(' ', '').rstrip().split(',')
                    new_record = dict(list(zip(keys, values)))

                    try:
                        temp = int(new_record['MaxTemperatureC'])
                        if temp > max_temperature:
                            max_temperature = temp
                            max_temperature_recored = new_record
                    except ValueError:
                        # print(ValueError)
                        pass
        return max_temperature_recored

    def get_lowest_temparature_recored(self, file_names_list):
        '''
        This method takes list of paths and return the record of a day
        that have lowest temperature.
        '''

        min_temperature_recored = dict()
        min_temperature = None
        temp = 273
        for file_name in file_names_list:
            with open(file_name) as current_file:
                keys = current_file.readline().rstrip()\
                    .replace(' ', '').split(',')

                for line in current_file:
                    values = line.replace(' ', '').rstrip().split(',')
                    new_record = dict(list(zip(keys, values)))

                    try:
                        temp = int(new_record['MinTemperatureC'])
                        if (min_temperature is None)\
                                or (min_temperature > temp):
                            min_temperature = temp
                            min_temperature_recored = new_record
                    except ValueError:
                        # print(ValueError)
                        pass
        return min_temperature_recored

    def get_highest_humidity_recored(self, file_names_list):
        '''
        This method takes list of paths and return the record of a day
        that have highest humidity.
        '''

        max_humidity_recored = dict()
        max_humidity = 0
        temp = 0
        for file_name in file_names_list:
            with open(file_name) as current_file:
                keys = current_file.readline().rstrip()\
                    .replace(' ', '').split(',')

                for line in current_file:
                    values = line.replace(' ', '').rstrip().split(',')
                    new_record = dict(list(zip(keys, values)))

                    try:
                        temp = int(new_record['MaxHumidity'])
                        if temp > max_humidity:
                            max_humidity = temp
                            max_humidity_recored = new_record
                    except ValueError:
                        # print(ValueError)
                        pass
        return max_humidity_recored

    def get_average_highest_temp(self, file_name):
        '''
        This method take a a file path and return the average
        of maximum temprature of the day.
        '''

        temp = 0
        counter = 0
        with open(file_name) as current_file:
            keys = current_file.readline().rstrip().replace(' ', '').split(',')
            for line in current_file:
                values = line.replace(' ', '').rstrip().split(',')
                new_record = dict(list(zip(keys, values)))

                try:
                    temp += int(new_record['MaxTemperatureC'])
                    counter += 1
                except ValueError:
                    # print(ValueError)
                    pass
        return temp/counter

    def get_average_lowest_temp(self, file_name):
        '''
        This method take a a file path and return the average
        of minimum temprature of the day.
        '''

        temp = 0
        counter = 0
        with open(file_name) as current_file:
            keys = current_file.readline().rstrip().replace(' ', '').split(',')
            for line in current_file:
                values = line.replace(' ', '').rstrip().split(',')
                new_record = dict(list(zip(keys, values)))
                try:
                    temp += int(new_record['MinTemperatureC'])
                    counter += 1
                except ValueError:
                    # print(ValueError)
                    pass
        return temp/counter

    def get_average_mean_humidity_temp(self, file_name):
        '''
        This method takea a file path and return the average
        of mean humidity of the day.
        '''

        temp = 0
        counter = 0
        with open(file_name) as current_file:
            keys = current_file.readline().rstrip().replace(' ', '').split(',')
            for line in current_file:
                values = line.replace(' ', '').rstrip().split(',')
                new_record = dict(list(zip(keys, values)))

                try:
                    temp += int(new_record['MeanHumidity'])
                    counter += 1
                except ValueError:
                    # print(ValueError)
                    pass
        return temp/counter

    def get_day(self, date):
        '''
        This method takes date in str type i.e 'yyyy-mm-dd' ad return
        day in int an type
        '''

        datee = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return datee.day

    def get_high_temp_record(self, file_name):
        '''
        This method take a a file path and return the weather
        of the day having highest temperature  of the day.
        '''

        high_temp_list = []
        date_list = []
        with open(file_name) as current_file:
            keys = current_file.readline().rstrip().replace(' ', '').split(',')
            for line in current_file:
                values = line.replace(' ', '').rstrip().split(',')
                new_record = dict(list(zip(keys, values)))

                try:
                    high_temp_list.append(int(new_record['MaxTemperatureC']))
                    date_list.append(self.get_day(new_record['PKT']))
                except ValueError:
                    # print(ValueError)
                    pass

        return dict(list(zip(date_list, high_temp_list)))

    def get_low_temp_record(self, file_name):
        '''
        This method take a a file path and return lowest temprature
        record of the day.
        '''

        low_temp_list = []
        date_list = []
        with open(file_name) as current_file:
            keys = current_file.readline().rstrip().replace(' ', '').split(',')
            for line in current_file:
                values = line.replace(' ', '').rstrip().split(',')
                new_record = dict(list(zip(keys, values)))

                try:
                    low_temp_list.append(int(new_record['MinTemperatureC']))
                    date_list.append(self.get_day(new_record['PKT']))
                except ValueError:
                    # print(ValueError)
                    pass

        return dict(list(zip(date_list, low_temp_list)))

    def get_a_fiter(self, date):
        '''
        This method take a date in formate 'yyyy/mm' and converts it into
        the another formate i.e 'yyyy_mm'
        '''

        filter = ''
        date = datetime.datetime.strptime(date, "%Y/%m")
        filter = str(date.year)+'_'+calendar.month_name[date.month][:3]
        # print(filter)
        return filter

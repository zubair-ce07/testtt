from __future__ import print_function
from file_detector_weather_man import FileDetector

import csv


class DataCalculation(FileDetector):
    """This class is the brains of the program and calculates the the data
    after traversing all the files which are passed from the class
    FileDetector.
    methods : monthly_analysis: contains logic to handle the '-a' flag
              monthly_chart : contains logic to handle '-c' flag
              monthly_bonus : contains logic to handle '-b' flag
              yearly_bonus : contains logic to handle '-e' flag"""

    def __init__(self, file_resolver):
        """This __init__ function stores the path passed on from FileDetector
        and stores the path dictionary in case of multiple paths.
        :param file_resolver: This class is inherited to pass locations
        :returns path : path of file in case of one file needed
                 multiple:paths : dictionary of paths in case of multiple
                 paths
                 several variables declared to be passed on to methods"""
        self.path = file_resolver.location_list[0]
        self.avg_highest_temp = 0
        self.avg_lowest_temp = 0
        self.avg_mean_humid = 0
        self.multiple_paths = file_resolver.location_list
        self.maximum_temp = 0
        self.maximum_temp_date = ''
        self.minimum_temp = 100
        self.minimum_temp_date = ''
        self.maximum_humid = 0
        self.maximum_humid_day = ''
        self.file_closer = ''
        self.max_iterations = 0
        self.blank_records_max = 0
        self.min_iterations = 0
        self.blank_records_min = 0
        self.humid_iterations = 0
        self.blank_records_humid = 0

    def file_reader(self):
        """This method returns the opened file after performing the open
        operation and returns the opened file to other methods.
        :return:reader """
        file_open = open(self.path, 'rb')
        reader = csv.reader(file_open)
        self.file_closer = file_open
        return reader

    def monthly_max_calculation(self):
        """This method is used for the final calculation of monthly data.
        It will be called by monthly_analysis method and will return
        the final answer"""
        total_max_temperature = 0
        opened_file = self.file_reader()
        next(opened_file)
        for row in opened_file:
            self.max_iterations += 1

            if row[1] == '':
                self.blank_records_max += 1
            else:
                total_max_temperature += int(row[1])
        # This line closes the file which is currently opened for traversing
        self.file_closer.close()
        monthly_average = total_max_temperature/(self.max_iterations
                                                 - self.blank_records_max)
        return  monthly_average

    def monthly_min_calculation(self):
        """This method is used for the final calculation of monthly data.
        It will be called by monthly_analysis method and will return
        the final answer"""
        total_min_temperature = 0
        opened_file = self.file_reader()
        next(opened_file)
        for row in opened_file:
            self.min_iterations += 1
            if row[3] == '':
                self.blank_records_min += 1
            else:
                total_min_temperature += int(row[3])
        self.file_closer.close()
        monthly_average = total_min_temperature/(self.min_iterations
                                                 - self.blank_records_min)
        return monthly_average

    def monthly_humid_calculation(self):
        """This method is used for the final calculation of monthly data.
        It will be called by monthly_analysis method and will return
        the final answer"""
        total_mean_humid = 0
        opened_file = self.file_reader()
        next(opened_file)
        for row in opened_file:
            self.humid_iterations += 1
            if row[8] == '':
                self.blank_records_humid += 1
            else:
                total_mean_humid += int(row[8])
        self.file_closer.close()
        monthly_average = total_mean_humid/(self.humid_iterations
                                            - self.blank_records_humid)
        return monthly_average

    def monthly_analysis(self):
        """Contains the logic to calculate data w/r to flag '-a'.
        The calculation is done in 3 modules. First monthly average is taken
        for highest temperatures. Secondly, monthly average for minimum
        temperatures, and thirdly, monthly average for mean humidity.
        This method traverses through all the files passed as params,
        selects the column when traversing a row, stores data into
        temporary variables, and calculates the averages.
        It also has the mechanism to ignore a field if it is zero and
        safeguard the average from being distorted because of an empty field.
        :return: avg_highest_temp : average of maximum temperatures
                 avg_lowest_temp : average of minimum temperatures
                 avg_mean_humid : average of mean humidity"""
        # Calculating average of maximum temperature
        self.avg_highest_temp = self.monthly_max_calculation()

        # Calculating average of minimum temperature
        self.avg_lowest_temp = self.monthly_min_calculation()

        # Calculating average of mean humidity
        self.avg_mean_humid = self.monthly_humid_calculation()

    def monthly_chart(self):
        """This method handles the visualization of the flag '-c'.
        It traverses through the maximum and minimum temperature for each day,
        stores it in a variable, and then draws the '*' according to the number.
        :param: path : path of the file to be traversed.
        :return: visualization of the daily maximum and minimum temperatures"""
        iterations = 0
        zeroes_in_calculation = 0
        opened_file = self.file_reader()
        next(opened_file)
        for row in opened_file:
            iterations += 1

            if row[1] == '':
                zeroes_in_calculation += 1
            else:
                maximum = row[1]
                print (iterations, " ", end='')
                for values in range(int(maximum)):
                    # for printing red chart
                    print ('\033[1;31m*\033[1;m', end='')

                print(" ", maximum)

            if row[3] == '':
                zeroes_in_calculation += 1
            else:
                minimum = row[3]
                print (iterations, " ", end='')
                for values in range(int(minimum)):
                    # for printing blue chart
                    print ('\033[1;34m*\033[1;m', end='')

                print(" ", minimum)

    def monthly_bonus(self):
        """This method handles the visualization of the bonus task with the
        flag '-b'.
        :param: path : path of the file passed from where data is extracted
        :return: visualization of the bonus task"""
        iterations = 0
        zeroes_in_calculation = 0
        opened_file = self.file_reader()
        next(opened_file)
        for row in opened_file:
            iterations += 1

            if row[1] == '':
                zeroes_in_calculation += 1
            else:
                maximum = int(row[1])
                minimum = int(row[3])
                difference = maximum - minimum
                print(iterations, " ", end='')
                for values in range(minimum):
                    # for printing chart with dual color
                    print('\033[1;34m*\033[1;m', end='')
                for values in range (difference):
                    print('\033[1;31m*\033[1;m', end='')
                print(" ", minimum, " - ", maximum)
        self.file_closer.close()

    def yearly_analysis(self):
        """This function handles the calculation for the flag '-e'.
        Since yearly analysis is required to traverse through all the files
        in a year, it is passed multiple_paths instead of path.
        It calculates the maximum and minimum for the year and also stores
        the date and month. Also contains logic to disregard an empty field.
        :param: multiple_paths : dictionary containing all the paths of files
        :return: maximum_temp : maximum temperature in the year
                 maximum_temp_date : date of the maximum temperature
                 minimum_temp : minimum temperature in the year
                 minimum_temp_date : date of minimum temperature
                 maximum_humid : maximum humidity in the year
                 maximum_humid_date : date of maximum humidity"""
        iterations = 0
        number_of_zeroes = 0

        for key, value in self.multiple_paths.items():
            # cannot use file reader here because multiple values are used
            file_open = open(value, 'rb')
            reader = csv.reader(file_open)
            next(reader)
            for row in reader:
                iterations += 1
                if row[1] == '':
                    number_of_zeroes += 1
                else:
                    if int(row[1]) > self.maximum_temp:
                        self.maximum_temp = int(row[1])
                        self.maximum_temp_date = row[0]
                if row[3] == '':
                    number_of_zeroes += 1
                else:
                    if int(row[3]) < self.minimum_temp:
                        self.minimum_temp = int(row[3])
                        self.minimum_temp_date = row[0]

                if row[7] == '':
                    number_of_zeroes += 1
                else:
                    if int(row[7]) > self.maximum_humid:
                        self.maximum_humid = row[7]
                        self.maximum_humid_day = row[0]

            file_open.close()

import csv
from file_locator import FileDetector


class CalculatingData(FileDetector):

    def __init__(self, file_obtainer):
        self.single_path = file_obtainer.location_dict
        self.file_closer = ''
        self.average_high_temp = 0
        self.average_min_temp = 0
        self.average_mean_humidity = 0
        self.yearly_highest_temp = 0
        self.yearly_highest_temp_date = 0
        self.yearly_lowest_temp = 0
        self.yearly_lowest_temp_date = 0
        self.yearly_most_humid_day = 0
        self.yearly_most_humid_value = 0
        self.month_date = file_obtainer.month
        """These are variables which will be made use of by other modules
        when the calculations are done and saved"""

    def reading_file(self):
        """This is a file reading module which will be called by
        preceding calculators"""
        open_file = open(self.single_path[1])
        reading = csv.reader(open_file)
        self.file_closer = open_file
        return reading

    def calculate_monthly_max_avg(self):
        """This is the module for calculating monthly maximum average"""
        total_max_temperature = 0
        iterations = 0
        blank_record = 0
        opened_file = self.reading_file()
        next(opened_file)
        for row in opened_file:
            iterations += 1

            if row[1] == '':
                blank_record += 1
            else:
                total_max_temperature += int(row[1])
            self.month_date = row[0]
        self.file_closer.close()
        monthly_average = total_max_temperature / (iterations -
                                                   blank_record)
        return monthly_average

    def calculate_monthly_low_avg(self):
        """This is the module for calculating monthly minimum average"""
        total_min_temperature = 0
        iterations = 0
        blank_record = 0
        opened_file = self.reading_file()
        next(opened_file)
        for row in opened_file:
            iterations += 1

            if row[3] == '':
                blank_record += 1
            else:
                total_min_temperature += int(row[3])
        self.file_closer.close()
        monthly_average = total_min_temperature / (iterations -
                                                   blank_record)
        return monthly_average

    def calculate_avg_humidity(self):
        """This is the module to calculate the monthly average humidity"""
        total_avg_humidity = 0
        iterations = 0
        blank_record = 0
        opened_file = self.reading_file()
        next(opened_file)
        for row in opened_file:
            iterations += 1

            if row[8] == '':
                blank_record += 1
            else:
                total_avg_humidity += int(row[8])
        self.file_closer.close()
        monthly_average = total_avg_humidity / (iterations -
                                                blank_record)
        return monthly_average

    def monthly_analysis(self):
        """This method invokes and calls all the above monthly methods
        for consistent modularity"""
        self.average_high_temp = self.calculate_monthly_max_avg()
        self.average_min_temp = self.calculate_monthly_low_avg()
        self.average_mean_humidity = self.calculate_avg_humidity()

    def yearly_analysis(self):
        """This module does the yearly analysis for maximum and minimum
        temperatures with dates"""
        iterations = 0
        blank_record = 0
        for key, value in self.single_path.items():
            file_open = open(value, 'r')
            reader = csv.reader(file_open)
            next(reader)
            for row in reader:
                iterations += 1
                if row[1] == '':
                    blank_record += 1
                else:
                    if int(row[1]) > self.yearly_highest_temp:
                        self.yearly_highest_temp = int(row[1])
                        self.yearly_highest_temp_date = row[0]
                if row[3] == '':
                    blank_record += 1
                else:
                    if int(row[3]) < self.yearly_lowest_temp:
                        self.yearly_lowest_temp = int(row[3])
                        self.yearly_lowest_temp_date = row[0]

                if row[7] == '':
                    blank_record += 1
                else:
                    if int(row[7]) > int(self.yearly_most_humid_value):
                        self.yearly_most_humid_value = row[7]
                        self.yearly_most_humid_day = row[0]

            file_open.close()

    def monthly_bonus(self):
        """Monthly bonus task is implemented here instead of normal bars,
        colored bars will be shown"""
        print('Calculating monthly averages for {}'.format
              (self.month_date))
        iterations = 0
        blank_record = 0
        file_reader = self.reading_file()
        next(file_reader)
        for row in file_reader:
            iterations += 1

            if row[1] == '':
                blank_record += 1
            else:
                maximum = int(row[1])
                minimum = int(row[3])
                difference = maximum - minimum
                print(iterations, " ", end='')
                for values in range(minimum):
                    print('\033[1;34m*\033[1;m', end='')
                for values in range(difference):
                    print('\033[1;31m*\033[1;m', end='')
                print(" ", minimum, "C - ", maximum, "C\n")
        self.file_closer.close()

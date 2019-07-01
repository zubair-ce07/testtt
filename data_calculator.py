import csv
import operator
import statistics
from input_handler import FileHandler


class CalculatingData(FileHandler):

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

    def monthly_analysis(self):
        total_max_temp = {}
        total_min_temp = {}
        total_avg_humidity = {}
        iterator = 1
        with open(self.single_path[iterator]) as open_file:
            opened_file = csv.reader(open_file)
            next(opened_file)
            for row in opened_file:
                total_max_temp[iterator] = int(row[1])
                total_min_temp[iterator] = int(row[3])
                total_avg_humidity[iterator] = int(row[8])
                iterator += 1
                self.month_date = row[0]
            self.average_high_temp = statistics.mean(total_max_temp.values())
            self.average_min_temp = statistics.mean(total_min_temp.values())
            self.average_mean_humidity = statistics.\
                mean(total_avg_humidity.values())

    def yearly_analysis(self):
        highest_temp = {}
        lowest_temp = {}
        most_humid = {}
        for key, value in self.single_path.items():
            with open(value) as open_file:
                reader = csv.reader(open_file)
                next(reader)
                for row in reader:
                    highest_temp.update({row[0]: int(row[1])})
                    lowest_temp.update({row[0]: int(row[3])})
                    most_humid.update({row[0]: int(row[7])})

        self.yearly_highest_temp_date = max(
            highest_temp.items(), key=operator.itemgetter(1))[0]
        self.yearly_lowest_temp_date = min(
            lowest_temp.items(), key=operator.itemgetter(1))[0]
        self.yearly_most_humid_day = max(
            most_humid.items(), key=operator.itemgetter(1))[0]
        self.yearly_highest_temp = max(highest_temp.values())
        self.yearly_lowest_temp = min(lowest_temp.values())
        self.yearly_most_humid_value = max(most_humid.values())

    def monthly_bonus(self):
        print(f"Calculating monthly averages for {self.month_date}")
        iterations = 0
        with open(self.single_path[1]) as open_file:
            file_reader = csv.reader(open_file)
            next(file_reader)
            for row in file_reader:
                iterations += 1
                maximum = int(row[1])
                minimum = int(row[3])
                difference = maximum - minimum
                print(iterations, " ", end='')
                for values in range(minimum):
                    print('\033[1;34m*\033[1;m', end='')
                for values in range(difference):
                    print('\033[1;31m*\033[1;m', end='')
                print(" ", minimum, "C - ", maximum, "C\n")

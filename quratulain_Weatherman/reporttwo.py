import math
import calendar


# from main import average

def average(sequence, key=None):
    if key:
        sequence = map(key, sequence)
    return sum(sequence) / len(sequence)


class ReportTwo:
    def __init__(self, files_dict, year, month):

        self.records = []
        self.found = False

        self.year = year
        self.month = month
        self.month_name = calendar.month_name[int(month)]
        self.separate_report_data(files_dict)

    def separate_report_data(self, files_dict):
        file_name = 'Murree_weather_' + self.year + '_' + self.month_name[:3] + '.txt'

        if files_dict.get(file_name):
            self.records = files_dict[file_name]
            self.found = True

    def generate_report(self):
        """
        The function performs the required calculation i.e. max temprature average, min temprature and max humidity
        on previously filtered list of dictionaries.
        """

        max_temp_list = [(record['maxTemprature']) for record in self.records if
                         record['maxTemprature'] != float('-inf')]
        min_temp_list = [(record['minTemprature']) for record in self.records if
                         record['minTemprature'] != float('inf')]
        mean_humid_list = [(record['meanHumidity']) for record in self.records if
                           record['meanHumidity'] != float('inf')]

        self.max_temp_average = math.ceil(average(max_temp_list))
        self.min_temp_average = math.ceil(average(min_temp_list))
        self.mean_humid_average = math.ceil(average(mean_humid_list))

    def print_report(self):
        if self.found:
            print("Report2:")
            print("Highest Average: {}C ".format(self.max_temp_average))
            print("Lowest Average: {}C ".format(self.min_temp_average))
            print("Mean Humidity Average: {}% \n".format(self.mean_humid_average))
        else:
            output = "For report2: Record for the %s/%s doesn't exists \n" % (self.year, self.month)
            print(output)

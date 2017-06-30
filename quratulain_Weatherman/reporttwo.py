import math
import calendar


def average(sequence, key=None):
    if key:
        sequence = map(key, sequence)
    return sum(sequence) / len(sequence)


class ReportTwo:
    def __init__(self, records):
        self.records = records

    def generate_report(self):
        max_temp = [(record['maxTemprature']) for record in self.records if
                    record['maxTemprature'] != float('-inf')]
        min_temp = [(record['minTemprature']) for record in self.records if
                    record['minTemprature'] != float('inf')]
        mean_humid = [(record['meanHumidity']) for record in self.records if
                      record['meanHumidity'] != float('inf')]

        self.max_temp_average = math.ceil(average(max_temp))
        self.min_temp_average = math.ceil(average(min_temp))
        self.mean_humid_average = math.ceil(average(mean_humid))

    def print_report(self):
        print("Report2:")
        print("Highest Average: {}C ".format(self.max_temp_average))
        print("Lowest Average: {}C ".format(self.min_temp_average))
        print("Mean Humidity Average: {}% \n".format(self.mean_humid_average))
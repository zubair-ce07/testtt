from termcolor import colored
import calendar


class TemperatureGraph:
    def __init__(self, records):
        self.records = records

    def print_report(self):
        print("Report3: ")

        for record in self.records:
            day = record['day']
            max_temp = record['maxTemprature']
            min_temp = record['minTemprature']

            if max_temp != float('-inf'):
                max_temp_output = str(day) + '+' * max_temp + str(max_temp) + 'C'
                print(colored(max_temp_output, 'red'))

            if min_temp != float('inf'):
                min_temp_output = str(day) + '+' * min_temp + str(min_temp) + 'C'
                print(colored(min_temp_output, 'blue'))
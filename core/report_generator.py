from termcolor import colored
from helpers.core.report_generator_helper import *
from models.calculated_result import CalculatedResult


class ReportGenerator:

    def __init__(self):
        self.results = CalculatedResult.get_data()

    def print_report(self):
        for entry in self.results:
            print()
            if 'type' in entry and 'data' in entry:
                if entry['type'] == "-e":
                    for each_entry in entry['data']:
                        print(each_entry['text'] + " "
                              + each_entry['value']
                              + each_entry['ending'] + " on "
                              , end='')
                        print(colored(readable_date(each_entry['date']), 'red'))
                elif entry['type'] == "-a":
                    for each_entry in entry['data']:
                        print(each_entry['text'] + " "
                              + each_entry['value']
                              + each_entry['ending']
                              )
                elif entry['type'] == "-c":
                    for each_entry in entry['data']:
                        print(each_entry['text'])
                        arr = each_entry['value']
                        for each_day in arr:
                            print(colored(each_day['pkt'].split('-')[-1] + "\t", 'red'), end='')
                            for i in range(0, int(each_day['max_temperature_c'])):
                                print(colored("+", 'red'), end='')
                            print(colored("  " + str(each_day['max_temperature_c']) + "C", 'red'))

                            print(colored(each_day['pkt'].split('-')[-1] + "\t", 'blue'), end='')
                            for i in range(0, int(each_day['min_temperature_c'])):
                                print(colored("+", 'blue'), end='')
                            print(colored("  " + str(each_day['min_temperature_c']) + "C", 'blue'))
                        print()
                elif entry['type'] == '-d':
                    for each_entry in entry['data']:
                        print(each_entry['text'])
                        arr = each_entry['value']
                        for each_day in arr:
                            print(each_day['pkt'].split('-')[-1] + "\t", end='')
                            # print(colored(each_day['pkt'].split('-')[-1] + "\t", 'red'), end='')
                            for i in range(0, (int(each_day['min_temperature_c'] + each_day['max_temperature_c']))):
                                if i < each_day['min_temperature_c']:
                                    print(colored("+", 'blue'), end='')
                                else:
                                    print(colored("+", 'red'), end='')
                            print(colored("  " + str(each_day['min_temperature_c']) + "C ", 'blue'), end='-')
                            print(colored("  " + str(each_day['max_temperature_c']) + "C", 'red'))
                        print()

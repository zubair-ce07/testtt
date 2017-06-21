from termcolor import colored
import calendar


class ReportThree:
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

    def print_report(self):

        if self.found:
            print("Report3: ")

            for record in self.records:
                max_temp = record['maxTemprature']
                min_temp = record['minTemprature']
                day = record['day']

                if max_temp != float('-inf'):
                    max_temp_output = str(day) + '+' * max_temp + str(max_temp) + 'C'
                    print(colored(max_temp_output, 'red'))

                if min_temp != float('inf'):
                    min_temp_output = str(day) + '+' * min_temp + str(min_temp) + 'C'
                    print(colored(min_temp_output, 'blue'))

        else:
            output = "For report3: Record for the %s/%s doesn't exists \n" % (self.year, self.month)
            print(output)

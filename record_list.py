from record import Record
from termcolor import colored


class RecordList:
    def __init__(self):
        self.record_list = []
        self.record = Record()

    def add_record(self, row):
        self.record = row
        self.record_list.append(row)

    def print_data(self):
        for row in self.record_list:
            print('Date: {}'.format(row.get_date()))
            print('Max Temperature: {}'.format(row.get_max_temp()))
            print('Max Humidity: {}'.format(row.get_max_humidity()))
            print('Min Temperature: {}'.format(row.get_min_temp()))
            print('Min Humidity: {}\n'.format(row.get_min_humidity()))

    def get_query_data(self, date):
        new_record_list = RecordList()
        date = date.replace('/', '-')  # in case the input date is of format yyyy/mm/dd instead of yyyy-mm-dd

        for record in self.record_list:
            if date in record.get_date():
                new_record_list.add_record(record)
                # print(record.get_date())
        return new_record_list

    def calculate_min_max(self):
        max = 0
        max_date = ''
        min_date = ''
        humid_date = ''
        min = 10000
        humid = 0

        result = {}
        for record in self.record_list:
            if record.get_max_temp():
                if record.get_max_temp() > max:
                    max = record.get_max_temp()
                    max_date = record.get_date()

            if record.get_min_temp():
                if record.get_min_temp() < min:
                    min = record.get_min_temp()
                    min_date = record.get_date()

            if record.get_max_humidity():
                if record.get_max_humidity() > humid:
                    humid = record.get_max_humidity()
                    humid_date = record.get_date()

        result['Max Temp'] = max
        result['Max Temp Date'] = max_date
        result['Min Temp'] = min
        result['Min Temp Date'] = min_date
        result['Max Humidity'] = humid
        result['Max Humidity Date'] = humid_date

        return result

    # Function to calculate mean averages and store the results in a list
    def calculate_mean(self):
        mean_result = {}
        max_avg_temp = 0
        min_avg_temp = 10000
        avg_humid = 0
        count = 0
        for record in self.record_list:
            if record.get_mean_humidity() > max_avg_temp:
                max_avg_temp = record.get_mean_humidity()

            if record.get_mean_temp() < min_avg_temp:
                min_avg_temp = record.get_mean_temp()

            if record.get_mean_humidity():
                if avg_humid == 0:
                    avg_humid = record.get_mean_humidity()
                    count += 1
                else:
                    avg_humid = avg_humid + record.get_mean_humidity()
                    count += 1

        avg_humid = avg_humid / count

        mean_result['Max Average Temp'] = max_avg_temp
        mean_result['Max Temp Date'] = min_avg_temp
        mean_result['Max Humidity'] = avg_humid

        return mean_result

    # Function to print horizontal bar charts of a given month
    def generate_bar_chart(self):
        for record in self.record_list:
            max_temp = record.get_max_temp()
            min_temp = record.get_min_temp()

            day = record.get_date().split(sep='-')[2]

            #     Sub-part 4
            #     print(day + ' ', end='')
            #     for i in range(max_temp):
            #         print(colored('+', 'red'), end='')
            #     print(' ' + str(max_temp) + 'C')
            #
            #     print(day + ' ', end='')
            #     for i in range(min_temp):
            #         print(colored('+', 'blue'), end='')
            #     print(' ' + str(min_temp) + 'C')

            # BONUS TASK
            print('{} '.format(day), end='')
            for i in range(min_temp):
                print(colored('+', 'blue'), end='')

            for i in range(max_temp):
                print(colored('+', 'red'), end='')
            print(' {}C -'.format(min_temp), end='')
            print(' {}C'.format(max_temp))
        print()








import sys
import datetime


# The class responsible for reading and organizing the data
class Parser:
    def __init__(self):
        pass

    # Read all files line by line and return them
    @staticmethod
    def read(files):
        collection = []

        for file in files:
            f = open(file, 'r')
            data = f.readlines()

            for line in data:
                collection.append(line)
            pass

        return collection

    # Read all the previously read lines and filter headers and useless rows
    def clean(self, collection):
        indices = []

        attributes = collection[0].split(',')

        attributes = [x.strip() for x in attributes]

        date_index = attributes.index('PKT')

        indices.append(attributes.index('Max TemperatureC'))
        indices.append(attributes.index('Mean TemperatureC'))
        indices.append(attributes.index('Min TemperatureC'))
        indices.append(attributes.index('Max Humidity'))
        indices.append(attributes.index('Mean Humidity'))
        indices.append(attributes.index('Min Humidity'))

        clean_data = [x for x in collection if not x[0].isalpha() and
                      self.includes_relevant_data(x, indices)]

        # Convert the data into a standard form

        standardized_data = []

        for row in clean_data:
            data = row.split(',')
            temp_row = data[date_index]
            temp_row += ','

            for i in range(0, len(indices)):
                temp_row += data[indices[i]]

                if not i == len(indices) - 1:
                    temp_row += ','

            standardized_data.append(temp_row)

        clean_data = standardized_data

        return clean_data

    # Check if the tuple contains at least one of the required attributes
    @staticmethod
    def includes_relevant_data(entry, indices):
        data = entry.split(',')
        relevant_indices = indices

        for r in relevant_indices:
            if data[r] != '':
                return True
            pass

        return False

    # Covert the list of lines into a dictionary
    @staticmethod
    def organize_data(clean_data):
        organized = []

        for entry in clean_data:
            data = entry.split(',')
            organized.append({'Date': data[0],
                              'Max Temp': data[1],
                              'Mean Temp': data[2],
                              'Min Temp': data[3],
                              'Max Humidity': data[4],
                              'Mean Humidity': data[5],
                              'Min Humidity': data[6]
                              })

        return organized


# The class responsible for performing calculations
class Calculator:
    def __init__(self):
        pass

    @staticmethod
    def calculate_annual_result(organized_data, year):
        result = {}

        lowest_temp = sys.maxsize
        highest_temp = -sys.maxsize
        highest_humidity = -sys.maxsize
        lowest_temp_date = '1990-1-1'
        highest_temp_date = '1990-1-1'
        highest_humidity_date = '1990-1-1'

        for data in organized_data:
            if year in data['Date']:
                if data['Min Temp'] != '' and \
                        int(data['Min Temp']) < lowest_temp:
                    lowest_temp = int(data['Min Temp'])
                    lowest_temp_date = data['Date']

                if data['Max Temp'] != '' and \
                        int(data['Max Temp']) > highest_temp:
                    highest_temp = int(data['Max Temp'])
                    highest_temp_date = data['Date']

                if data['Max Humidity'] != '' and \
                        int(data['Max Humidity']) > highest_humidity:
                    highest_humidity = int(data['Max Humidity'])
                    highest_humidity_date = data['Date']
            pass

        result['Lowest Annual Temp'] = [lowest_temp, lowest_temp_date]
        result['Highest Annual Temp'] = [highest_temp, highest_temp_date]
        result['Highest Annual Humidity'] = [highest_humidity,
                                             highest_humidity_date]

        return result

    @staticmethod
    def calculate_monthly_average_report(organized_data, year, month):
        result = {}
        date = year + '-' + month

        high_temps = []
        low_temps = []
        mean_humidity_val = []

        for data in organized_data:
            if date in data['Date']:
                if data['Max Temp'] != '':
                    high_temps.append(int(data['Max Temp']))
                if data['Min Temp'] != '':
                    low_temps.append(int(data['Min Temp']))
                if data['Max Humidity'] != '':
                    mean_humidity_val.append(int(data['Mean Humidity']))

        if len(high_temps) == 0 or len(low_temps) == 0 or \
                len(mean_humidity_val) == 0:
            return {}

        # print(highTemps)
        # print(sum(highTemps))
        # print(len(highTemps))

        result['Average Highest Temp'] = sum(high_temps) / len(high_temps)
        result['Average Lowest Temp'] = sum(low_temps) / len(low_temps)
        result['Average Mean Humidity'] = sum(
            mean_humidity_val) / len(mean_humidity_val)

        return result

    @staticmethod
    def calculate_daily_extremes_report(organized_data, year, month):
        result = {}
        date = year + '-' + month + '-'

        dates = []
        min_temps = []
        max_temps = []

        for data in organized_data:
            if date in data['Date']:
                # print(data['Date'])
                if data['Max Temp'] != '' and data['Min Temp'] != '':
                    dates.append(data['Date'])
                    min_temps.append(data['Min Temp'])
                    max_temps.append(data['Max Temp'])

        result['Dates'] = dates
        result['Min Temps'] = min_temps
        result['Max Temps'] = max_temps
        return result


# The class responsible for presenter the calculations
class Presenter:
    def __init__(self):
        pass

    @staticmethod
    def str_to_date(string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def present_annual_report(self, report):
        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        if humid[0] == -sys.maxsize or low[0] == sys.maxsize or \
                high[0] == -sys.maxsize:
            print('Invalid data or input')
            return

        date = self.str_to_date(high[1])
        print("Highest: {0}C on {1}".format(high[0], date.strftime("%d %B")))

        date = self.str_to_date(low[1])
        print("Lowest: {0}C on {1}".format(low[0], date.strftime("%d %B")))

        date = self.str_to_date(humid[1])
        print("Humidity: {0}% on {1}\n".format(
            humid[0], date.strftime("%d %B")))

        pass

    @staticmethod
    def present_monthly_average_report(report):

        if 'Average Highest Temp' not in report or \
                'Average Lowest Temp' not in report or \
                'Average Mean Humidity' not in report:
            print('Invalid data or input')
            return

        print('Highest Average: {0}C'.format(
            round(report['Average Highest Temp'])))
        print('Lowest Average: {0}C'.format(
            round(report['Average Lowest Temp'])))
        print('Average Mean Humidity: {0}%\n'.format(
            round(report['Average Mean Humidity'])))

        pass

    def present_daily_extremes_report(self, report, horizontal=False):
        dates = report['Dates']
        min_temps = report['Min Temps']
        max_temps = report['Max Temps']

        if len(dates) == 0 or len(dates) != len(min_temps) or \
                len(dates) != len(max_temps):
            print('Invalid data or input')
            return

        date = self.str_to_date(dates[0])
        print(date.strftime('%B %Y'))

        for i in range(0, len(dates)):
            day = dates[i].split(
                '-')[2] if len(dates[i].split('-')[2]) == 2 else '0' + \
                                                                 dates[i].split('-')[2]

            low = '+' * abs(int(min_temps[i]))
            high = '+' * int(max_temps[i])

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(
                    day, high, int(max_temps[i])))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(
                    day, low, int(min_temps[i])))
            else:
                print((u"{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}" +
                       u"\u001b[0m {3}C-{4}C").format(
                    day, low, high, int(min_temps[i]), int(max_temps[i])))

        print()
        pass

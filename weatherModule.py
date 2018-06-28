import sys
import datetime


# The class responsible for reading and organizing the data
class Parser():
    def __init__(self):
        pass

    # Read all files line by line and return them
    def read(self, files):
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

        dateIndex = attributes.index('PKT')

        indices.append(attributes.index('Max TemperatureC'))
        indices.append(attributes.index('Mean TemperatureC'))
        indices.append(attributes.index('Min TemperatureC'))
        indices.append(attributes.index('Max Humidity'))
        indices.append(attributes.index('Mean Humidity'))
        indices.append(attributes.index('Min Humidity'))

        cleanData = [x for x in collection if not x[0].isalpha() and
                     self.includesRelevantData(x, indices)]

        # Convert the data into a standard form

        standardizedData = []

        for row in cleanData:
            data = row.split(',')
            tempRow = data[dateIndex]
            tempRow += ','

            for i in range(0, len(indices)):
                tempRow += data[indices[i]]

                if not i == len(indices) - 1:
                    tempRow += ','

            standardizedData.append(tempRow)

        cleanData = standardizedData

        return cleanData

    # Check if the tuple contains at least one of the required attributes
    def includesRelevantData(self, tuple, indices):
        data = tuple.split(',')
        relevantIndices = indices

        for r in relevantIndices:
            if data[r] != '':
                return True
            pass

        return False

    # Covert the list of lines into a dictionary
    def organizeData(self, cleanData):
        organized = []

        for tuple in cleanData:
            data = tuple.split(',')
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
class Calculator():
    def __init__(self):
        pass

    def calculateAnnualResult(self, organizedData, year):
        result = {}

        lowestTemp = sys.maxsize
        highestTemp = -sys.maxsize
        highestHumidity = -sys.maxsize
        lowestTempDate = '1990-1-1'
        highestTempDate = '1990-1-1'
        highestHumidityDate = '1990-1-1'

        for data in organizedData:
            if year in data['Date']:
                if data['Min Temp'] != '' and \
                   int(data['Min Temp']) < lowestTemp:
                    lowestTemp = int(data['Min Temp'])
                    lowestTempDate = data['Date']

                if data['Max Temp'] != '' and \
                   int(data['Max Temp']) > highestTemp:
                    highestTemp = int(data['Max Temp'])
                    highestTempDate = data['Date']

                if data['Max Humidity'] != '' and \
                   int(data['Max Humidity']) > highestHumidity:
                    highestHumidity = int(data['Max Humidity'])
                    highestHumidityDate = data['Date']
            pass

        result['Lowest Annual Temp'] = [lowestTemp, lowestTempDate]
        result['Highest Annual Temp'] = [highestTemp, highestTempDate]
        result['Highest Annual Humidity'] = [highestHumidity,
                                             highestHumidityDate]

        return result

    def calculateMonthlyAverageReport(self, organizedData, year, month):
        result = {}
        date = year + '-' + month

        highTemps = []
        lowTemps = []
        meanHumidities = []

        for data in organizedData:
            if date in data['Date']:
                if data['Max Temp'] != '':
                    highTemps.append(int(data['Max Temp']))
                if data['Min Temp'] != '':
                    lowTemps.append(int(data['Min Temp']))
                if data['Max Humidity'] != '':
                    meanHumidities.append(int(data['Mean Humidity']))

        if len(highTemps) == 0 or len(lowTemps) == 0 or \
           len(meanHumidities) == 0:
            return {}

        # print(highTemps)
        # print(sum(highTemps))
        # print(len(highTemps))

        result['Average Highest Temp'] = sum(highTemps) / len(highTemps)
        result['Average Lowest Temp'] = sum(lowTemps) / len(lowTemps)
        result['Average Mean Humidity'] = sum(
            meanHumidities) / len(meanHumidities)

        return result

    def calculateDailyExtremesReport(self, organizedData, year, month):
        result = {}
        date = year + '-' + month + '-'

        dates = []
        minTemps = []
        maxTemps = []

        for data in organizedData:
            if date in data['Date']:
                # print(data['Date'])
                if data['Max Temp'] != '' and data['Min Temp'] != '':
                    dates.append(data['Date'])
                    minTemps.append(data['Min Temp'])
                    maxTemps.append(data['Max Temp'])

        result['Dates'] = dates
        result['Min Temps'] = minTemps
        result['Max Temps'] = maxTemps
        return result


# The class responsible for presenter the calculations
class Presenter():
    def __init__(self):
        pass

    def strToDate(self, string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def presentAnnualReport(self, report):
        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        if humid[0] == -sys.maxsize or low[0] == sys.maxsize or \
           high[0] == -sys.maxsize:
            print('Invalid data or input')
            return

        date = self.strToDate(high[1])
        print("Highest: {0}C on {1}".format(high[0], date.strftime("%d %B")))

        date = self.strToDate(low[1])
        print("Lowest: {0}C on {1}".format(low[0], date.strftime("%d %B")))

        date = self.strToDate(humid[1])
        print("Humidity: {0}% on {1}\n".format(
            humid[0], date.strftime("%d %B")))

        pass

    def presentMonthyAverageReport(self, report):

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

    def presentDailyExtremesReport(self, report, horizontal=False):
        dates = report['Dates']
        minTemps = report['Min Temps']
        maxTemps = report['Max Temps']

        if len(dates) == 0 or len(dates) != len(minTemps) or \
           len(dates) != len(maxTemps):
            print('Invalid data or input')
            return

        date = self.strToDate(dates[0])
        print(date.strftime('%B %Y'))

        for i in range(0, len(dates)):
            day = dates[i].split(
                '-')[2] if len(dates[i].split('-')[2]) == 2 else '0' + \
                dates[i].split('-')[2]

            low = '+' * abs(int(minTemps[i]))
            high = '+' * int(maxTemps[i])

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(
                    day, high, int(maxTemps[i])))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(
                    day, low, int(minTemps[i])))
            else:
                print((u"{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}" +
                       u"\u001b[0m {3}C-{4}C").format(
                    day, low, high, int(minTemps[i]), int(maxTemps[i])))

        print()
        pass

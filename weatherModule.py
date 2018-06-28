import sys
import datetime


class Parser():
    def __init__(self):
        pass

    def read(self, files):
        collection = []

        for file in files:
            f = open(file, 'r')
            data = f.readlines()

            # Remove the headers of the files

            for line in data:
                collection.append(line)
            pass

        return collection

    def clean(self, collection):
        cleanData = [x for x in collection if not x[0].isalpha() and
                     self.includesRelevantData(x)]
        return cleanData

    def includesRelevantData(self, tuple):
        data = tuple.split(',')
        relevantIndices = [1, 2, 3, 7, 8, 9]

        for r in relevantIndices:
            if data[r] != '':
                return True
            pass

        return False

    def organizeData(self, cleanData):
        organized = []

        for tuple in cleanData:
            data = tuple.split(',')
            organized.append({'Date': data[0],
                              'Max Temp': data[1],
                              'Mean Temp': data[2],
                              'Min Temp': data[3],
                              'Max Humidity': data[7],
                              'Mean Humidity': data[8],
                              'Min Humidity': data[9]
                              })

        return organized


class Calculator():
    def __init__(self):
        pass

    def calculateAnnualResult(self, organizedData, year):
        result = {}

        lowestTemp = sys.maxsize
        highestTemp = -1
        highestHumidity = -1
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
        date = year + '-' + month

        dates = []
        minTemps = []
        maxTemps = []

        for data in organizedData:
            if date in data['Date']:
                if data['Max Temp'] != '' and data['Min Temp'] != '':
                    dates.append(data['Date'])
                    minTemps.append(data['Min Temp'])
                    maxTemps.append(data['Max Temp'])

        result['Dates'] = dates
        result['Min Temps'] = minTemps
        result['Max Temps'] = maxTemps
        return result


class Presenter():
    def __init__(self):
        pass

    def strToDate(self, string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def presentAnnualReport(self, report):
        high = report['Highest Annual Temp']

        date = self.strToDate(high[1])
        print("Highest: {0}C on {1}".format(high[0], date.strftime("%d %B")))

        low = report['Lowest Annual Temp']

        date = self.strToDate(low[1])
        print("Lowest: {0}C on {1}".format(low[0], date.strftime("%d %B")))

        humid = report['Highest Annual Humidity']

        date = self.strToDate(humid[1])
        print("Humidity: {0}% on {1}\n".format(
            humid[0], date.strftime("%d %B")))

        pass

    def presentMonthyAverageReport(self, report):

        print('Highest Average: {0}C'.format(report['Average Highest Temp']))
        print('Lowest Average: {0}C'.format(report['Average Lowest Temp']))
        print('Average Mean Humidity: {0}%\n'.format(
            report['Average Mean Humidity']))

        pass

    def presentDailyExtremesReport(self, report, horizontal=False):
        dates = report['Dates']
        minTemps = report['Min Temps']
        maxTemps = report['Max Temps']

        date = self.strToDate(dates[0])
        print(date.strftime('%B %Y'))

        for i in range(0, len(dates)):
            day = dates[i].split(
                '-')[2] if len(dates[i].split('-')[2]) == 2 else '0' + \
                dates[i].split('-')[2]

            low = '+' * int(minTemps[i])
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

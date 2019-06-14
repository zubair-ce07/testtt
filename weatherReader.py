""" This is the driver program for the weatherman task.

"""

import csv
import sys
from os import listdir
from os.path import isfile, join, exists
from datetime import datetime

monthTranslationDict = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                        4: 'Apr', 5: 'May', 6: 'Jun',
                        7: 'Jul', 8: 'Aug', 9: 'Sep',
                        10: 'Oct', 11: 'Nov', 12: 'Dec',}


def makeINT(s, t):
    s = s.strip()

    if not s and t == 'min':
        return sys.maxsize
    elif not s and t == 'max':
        return (-sys.maxsize - 1)
    else:
        return int(s)
    # return int(s) if s else sys.maxsize if t == 'min' else (-sys.maxsize - 1) if t == "max"

def dateTranslation(date):
    if date:
        dateObject = datetime.strptime(date, '%Y-%m-%d')
    else:
        return None
    if dateObject:
        return datetime.strftime(dateObject,'%B %d')
    else:
        return None


class results:
    resultList = []
    def addResult(self, resultType, value, date):
        self.resultList.append({'type': resultType, 'value': value, 'date': date})

    def clearResults(self):
        self.resultList.clear()

    def printResult(self):
        for result in self.resultList:
            character = 'C'
            if 'Humidity' in result['type']:
                character = '%'
            print(result['type'], ': ', result['value'], character, ' on ', dateTranslation(result['date']), sep='')


class calculate:
    result = results()

    def calculateHighest(self, weatherData):
        highestTemp = {'value': (-sys.maxsize - 1), 'date': ''}
        lowestTemp =  {'value': (sys.maxsize), 'date': ''}
        highestHumidity =  {'value': (-sys.maxsize - 1), 'date': ''}
        
        for singleDay in weatherData:
            date = singleDay.weatherDataForTheDay.get('PKT')
            maxTempForTheDay = {'date': date, 'value': makeINT(singleDay.weatherDataForTheDay.get('MaxTemp'), 'max')}
            minTempForTheDay = {'date': date, 'value': makeINT(singleDay.weatherDataForTheDay.get('MinTemp'), 'min')}
            maxHumidForTheDay = {'date': date, 'value': makeINT(singleDay.weatherDataForTheDay.get('MaxHumidity'), 'max')}

            if maxTempForTheDay['value'] > highestTemp['value']:
                highestTemp['value'] = maxTempForTheDay['value']
                highestTemp['date'] = date

            if minTempForTheDay['value'] < lowestTemp['value']:
                lowestTemp['value'] = minTempForTheDay['value']
                lowestTemp['date'] = date

            if maxHumidForTheDay['value'] > highestHumidity['value']:
                highestHumidity['value'] = maxHumidForTheDay['value']
                highestHumidity['date'] = date

        self.result.clearResults()
        self.result.addResult('Highest', highestTemp['value'], highestTemp['date'])
        self.result.addResult('Lowest', lowestTemp['value'], lowestTemp['date'])
        self.result.addResult('Humidity', highestHumidity['value'], highestHumidity['date'])

        return self.result

    def calculateAverage(self, weatherData):
        print("")

    def calculateBarCharts(self, weatherData):
        print("")

    def compute(self, weatherData, calculationType):
        if calculationType == '-e':
            return self.calculateHighest(weatherData)
        elif calculationType == '-a':
            return self.calculateAverage(weatherData)
        elif calculationType == '-c':
            self.calculateBarCharts(weatherData)




class singleReading:
    weatherDataForTheDay = {}
    def __init__(self, oneReading):
        self.weatherDataForTheDay = {'PKT': oneReading.get('PKT'), 
                                     'MaxTemp': oneReading.get('Max TemperatureC'), 
                                     'MinTemp': oneReading.get('Min TemperatureC'), 
                                     'MaxHumidity': oneReading.get('Max Humidity'), 
                                     'MeanHumidity': oneReading.get('Mean Humidity')}


class weatherReader:
    data = []
    def __init__(self, directory, request):
        if exists(directory):
            allFiles = [f for f in listdir(directory)]
        else:
            print("Directory does not exists!")
            return None
        yearAndMonth = request.split('/')
        year = request.split('/')[0]
        month = 0
        if len(yearAndMonth) > 1:
            if request.split('/')[1]:
                month = int(request.split('/')[1])
        
        files = [x for x in allFiles if year in x]
        monthFiles = []
        if month:
            monthFiles = [x for x in files if monthTranslationDict.get(month) in x]
            files = monthFiles
        # print(files)

        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
                for row in readCSV:
                    dayReading = singleReading(row)
                    self.data.append(dayReading)

        
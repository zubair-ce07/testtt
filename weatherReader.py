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

def makeINTZero(s):
    s = s.strip()
    return int(s) if s else 0

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
        avgHighestTemp = 0
        avgLowestTemp =  0
        avgMeanHumidity =  0
        
        for singleDay in weatherData:
            avgHighestTemp += makeINT(singleDay.weatherDataForTheDay.get('MaxTemp'), 'max')
            avgLowestTemp += makeINT(singleDay.weatherDataForTheDay.get('MinTemp'), 'min')
            avgMeanHumidity += makeINT(singleDay.weatherDataForTheDay.get('MeanHumidity'), 'max')

        avgHighestTemp /= len(weatherData)
        avgLowestTemp /= len(weatherData)
        avgMeanHumidity /= len(weatherData)

        self.result.clearResults()
        self.result.addResult('Highest Average', int(avgHighestTemp), '')
        self.result.addResult('Lowest Average', int(avgLowestTemp), '')
        self.result.addResult('Average Mean Humidity', int(avgMeanHumidity), '')

        return self.result

    def calculateBarCharts(self, weatherData):

        self.result.clearResults()

        for day in weatherData:
            maxTempForTheDay = day.weatherDataForTheDay.get('MaxTemp')
            minTempForTheDay = day.weatherDataForTheDay.get('MinTemp')
            date = day.weatherDataForTheDay.get('PKT')
            maxString = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%d') + ' '
            maxString += ''.join(["\033[0;31;40m+" for x in range(abs(makeINTZero(maxTempForTheDay)))])
            maxString += ' '+ "\033[0;35;40m" + maxTempForTheDay + 'C'

            minString = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%d') + ' '
            minString += ''.join(["\033[0;34;40m+" for x in range(abs(makeINTZero(minTempForTheDay)))])
            minString += ' '+ "\033[0;35;40m" + minTempForTheDay + 'C'
            print(maxString)
            print(minString)

    def compute(self, weatherData, calculationType, req):
        if calculationType == '-e':
            if len(req.split('/')) != 1:
                print("Wrong format. Exiting!")
                exit() 
            return self.calculateHighest(weatherData)
        elif calculationType == '-a':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()
            return self.calculateAverage(weatherData)
        elif calculationType == '-c':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()
            print(datetime.strftime(datetime.strptime(req, '%Y/%m'),'%B %Y'))
            return self.calculateBarCharts(weatherData)




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

        
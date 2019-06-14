""" This file contains the weatherReader, calculator
    and result classes, which are used to store data,
    calculate results, and store those results respectively

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import csv
import sys
from os import listdir
from os.path import isfile, join, exists
from datetime import datetime

# This dictionary is used to translate numbered months
# to respective names. Method used to optimize performance
monthTranslationDict = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                        4: 'Apr', 5: 'May', 6: 'Jun',
                        7: 'Jul', 8: 'Aug', 9: 'Sep',
                        10: 'Oct', 11: 'Nov', 12: 'Dec',}

# Customized function created to deal with empty strings.
# Returns max size or min size depending on the comparison
# the value is going to be used in.
def makeINT(s, t):
    s = s.strip()

    if not s and t == 'min':
        return sys.maxsize
    elif not s and t == 'max':
        return (-sys.maxsize - 1)
    else:
        return int(s)

# Customized function created to deal with empty strings.
# Returns zero 0 in case of empty string
def makeINTZero(s):
    s = s.strip()
    return int(s) if s else 0

# This methos translates a date from %Y-%m-%d format to %B %d
def dateTranslation(date):
    if date:
        dateObject = datetime.strptime(date, '%Y-%m-%d')
    else:
        return None
    if dateObject:
        return datetime.strftime(dateObject,'%B %d')
    else:
        return None

# Results container class with methods to add result in the
# available memeber list, clear the list in case same object
# is being used multiple times, and print the results
class resultContainer:
    # Member list to store multiple results
    resultList = []

    # Appends a result in the list
    def addResult(self, resultType, value, date):
        self.resultList.append({'type': resultType, 
                                'value': value, 
                                'date': date})

    # Clears the list of all the results
    def clearResults(self):
        self.resultList.clear()

    # Prints the results
    def printResult(self):
        for result in self.resultList:
            character = 'C'
            if 'Humidity' in result['type']:
                character = '%'

            if result['date']:
                print(result['type'], ': ', 
                      result['value'], character, ' on ', 
                      dateTranslation(result['date']), 
                      sep='')
            else:
                print(result['type'], ': ', 
                      result['value'], character, 
                      sep='')
            

# This class generates the calculations using the given data
# and resturns the resultContainer object with the results in it
class calculator:
    # resultContainer object to store results
    result = resultContainer()

    # Report 1: calculates highest temperature and day, lowest 
    # temperature and day, most humid day and humidity. 
    def calculateHighest(self, weatherData):
        highestTemp = {'value': (-sys.maxsize - 1), 'date': ''}
        lowestTemp =  {'value': (sys.maxsize), 'date': ''}
        highestHumidity =  {'value': (-sys.maxsize - 1), 'date': ''}
        
        for singleDay in weatherData:
            date = singleDay.weatherDataForTheDay.get('PKT')


            maxTempForTheDay = {'date': date, 
                                'value': makeINT(singleDay.weatherDataForTheDay.get('MaxTemp'), 'max')}

            minTempForTheDay = {'date': date, 
                                'value': makeINT(singleDay.weatherDataForTheDay.get('MinTemp'), 'min')}

            maxHumidForTheDay = {'date': date, 
                                 'value': makeINT(singleDay.weatherDataForTheDay.get('MaxHumidity'), 'max')}


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

        self.result.addResult('Highest', 
                              highestTemp['value'], 
                              highestTemp['date'])

        self.result.addResult('Lowest', 
                              lowestTemp['value'], 
                              lowestTemp['date'])

        self.result.addResult('Humidity', 
                              highestHumidity['value'], 
                              highestHumidity['date'])

        return self.result


    # Report 2: For a given month display the average highest temperature, 
    # average lowest temperature, average mean humidity.
    def calculateAverage(self, weatherData):
        avgHighestTemp = 0
        avgLowestTemp =  0
        avgMeanHumidity =  0
        skipMinDays = 0
        skipMaxDays = 0
        skipMeanDays = 0
        
        for singleDay in weatherData:
            initialMaxTemp = makeINTZero(singleDay.weatherDataForTheDay.get('MaxTemp'))
            initialMinTemp = makeINTZero(singleDay.weatherDataForTheDay.get('MinTemp'))
            initialMeanhumidity = makeINTZero(singleDay.weatherDataForTheDay.get('MeanHumidity'))

            if not initialMaxTemp:
                skipMaxDays += 1
            else:
                avgHighestTemp += initialMaxTemp

            if not initialMinTemp:
                skipMinDays += 1
            else:
                avgLowestTemp += initialMinTemp

            if not initialMeanhumidity:
                skipMeanDays += 1
            else:
                avgMeanHumidity += initialMeanhumidity

        avgHighestTemp /= len(weatherData) - skipMaxDays
        avgLowestTemp /= len(weatherData) - skipMinDays
        avgMeanHumidity /= len(weatherData) - skipMeanDays

        self.result.clearResults()
        self.result.addResult('Highest Average', int(avgHighestTemp), '')
        self.result.addResult('Lowest Average', int(avgLowestTemp), '')
        self.result.addResult('Average Mean Humidity', int(avgMeanHumidity), '')

        return self.result

    # For a given month draw two horizontal bar charts on the console for the highest 
    # and lowest temperature on each day. Highest in red and lowest in blue.
    def calculateBarCharts(self, weatherData):

        self.result.clearResults()

        for day in weatherData:
            maxTempForTheDay = day.weatherDataForTheDay.get('MaxTemp')
            minTempForTheDay = day.weatherDataForTheDay.get('MinTemp')
            date = day.weatherDataForTheDay.get('PKT')

            maxString = "\033[0;35;40m" + datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%d') + ' '
            maxString += ''.join(["\033[0;31;40m+" for x in range(abs(makeINTZero(maxTempForTheDay)))])
            maxString += ' '+ "\033[0;35;40m" + maxTempForTheDay + 'C'

            minString = datetime.strftime(datetime.strptime(date, '%Y-%m-%d'),'%d') + ' '
            minString += ''.join(["\033[0;34;40m+" for x in range(abs(makeINTZero(minTempForTheDay)))])
            minString += ' '+ "\033[0;35;40m" + minTempForTheDay + 'C'
            
            print(maxString)
            print(minString)
        
        print("\033[0;0;40m")

    # Method called from the main multiple times, given the request and data
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


# Class for storing a single day weather value in a dict
class singleReading:
    weatherDataForTheDay = {}
    def __init__(self, oneReading):
        self.weatherDataForTheDay = {'PKT': oneReading.get('PKT'), 
                                     'MaxTemp': oneReading.get('Max TemperatureC'), 
                                     'MinTemp': oneReading.get('Min TemperatureC'), 
                                     'MaxHumidity': oneReading.get('Max Humidity'), 
                                     'MeanHumidity': oneReading.get('Mean Humidity')}


# Class that stores required data in a member variable of the
# object, as specified by the given option
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
        monthFiles = []
        files = [x for x in allFiles if year in x]

        if len(yearAndMonth) > 1:
            if request.split('/')[1]:
                month = int(request.split('/')[1])

        if month:
            monthFiles = [x for x in files if monthTranslationDict.get(month) in x]
            files = monthFiles

        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
                for row in readCSV:
                    dayReading = singleReading(row)
                    self.data.append(dayReading)

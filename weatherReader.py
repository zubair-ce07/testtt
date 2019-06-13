""" This is the driver program for the weatherman task.

"""

import csv
from os import listdir
from os.path import isfile, join

allMonths = {1: 'Jan', 2: 'Feb', 3: 'Mar',
          4: 'Apr', 5: 'May', 6: 'Jun',
          7: 'Jul', 8: 'Aug', 9: 'Sep',
          10: 'Oct', 11: 'Nov', 12: 'Dec',}


class results:
    resultList = []
    def addResult(self, givenDict):
        self.resultList.append(givenDict)

    def printResult(self):
        for result in self.resultList:
            character = 'C'
            if 'Humidity' in result['type']:
                character = '%'
            print(result['type'], ': ', result['value'], character, ' on ', result['day'], sep='')


# class calculate:
#     result = results()
#     def __init__(self, weatherData, calculationType):
#         # if calculationType == '-e'

#         # elif calculationType == '-a'

#         # elif calculationType == '-c'


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
        allFiles = [f for f in listdir(directory)]
        yearAndMonth = request.split('/')
        year = request.split('/')[0]
        month = 0
        if len(yearAndMonth) > 1:
            if request.split('/')[1]:
                month = int(request.split('/')[1])
        # print(year, month)
        
        files = [x for x in allFiles if year in x]
        monthFiles = []
        if month:
            monthFiles = [x for x in files if allMonths.get(month) in x]
            files = monthFiles
        print(files)

        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
                for row in readCSV:
                    dayReading = singleReading(row)
                    self.data.append(dayReading)

        
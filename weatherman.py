import sys
import os


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
        cleanData = [x for x in collection if not x[0].isalpha()
                     and self.includesRelevantData(x)]
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
        result['Average Mean Humidity'] = sum(meanHumidities) / len(meanHumidities)

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


# Get all contents of the directory passed as the first argument

contents = os.listdir(sys.argv[1])
contents = [os.path.join(sys.argv[1], x) for x in contents]

# Remove nested directories and only pickup non hidden files

files = [x for x in contents if os.path.isfile(x) and not x.startswith('.')]

# Read all files and extract data

parser = Parser()

weatherData = parser.read(files)

cleanData = parser.clean(weatherData)

organizedData = parser.organizeData(cleanData)

# for x in organizedData:
#     print(x)

# for x in organizedData:
#     print(x['Mean Temp'] == '')

# Perform Calculations

result = []
calculator = Calculator()
mode = []

[mode.append(x) for x in sys.argv if x[0] == '-']

if '-e' in mode:
    year = sys.argv[sys.argv.index('-e') + 1]

    if str.isdigit(year):
        result.append(calculator.calculateAnnualResult(organizedData, year))
    pass

if '-a' in mode:
    date = sys.argv[sys.argv.index('-a') + 1]
    date = date.split('/')

    year = date[0]
    month = date[1]

    if str.isdigit(year) and str.isdigit(month):
        month = str(int(month))
        result.append(calculator.calculateMonthlyAverageReport(organizedData, year, month))
    pass

if '-c' in mode:
    date = sys.argv[sys.argv.index('-a') + 1]
    date = date.split('/')

    year = date[0]
    month = date[1]

    if str.isdigit(year) and str.isdigit(month):
        month = str(int(month))
        result.append(calculator.calculateDailyExtremesReport(organizedData, year, month))
    pass

print(result)

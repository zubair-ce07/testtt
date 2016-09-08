from os import listdir
from os.path import isfile, join
import argparse
import csv


"""	This WeatherDataParser class reads a file, and stores the results """
class WeatherDataParser(object):

	""" Class constructor that takes file path as an argument """
	def __init__(self, filePath):
		self.filePath = filePath

	@staticmethod
	def __extractYear(str):
		return str.split ('-') [0]
	
	@staticmethod
	def __toInt(string):
		if string:
			return int (string)

	""" Reads the file row by row and records min/max Temperatures, HUmidities and hottest days """
	def parseFile(self):
		with open(self.filePath) as csvfile:
			readingFirstRow = 1
			csvfile.seek (0)
			next (csvfile)
			reader = csv.DictReader(csvfile)

			for row in reader:

				if readingFirstRow == 1:

					readingFirstRow = 0
					minTemp = self.__toInt(row ['Min TemperatureC'])
					maxTemp = self.__toInt(row ['Max TemperatureC'])
	
					if 'PKT' in row.keys():

						dateKey = 'PKT'
					else:

						dateKey = 'PKST'

					hottestDay = row [dateKey]
					year = self.__extractYear (row[dateKey])

					minHumidity = self.__toInt(row [' Min Humidity'])
					maxHumidity = self.__toInt(row ['Max Humidity'])

			
				val = self.__toInt(row ['Max TemperatureC'])
				if val is not None and (maxTemp is None or val > maxTemp):
					maxTemp = val
					hottestDay = row [dateKey]
					year = self.__extractYear (row[dateKey])

				val = self.__toInt(row ['Max Humidity'])
				if val is not None and (maxHumidity is None or val > maxTemp):
					maxHumidity = val

				val = self.__toInt(row [' Min Humidity'])
				if val is not None and (minHumidity is None or val < minHumidity):
					minHumidity = val

				val = self.__toInt(row ['Min TemperatureC'])
				if val is not None and (minTemp is None or val < minTemp):
					minTemp = val

			self.minTemp = minTemp
			self.maxTemp = maxTemp
			self.minHumidity = minHumidity
			self.maxHumidity = maxHumidity
			self.hottestDay = hottestDay
			self.year = year
# <------------- END OF CLASS ---------------->


""" Returns 1 if the input is a valid integer and returns 0 otherwise"""
def isValidInt (value):
	if value is not None:

		return 1
	else:

		return 0

""" Finds annual min/max Temperatures, min/max Humidities and hottest days """
def generateAnnualReport (parsedDataList):

	annualDictionary = {}

	for parsedData in parsedDataList:
		
		if not parsedData.year in annualDictionary.keys():
			# Set starting values for min/max Temperatures and min/max Humidity
			annualDictionary [parsedData.year] = {}
			annualDictionary [parsedData.year]['minTemp'] = parsedData.minTemp
			annualDictionary [parsedData.year]['maxTemp'] = parsedData.maxTemp 
			annualDictionary [parsedData.year]['minHumidity'] = parsedData.minHumidity
			annualDictionary [parsedData.year]['maxHumidity'] = parsedData.maxHumidity
			annualDictionary [parsedData.year]['hottestDay'] = parsedData.hottestDay
			annualDictionary [parsedData.year]['year'] = parsedData.year
		else:
			# Update the min/max temperatures and Humidities if required

			val = parsedData.maxTemp
			if isValidInt(val) and (
					annualDictionary [parsedData.year]['maxTemp'] is None or 
					val > annualDictionary [parsedData.year]['maxTemp']):
				# Update max temperature, hottest day and the current year

				annualDictionary [parsedData.year]['maxTemp'] = val
				annualDictionary [parsedData.year]['hottestDay'] = parsedData.hottestDay
				annualDictionary [parsedData.year]['year'] = parsedData.year

			val = parsedData.maxHumidity
			if isValidInt(val) and (
					annualDictionary [parsedData.year]['maxHumidity'] is None or 
					val > annualDictionary [parsedData.year]['maxHumidity']):
				# Update the max Humidity

				annualDictionary [parsedData.year]['maxHumidity'] = val

			val = parsedData.minTemp
			if isValidInt(val) and (
					annualDictionary [parsedData.year]['minTemp'] is None or 
					val < annualDictionary [parsedData.year]['minTemp']):
				# Update the minimum Temperature

				annualDictionary [parsedData.year]['minTemp'] = val

			val = parsedData.minHumidity
			if isValidInt(val) and (
					annualDictionary [parsedData.year]['minHumidity'] is None  or 
					val < annualDictionary [parsedData.year]['minHumidity']):
				# Update min humidity

				annualDictionary [parsedData.year]['minHumidity'] = val
	
	return annualDictionary


""" Prints annual report with Year, MAX Temp, MIN Temp, MAX Humidity and Min Humidity """
def printAnnualWeatherReport (parsedDataList): 

	print ('Year\t\tMAX Temp\tMIN Temp\tMAX Humidity\t  Min Humidity')
	print ('-----------------------------------------------------------------------------')
	count = 0
	annualDictionary = generateAnnualReport (parsedDataList)
	for year,yearData in annualDictionary.items ():

		print (yearData['year'], '\t\t', yearData['maxTemp'], '\t\t', yearData['minTemp'], '\t\t',  yearData['maxHumidity'], '\t\t', yearData['minHumidity'])


""" Prints yearly hottest days and the corresponding maximum temperatures """
def printHottestDays(parsedDataList):

	print ('Hotest days of each year')
	print ('Year\tDate\t\tTemp')
	annualDictionary = generateAnnualReport (parsedDataList)
	for year,yearData in annualDictionary.items ():

		print (yearData['year'], '\t', yearData['hottestDay'].replace ('-', '/'), '\t', yearData['maxTemp'])	

""" Format the path of the file """
def formatFilePath(directoryPath, fileName):
	formattedFilePath = ''

	if directoryPath[len (directoryPath) - 1] != '/':

		formattedFilePath = directoryPath+'/'+fileName
	else:

		formattedFilePath = directoryPath+fileName

	return formattedFilePath

""" Main Function """
def main():

	# Read Command Line arguments and proceed if the arguments are valid. 

	parser = argparse.ArgumentParser(description='Example with non-optional arguments')

	parser.add_argument('reportID', help='Use 1 for Annual Max/Min Temperature and 2 for Hottest day of each year',
							action="store", type=int)
	parser.add_argument('data_dir', action="store", 
							help='Path of directory containing weather data files')

	args = parser.parse_args()

	dataFolderPath = args.data_dir

	try:
		allFileNames = [f for f in listdir(dataFolderPath) if isfile(join(dataFolderPath, f))]

	except OSError as err:

		print("OS error: {0}".format(err))
		exit ()
	
	parsedFileDataList= []

	for fileName in allFileNames:

		weatherDataParser = WeatherDataParser(formatFilePath(dataFolderPath,fileName))
		weatherDataParser.parseFile()
		parsedFileDataList.append (weatherDataParser)

	if args.reportID == 1:

		printAnnualWeatherReport (parsedFileDataList)
	else:

		printHottestDays (parsedFileDataList)

if __name__ == "__main__":
	main()
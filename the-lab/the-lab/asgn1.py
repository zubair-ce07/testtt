from os import listdir
from os.path import isfile, join
import argparse
import csv


class WeatherDataParser(object):

	def __init__(self, fileName,dataFolderPath):
		self.fileName = fileName;
		self.dataFolderPath = dataFolderPath;

	@staticmethod
	def __extractYear(str):
		return str.split ('-') [0];
	
	@staticmethod
	def __toInt(str):
		if str is not None and str != '':
			return int (str);

	def parseFile(self):
		with open(self.dataFolderPath+self.fileName) as csvfile:
			firstTime = 1
			csvfile.seek (0)
			next (csvfile)
			reader = csv.DictReader(csvfile)

			for row in reader:

				if firstTime == 1:
					firstTime = 0;

					minTemp = self.__toInt(row ['Min TemperatureC']);
					maxTemp = self.__toInt(row ['Max TemperatureC']);
	
					if 'PKT' in row.keys():
						dateKey = 'PKT'
					else:
						dateKey = 'PKST'

					hottestDay = row [dateKey];
					year = self.__extractYear (row[dateKey]);

					minHumidity = self.__toInt(row [' Min Humidity']);
					maxHumidity = self.__toInt(row ['Max Humidity']);

				val = self.__toInt(row ['Max TemperatureC'])
				if val is not None and (maxTemp is None or val > maxTemp):
					maxTemp = val;
					hottestDay = row [dateKey];
					year = self.__extractYear (row[dateKey]);

				val = self.__toInt(row ['Max Humidity'])
				if val is not None and (maxHumidity is None or val > maxTemp):
					maxHumidity = val;

				val = self.__toInt(row [' Min Humidity'])
				if val is not None and (minHumidity is None or val < minHumidity):
					minHumidity = val;

				val = self.__toInt(row ['Min TemperatureC']);
				if val is not None and (minTemp is None or val < minTemp):
					minTemp = val;

			self.minTemp = minTemp;
			self.maxTemp = maxTemp;
			self.minHumidity = minHumidity;
			self.maxHumidity = maxHumidity;
			self.hottestDay = hottestDay
			self.year = year

def generateAnnualReport (parsedDataList):
	firstTime = 1

	annualDictionary = {}

	for parsedData in parsedDataList:
		
		if not parsedData.year in annualDictionary.keys():
			annualDictionary [parsedData.year] = {}
			annualDictionary [parsedData.year]['minTemp'] = parsedData.minTemp
			annualDictionary [parsedData.year]['maxTemp'] = parsedData.maxTemp 
			annualDictionary [parsedData.year]['minHumidity'] = parsedData.minHumidity
			annualDictionary [parsedData.year]['maxHumidity'] = parsedData.maxHumidity
			annualDictionary [parsedData.year]['hottestDay'] = parsedData.hottestDay
			annualDictionary [parsedData.year]['year'] = parsedData.year;
		else:

			val = parsedData.maxTemp
			if val is not None and (annualDictionary [parsedData.year]['maxTemp'] is None or val > annualDictionary [parsedData.year]['maxTemp']):
				annualDictionary [parsedData.year]['maxTemp'] = val;
				annualDictionary [parsedData.year]['hottestDay'] = parsedData.hottestDay;
				annualDictionary [parsedData.year]['year'] = parsedData.year;

			val = parsedData.maxHumidity
			if val is not None and (annualDictionary [parsedData.year]['maxHumidity'] is None or val > annualDictionary [parsedData.year]['maxHumidity']):
				annualDictionary [parsedData.year]['maxHumidity'] = val;

			val = parsedData.minTemp;
			if val is not None and (annualDictionary [parsedData.year]['minTemp'] is None or val < annualDictionary [parsedData.year]['minTemp']):
				annualDictionary [parsedData.year]['minTemp'] = val;

			val = parsedData.minHumidity
			if val is not None and (annualDictionary [parsedData.year]['minHumidity'] is None or val < annualDictionary [parsedData.year]['minHumidity']):
				annualDictionary [parsedData.year]['minHumidity'] = val;
	
	return annualDictionary;

def printAnnualWeatherReport (parsedDataList): 

	print ('Year\t\tMAX Temp\tMIN Temp\tMAX Humidity\t  Min Humidity')
	print ('-----------------------------------------------------------------------------')
	count = 0
	annualDictionary = generateAnnualReport (parsedDataList);
	for year,yearData in annualDictionary.items ():
		print (yearData['year'], '\t\t', yearData['maxTemp'], '\t\t', yearData['minTemp'], '\t\t',  yearData['maxHumidity'], '\t\t', yearData['minHumidity']);

def printHottestDays(parsedDataList):

	print ('Hotest days of each year');
	print ('Year\tDate\t\tTemp');
	annualDictionary = generateAnnualReport (parsedDataList);
	for year,yearData in annualDictionary.items ():
		print (yearData['year'], '\t', yearData['hottestDay'].replace ('-', '/'), '\t', yearData['maxTemp']);	

def main():

	parser = argparse.ArgumentParser(description='Example with non-optional arguments')

	parser.add_argument('reportID', help='Use 1 for Annual Max/Min Temperature and 2 for Hottest day of each year',action="store", type=int)
	parser.add_argument('data_dir', action="store", help='Path of directory containing weather data files')

	args = parser.parse_args()

	dataFolderPath = args.data_dir;

	try:
		allFileNames = [f for f in listdir(dataFolderPath) if isfile(join(dataFolderPath, f))]
	except OSError as err:
		print("OS error: {0}".format(err))
		exit ();
	
	parsedFileDataList= [];

	for fileName in allFileNames:
		weatherDataParser = WeatherDataParser(fileName, dataFolderPath);
		weatherDataParser.parseFile();
		parsedFileDataList.append (weatherDataParser);

	if args.reportID == 1:
		printAnnualWeatherReport (parsedFileDataList);
	else:
		printHottestDays (parsedFileDataList);

if __name__ == "__main__":
	main()
from os import listdir
from os.path import isfile, join
from sys import argv

class WeatherDataParser(object):

	def __init__(self, fileName,dataFolderPath):
		# print 'init file: ', fileName;
		self.fileName = fileName;
		self.year = ''
		self.dataFolderPath = dataFolderPath;
	
	@staticmethod
	def __extractMaxTemp(record):
		if record [1] != '':
			return int(record [1]);

	@staticmethod
	def __extractMinTemp(record):
		if record [3] != '':
			return int(record [3]);

	@staticmethod
	def __extractMaxHumidity(record):
		if record [7] != '':
			return int(record [7]);

	@staticmethod
	def __extractMinHumidity(record):
		if record [9] != '':
			return int(record [9]);

	@staticmethod
	def __extractDate(record):
		return record [0].replace ('-', '/');

	@staticmethod
	def __extractYear(record):
		return record [0].split ('-') [0];
	
	def parseFile(self):
		file = open (dataFolderPath+self.fileName, 'r');

		# Skip first two lines
		file.readline();
		file.readline();

	
		firstTime = 1

		for line in file:
			splittedLine = line.split (',');
			
			if len (splittedLine) <= 1:
				break;

			if firstTime == 1:
				firstTime = 0;
				minTemp = self.__extractMinTemp (splittedLine);
				minHumidity = self.__extractMinHumidity (splittedLine);
				maxTemp = self.__extractMaxTemp (splittedLine);
				hottestDay = self.__extractDate (splittedLine);
				maxHumidity = self.__extractMaxHumidity (splittedLine);
				year = self.__extractYear (splittedLine);

			if self.__extractMaxTemp(splittedLine) > maxTemp or maxTemp is None:
				maxTemp = self.__extractMaxTemp(splittedLine);
				hottestDay = self.__extractDate (splittedLine);

			if self.__extractMaxHumidity(splittedLine) > maxTemp or maxHumidity is None:
				maxHumidity = self.__extractMaxHumidity(splittedLine);

			if self.__extractMinHumidity(splittedLine)< minHumidity or minHumidity is None:
				minHumidity = self.__extractMinHumidity (splittedLine);

			if self.__extractMinTemp (splittedLine) < minHumidity or minTemp is None:
				minTemp = self.__extractMinTemp (splittedLine);

		self.minTemp = minTemp;
		self.maxTemp = maxTemp;
		self.minHumidity = minHumidity;
		self.maxHumidity = maxHumidity;
		self.hottestDay = hottestDay
		self.year = year

if len (argv) != 3:
	print 'usage: ', argv [0], ' [report#] [data_dir]';
	exit ();

dataFolderPath = argv [2];

try:
	allFileNames = [f for f in listdir(dataFolderPath) if isfile(join(dataFolderPath, f))]
except OSError:
	print 'Invalid directory name'
	exit ();
	
if int (argv [1]) == 1:
	print 'Year\t\tMAX Temp\tMIN Temp\tMAX Humidity\t MIN Humidity'
	print '-----------------------------------------------------------------------------'
else:
	print 'Hotest days of each year';
	print 'Year\tDate\t\tTemp';

for fileName in allFileNames:
	parser = WeatherDataParser(fileName, dataFolderPath);
	parser.parseFile();
	if int (argv [1]) == 1:
	
		print parser.year, '\t\t', parser.maxTemp, '\t\t', parser.minTemp, '\t\t',  parser.maxHumidity, '\t\t', parser.minHumidity;
	else:
		print parser.year, '\t', parser.hottestDay, '\t', parser.maxTemp	
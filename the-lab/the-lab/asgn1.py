from os import listdir
from os.path import isfile, join
from sys import argv

class WeatherDataParser(object):

	def __init__(self, fileName,dataFolderPath):
		# print 'init file: ', fileName;
		self.fileName = fileName;
		self.year = ''
		self.dataFolderPath = dataFolderPath;
	
	def getYear (self): 
		return self.year;

	def getDate (self):
		return self.date;

	def getMinTemp(self):
		return self.minTemp;

	def getMaxTemp(self):
		return self.maxTemp;

	def getMinHumidity(self):
		return self.minHumidity;

	def getMaxHumidity(self):
		return self.maxHumidity;

	@staticmethod
	def extractMaxTemp(record):
		if record [1] != '':
			return int(record [1]);

	@staticmethod
	def extractMinTemp(record):
		if record [3] != '':
			return int(record [3]);

	@staticmethod
	def extractMaxHumidity(record):
		if record [7] != '':
			return int(record [7]);

	@staticmethod
	def extractMinHumidity(record):
		if record [9] != '':
			return int(record [9]);

	@staticmethod
	def extractDate(record):
		return record [0].replace ('-', '/');

	@staticmethod
	def extractYear(record):
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
				minTemp = self.extractMinTemp (splittedLine);
				minHumidity = self.extractMinHumidity (splittedLine);
				maxTemp = self.extractMaxTemp (splittedLine);
				hottestDay = self.extractDate (splittedLine);
				maxHumidity = self.extractMaxHumidity (splittedLine);
				year = self.extractYear (splittedLine);

			if self.extractMaxTemp(splittedLine) > maxTemp or maxTemp is None:
				maxTemp = self.extractMaxTemp(splittedLine);
				hottestDay = self.extractDate (splittedLine);

			if self.extractMaxHumidity(splittedLine) > maxTemp or maxHumidity is None:
				maxHumidity = self.extractMaxHumidity(splittedLine);

			if self.extractMinHumidity(splittedLine)< minHumidity or minHumidity is None:
				minHumidity = self.extractMinHumidity (splittedLine);

			if self.extractMinTemp (splittedLine) < minHumidity or minTemp is None:
				minTemp = self.extractMinTemp (splittedLine);

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
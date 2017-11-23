
import sys
import glob, os
from datetime import datetime
import re
import calendar
from termcolor import colored
class weatherMan(object):

  def print_Yearly_results(self,filePath,year):

    fileNames=[]
    os.chdir(filePath)
    for file in glob.glob("*.txt"):
      if file.find(year) != -1:
          fileNames.append(file)


    if len(fileNames)==0:
      print 'No Data Found!'
    else:
      for filename in fileNames:

        f = open(filename,'r')
        next(f)
        hightemp = {}
        lowTemp = {}
        highHumidity = {}

        for line in f:
            splittedWords = line.split(',')
            hightemp[splittedWords[0]]=splittedWords[1]
            lowTemp[splittedWords[0]]=splittedWords[3]
            highHumidity[splittedWords[0]]=splittedWords[7]

      highTempRes = sorted(hightemp.items(), key=lambda x: x[1],reverse=True)
      lowTempRes = sorted(lowTemp.items(), key=lambda x: x[1], reverse=True)
      highHumidityRes = sorted(highHumidity.items(), key=lambda x: x[1], reverse=True)
      del highTempRes[1:]
      del lowTempRes[1:]
      del highHumidityRes[1:]
      highDate = datetime.strptime(highTempRes[0][0] , '%Y-%m-%d')
      lowDate = datetime.strptime(lowTempRes[0][0] , '%Y-%m-%d')
      humDate = datetime.strptime(highHumidityRes[0][0] , '%Y-%m-%d')

      print  'Highest: '+ highTempRes[0][1]+'C on '+ highDate.strftime("%B") + ' '+str(highDate.strftime("%d"))
      print  'Lowest: '+ lowTempRes[0][1]+'C on '+ lowDate.strftime("%B") +' ' +str(lowDate.strftime("%d"))
      print  'Humidity: '+ highHumidityRes[0][1]+'% on '+ humDate.strftime("%B") + ' '+str(humDate.strftime("%d"))

    return

  def verifyDirectory(self,directoryPath):
    if os.path.isdir(directoryPath):
      return True
    else:
      return False
    return

  def verifyYear(self,year):
    if year.isdigit() and len(year)==4:
      return True
    else:
      return False

    return

  def verifyYearMonth(self, yearMonth):
    match = re.search(r'^\d\d\d\d/\d+$', yearMonth)
    if match:
      splittedWords = yearMonth.split('/')
      month = int(splittedWords[1])
      if  month >=1 and month <=12:
        return True
      else:
        return False
    else:
      return False

    return

  def print_Month_average(self,filePath,year,month):

    fileNames=[]
    os.chdir(filePath)
    for file in glob.glob("*.txt"):
      if file.find(year) != -1 and file.find(month) != -1:
          fileNames.append(file)


    if len(fileNames)==0:
      print 'No Data Found!'
    else:
      for filename in fileNames:

        f = open(filename,'r')
        next(f)
        hightemp = {}
        lowTemp = {}
        highHumidity = {}

        for line in f:
            splittedWords = line.split(',')
            hightemp[splittedWords[0]]=splittedWords[1]
            lowTemp[splittedWords[0]]=splittedWords[3]
            highHumidity[splittedWords[0]]=splittedWords[9]

            hightempAvg=self.findAverage(hightemp.values())
            lowempAvg=self.findAverage(lowTemp.values())
            highHumAvg=self.findAverage(highHumidity.values())

      print  'Highest Average: '+ str(round(hightempAvg,2))+'C'
      print  'Lowest average: '+ str(round(lowempAvg,2))+'C'
      print  'average Mean Humidity: '+ str(round(highHumAvg,2))+'%'

    return
  def findAverage(self,values):
    sumVal =0.0
    for val in values:
      if len(val)!=0:
        sumVal += float(val)
    return sumVal/len(values)


  def print_day_bars(self,filePath,year,month):

    fileNames=[]
    os.chdir(filePath)
    for file in glob.glob("*.txt"):
      if file.find(year) != -1 and file.find(month) != -1:
          fileNames.append(file)


    if len(fileNames)==0:
      print 'No Data Found!'
    else:
      for filename in fileNames:

        f = open(filename,'r')
        next(f)

        for line in f:
            splittedWords = line.split(',')
            day = datetime.strptime(splittedWords[0] , '%Y-%m-%d')

            high = self.get_Integer(splittedWords[1])
            low = self.get_Integer(splittedWords[3])

            """print day.strftime("%d"),
            self.print_plus(high,'red')
            print str(high) + 'C'
            print day.strftime("%d"),
            self.print_plus(low,'blue')
            print str(low) + 'C'
            """
            print day.strftime("%d"),
            self.print_plus(low, 'blue')
            self.print_plus(high-low, 'red')
            print str(low) + 'C - ' + str(high) + 'C'
    return
  def get_Integer(self,val):
    if len(val) == 0:
      result = 0
    else:
      result = int(val)

    return result

  def print_plus(self,val,color):
    i = 0
    while i < val:
      print colored('+',color),
      i += 1
    return

def subMain(directoryPath,year,reportType):
  weather = weatherMan()
  if reportType == '-e':
    if weather.verifyDirectory(directoryPath) and weather.verifyYear(year):
      weather.print_Yearly_results(directoryPath, year)
    else:
      print 'Incorrect Arguments!'

  elif reportType == '-a':

    if weather.verifyDirectory(directoryPath) and weather.verifyYearMonth(year):
      splittedWords = year.split('/')
      year = splittedWords[0]
      temp = calendar.month_name[int(splittedWords[1])]
      month = temp[0:3]
      weather.print_Month_average(directoryPath, year, month)
    else:
      print "Incorrect Arguments!"

  elif reportType == '-c':

    if weather.verifyDirectory(directoryPath) and weather.verifyYearMonth(year):
      splittedWords = year.split('/')
      year = splittedWords[0]
      temp = calendar.month_name[int(splittedWords[1])]
      month = temp[0:3]
      weather.print_day_bars(directoryPath, year, month)
    else:
      print "Incorrect Arguments!"
  return


def main():

  if len(sys.argv) == 4:
    directoryPath = sys.argv[1]
    year = sys.argv[3]
    reportType = sys.argv[2]
    subMain(directoryPath, year, reportType)
  elif len(sys.argv) ==8:
    directoryPath = sys.argv[1]
    year1 = sys.argv[3]
    year2 = sys.argv[5]
    year3 = sys.argv[7]
    reportType1 = sys.argv[2]
    reportType2 = sys.argv[4]
    reportType3 = sys.argv[6]
    subMain(directoryPath, year1, reportType1)
    print '##############################################################################'
    subMain(directoryPath, year2, reportType2)
    print '##############################################################################'
    subMain(directoryPath, year3, reportType3)

  else:
   print'Incorrect arguments!'


  sys.exit(1)

if __name__ == '__main__':
  main()

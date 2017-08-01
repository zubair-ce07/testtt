import sys
import fnmatch
import argparse
import os
import calendar
import re
import csv

def generateFileNames(arg, operation):
    fileNames = []
    for file in os.listdir(args.f):
        fileNames.append(file)

    if operation == '-a' or operation == '-c':
        yymm = arg.split("/")
        year = yymm[0]
        month = calendar.month_abbr[int(yymm[1])]
        pattern = r'[A-Za-z]*_weather_' + year + '_' + month + '.txt'    
        name = []
        for file in fileNames:
            if fnmatch.fnmatch(file, pattern):
                name.append(file)
        namestring = str(name[0])
        return namestring

    if operation == '-e':
        year = arg
        pattern = r'[A-Za-z]*_weather_' + year + '_' + r'???' + '.txt'    
        name = []
        for file in fileNames:
            if fnmatch.fnmatch(file, pattern):
                name.append(file)
        return name
 
def calcMax(result, attribute):    
    maxVal = None 
    maxList = filter(None, result.get(attribute))
    maxList = [int(i) for i in maxList]
    maxVal = max(maxList)
    return maxVal
    
def calcMin(result, attribute):    
    minVal = None 
    minList = filter(None, result.get(attribute))
    minList = [int(i) for i in minList]
    minVal = min(minList)
    return minVal
    
def calcAvg(result, attribute):    
    avg = None
    l1 = list(filter(None, result.get(attribute)))
    l1 = [int(i) for i in l1]
    avg = sum(l1)/len(l1)
    return int(avg)

def calcDates(fileNames, yearMaxTemp, yearMinTemp, yearMaxHumid, args):    
    yearMaxTempDate, yearMinTempDate, yearMaxHumidDate  = "", "", ""
    for file in fileNames:
        iteration = 1
        result = readFile(args, file)

        for maxT, minT, maxH, date in zip(result.get("Max TemperatureC"), result.get("Min TemperatureC"), result.get("Max Humidity"), result.get("PKT")):
            if not maxT:
                continue
                
            if yearMaxTemp == int(maxT):
                hdate = date.split("-")
                yearMaxTempDate = str(calendar.month_name[int(hdate[1])])
                yearMaxTempDate = yearMaxTempDate + " " + hdate[2] 

            if yearMinTemp == int(minT):
                ldate = date.split("-")
                yearMinTempDate = str(calendar.month_name[int(ldate[1])])
                yearMinTempDate = yearMinTempDate + " " + ldate[2] 
                
            if not maxH:
                continue
                
            if yearMaxHumid == int(maxH):
                hudate = date.split("-")
                yearMaxHumidDate = str(calendar.month_name[int(hudate[1])])
                yearMaxHumidDate = yearMaxHumidDate + " " + hudate[2]
    return yearMaxTempDate,yearMinTempDate, yearMaxHumidDate 

def barChart(result):    
    index = 1
    maxList = list(filter(None, result.get("Max TemperatureC")))
    maxList = [int(i) for i in maxList]
    minList = list(filter(None, result.get("Min TemperatureC")))
    minList = [int(i) for i in minList]
    for maxTemp, minTemp in zip(maxList, minList):
        print('\033[35m', index, '\033[31m' , "+" * maxTemp, '\033[35m', maxTemp,"C")
        print('\033[35m', index, '\033[36m' ,"+" * minTemp, '\033[35m', minTemp,"C", '\033[0m')
        index += 1
        
def barChartBonus(result):
    index = 1
    maxList = list(filter(None, result.get("Max TemperatureC")))
    maxList = [int(i) for i in maxList]
    minList = list(filter(None, result.get("Min TemperatureC")))
    minList = [int(i) for i in minList]
    for maxTemp, minTemp in zip(maxList, minList):
        print('\033[35m', index, '\033[36m' ,"+" * minTemp +  '\033[31m', "+" * maxTemp, '\033[35m', minTemp,"C  -", '\033[35m', maxTemp,"C", '\033[0m')        
        index += 1

def calcValues(fileNames, args):
    monthMaxTemp, monthMinTemp, monthMaxHumid = [],[],[]
    yearMaxTemp, yearMinTemp, yearMaxHumid = 0, 0, 0
    
    for file in fileNames:
        result = readFile(args, file)
        monthMaxTemp.append(calcMax(result, "Max TemperatureC"))
        monthMinTemp.append(calcMin(result, "Min TemperatureC"))
        monthMaxHumid.append(calcMax(result, "Max Humidity"))
    yearMaxTemp = max(monthMaxTemp)
    yearMinTemp = min(monthMinTemp)
    yearMaxHumid = max(monthMaxHumid)
    return yearMaxTemp, yearMinTemp, yearMaxHumid        
 
def readFile(args, fileName):
    with open(args.f + fileName) as read:
        oneFile = csv.DictReader(read)
        result = {}
        for row in oneFile:
            for column, value in row.items():
                result.setdefault(column, []).append(value)
    return result
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='File directory')
    parser.add_argument('-c', type=str, help='-c')
    parser.add_argument('-a', type=str, help='-a')
    parser.add_argument('-e', type=str, help='-e')
    args = parser.parse_args()
    
    if args.e:
        fileNames = generateFileNames(args.e, '-e')
        yearMaxTemp, yearMinTemp, yearMaxHumid = calcValues(fileNames, args)
        yearMaxTempDate, yearMinTempDate, yearMaxHumidDate = calcDates(fileNames, yearMaxTemp, yearMinTemp, yearMaxHumid, args)
        print("Highest: %dC on %s" % (yearMaxTemp, yearMaxTempDate))
        print("Lowest: %dC on %s" % (yearMinTemp, yearMinTempDate))
        print("Humidity:", yearMaxHumid, "% on", yearMaxHumidDate)
        
    if args.a:
        fileName = generateFileNames(args.a, '-a')
        result = readFile(args, fileName)           
        print("Highest Average:" , calcMax(result, "Mean TemperatureC"), "C")
        print("Lowest Average:" , calcMin(result, "Mean TemperatureC"), "C")
        print("Average mean humidity:", calcAvg(result, " Mean Humidity"), "%")

        
    if args.c:
        fileName = generateFileNames(args.c, '-c')
        result = readFile(args, fileName)
        barChart(result)
        barChartBonus(result)
    

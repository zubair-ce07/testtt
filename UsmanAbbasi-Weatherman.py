import sys
import fnmatch
import os
import calendar




def calcFileName(argList):
    fileNames = []
    pattern = 'Murree_weather_' + argList[argList.index("-e")+1] + '_' + '???' + '.txt'
    for file in os.listdir(argList[1]):
        if fnmatch.fnmatch(file, pattern):
            fileNames.append(file)
    return fileNames


def calcFileName2(argList):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if "-c" in argList:
        index = int(argList.index("-c")) + 1
        
    if "-a" in argList:
        index = int(argList.index("-a")) + 1
    
    yymm = argList[index].split("/")
    pattern = 'Murree_weather_' + yymm[0] + '_' + months[int(yymm[1])-1] + '.txt'
    return pattern


def calcMax(lines, attribute):    
    i = 1
    maxVal= -100
    while i != (len(lines)):
        line = lines[i].split(",")      
        i += 1
        
        if not line[attribute]:
            continue
            
        maxVal = max(maxVal, int(line[attribute]))        
    return maxVal


def calcMin(lines, attribute):    
    i = 1
    minVal = 100
    while i != (len(lines)):
        line = lines[i].split(",")      
        i += 1
        if not line[attribute]:
            continue
        minVal = min(minVal, int(line[attribute]))   
    return minVal
    

def calcAvg(lines, attribute):    
    i = 1
    l1 = []
    while i != (len(lines)):
        line = lines[i].split(",")      
        i += 1
        if not line[attribute]:
            continue
        l1.append(int(line[attribute]))    
    avg = sum(l1)/len(l1)
    return int(avg)
    
    
def calcDates(fileNames, highest, lowest, humid):    
    
    lines = []
    for file in fileNames:
        i = 1
        lines = open('weatherfiles/'+file, "r").readlines()
        
        while i != (len(lines)):
            line = lines[i].split(",")      
            i+=1
            if line[3] and lowest == int(line[3]):
                ldate = line[0].split("-")
                lldate = str(calendar.month_name[int(ldate[1])])
                lldate = lldate + " " + ldate[2]
        
            if line[7] and humid == int(line[7]):
                hudate = line[0].split("-")
                hhudate = str(calendar.month_name[int(hudate[1])])
                hhudate = hhudate + " " + hudate[2]


                
            if line[1] and highest == int(line[1]):
                hdate = line[0].split("-")
                hhdate = str(calendar.month_name[int(hdate[1])])
                hhdate = hhdate + " " + hdate[2]
    
    
    
    return hhdate,lldate, hhudate   
    

def barChart(lines):    
    i, index = 1, 1
    while i != (len(lines)):
        line = lines[i].split(",")
        i += 1    
        if not line[1] and not line[3]:
            continue
        
        print('\033[35m', index, '\033[31m' , "+" * int(line[1]), '\033[35m', line[1],"C")
        print('\033[35m', index, '\033[36m' ,"+" * int(line[3]), '\033[35m', line[3],"C", '\033[0m')
        index += 1
        
def barChartBonus(lines):
    i, index = 1, 1
    while i != (len(lines)):
        line = lines[i].split(",")
        i += 1    
        if not line[1] and not line[3]:
            continue    
        print('\033[35m', index, '\033[36m' ,"+" * int(line[3]) +  '\033[31m', "+" * int(line[1]), '\033[35m', line[3],"C  -", '\033[35m', line[1],"C", '\033[0m')        
        index += 1


if __name__ == "__main__":

    if '-e' in sys.argv:
        fileNames = calcFileName(sys.argv)
        monthMaxTemp, monthMinTemp, monthMaxHumid = [],[],[]
        highest, lowest, humid = 0, 0, 0
        for file in fileNames:
            lines = open(sys.argv[1] + file, "r").readlines()
            monthMaxTemp.append(calcMax(lines, 1))
            monthMinTemp.append(calcMin(lines, 3))
            monthMaxHumid.append(calcMax(lines, 7))
        highest = max(monthMaxTemp)
        lowest = min(monthMinTemp)
        humid = max(monthMaxHumid)
        hdate, ldate, hudate = calcDates(fileNames, highest, lowest, humid)
        print("Highest: %dC on %s" % (highest, hdate))
        print("Lowest: %dC on %s" % (lowest, ldate))
        print("Humidity:", humid, "% on", hudate)
        print("\n")
        
    if '-a' in sys.argv:
        fileName = calcFileName2(sys.argv)
        lines = open(sys.argv[1] + fileName, "r").readlines()
        print("Highest Average:" , calcMax(lines, 2), "C")
        print("Lowest Average:" , calcMin(lines, 2), "C")
        print("Average mean humidity:", calcAvg(lines, 8), "%")
        print("\n")
        
    if '-c' in sys.argv:
        fileName = calcFileName2(sys.argv)
        lines = open(sys.argv[1] + fileName, "r").readlines()
        monthMaxTemp, monthMinTemp = 0,0
        highest, lowest = 0, 0
        monthMaxTemp = calcMax(lines, 1)
        monthMinTemp = calcMin(lines, 3)
        barChart(lines)
        print("\n")
        barChartBonus(lines)
        print("\n")
        
    else:
        print("Invalid arguments.")
        sys.exit()
        
    

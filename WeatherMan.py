import FileReader, CalculationsResults, ReportGenerator, ResultStorage, WeatherReadings
import sys

calculationObject = CalculationsResults.CalculationsResults()
report = ReportGenerator.ReportGenerator()

# generated year report
def yearReport(year):
    try: #check if year entered is valid
        if (int(year) > 2019):
            print("Invalid Year")
            return
    except:
        print("Invalid year")
        return
    requiredDays = calculationObject.monthsOfYear(year)
    result = calculationObject.calculateForGivenDays(requiredDays)
    report.yearReport(result)

#generate month's report
def monthReport(yearMonth):
    month, year = extractMonthYear(yearMonth)
    if (month == None or year == None):
        return
    daysofMonth = calculationObject.daysOfMonth(month, year)
    resultMonthavg = calculationObject.avgCalculation(daysofMonth)
    report.monthReport(resultMonthavg)

#draw charts
def barChart(yearMonth):
    month, year = extractMonthYear(yearMonth)
    if (month == None or year == None):
        return
    daysofMonth = calculationObject.daysOfMonth(month, year)
    report.drawBarCharts(daysofMonth, calculationObject.weatherData,month,year)
    report.drawSingleChart(daysofMonth, calculationObject.weatherData,month,year)

#Seperate year and month and check if it's valid or not
def extractMonthYear(yearMonth):
    try:
        year = yearMonth[:4]
        month = yearMonth[5:]
        intYear = int(year)
        intMonth = int(month)
        if (intMonth in range(13)):
            return month, year
    except:
        print("Invalid month or year")
        return None, None

#read arguments from comand line and taking appropriate actions
i = 1
while (i < len(sys.argv)):
    if ((len(sys.argv)-1) < i+1):
        print("Invalid Command")
    elif (sys.argv[i] == "-e"):
        yearReport(sys.argv[i+1])
    elif (sys.argv[i] == "-a"):
        monthReport(sys.argv[i+1])
    elif (sys.argv[i] == "-c"):
        barChart(sys.argv[i+1])
    else:
        print("Invalid Command")
    i += 2
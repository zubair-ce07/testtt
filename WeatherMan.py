import FileReader, CalculationsResults, ReportGenerator, ResultStorage, WeatherReadings
import sys

calculationObject = CalculationsResults.CalculationsResults()
report = ReportGenerator.ReportGenerator()

def yearReport(year):
    requiredDays = calculationObject.monthsOfYear(year)
    result = calculationObject.calculateForGivenDays(requiredDays)
    report.yearReport(result)

def monthReport(yearMonth):
    year = yearMonth[:4]
    month = yearMonth[5:]
    daysofMonth = calculationObject.daysOfMonth(month, year)
    resultMonthavg = calculationObject.avgCalculation(daysofMonth)
    report.monthReport(resultMonthavg)

def barChart(yearMonth):
    year = yearMonth[:4]
    month = yearMonth[5:]
    daysofMonth = calculationObject.daysOfMonth(month, year)
    report.drawBarCharts(daysofMonth, calculationObject.weatherData,month,year)
    report.drawSingleChart(daysofMonth, calculationObject.weatherData,month,year)

i = 1
while (i < len(sys.argv)):
    if (sys.argv[i] == "-e"):
        yearReport(sys.argv[i+1])
    elif (sys.argv[i] == "-a"):
        monthReport(sys.argv[i+1])
    elif (sys.argv[i] == "-c"):
        barChart(sys.argv[i+1])
    else:
        print("Invalid Command")
    i += 2
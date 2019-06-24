import WeatherDataExtractor, CalculationsResults, ReportGenerator, ResultStorage, WeatherReadings
import sys

calculationObject = CalculationsResults.CalculationsResults()
def extractMonthYear(yearMonth):
    try:
        year = yearMonth[:4]
        month = yearMonth[5:]
        intYear = int(year)
        intMonth = int(month)
        if (intMonth in range(13)):
            return intMonth, year
    except:
        print("Invalid month or year")
        return None, None

i = 1
while (i < len(sys.argv)):
    if ((len(sys.argv)-1) < i+1):
        print("Invalid Command")
    elif (sys.argv[i] == "-e"):
        report = ReportGenerator.ReportGenerator(sys.argv[i + 1][:4], None, calculationObject)
        report.yearReport()
    elif (sys.argv[i] == "-a"):
        month, year = extractMonthYear(sys.argv[i + 1])
        report = ReportGenerator.ReportGenerator(year, month, calculationObject)
        report.monthReport()
    elif (sys.argv[i] == "-c"):
        month, year = extractMonthYear(sys.argv[i + 1])
        report = ReportGenerator.ReportGenerator(year, month, calculationObject)
        report.drawBarCharts()
        report.drawSingleChart()
    else:
        print("Invalid Command")
    i += 2

    # Seperate year and month and check if it's valid or not






'''
# generated year report
def yearReport(year):
    try: #check if year entered is valid
        if (int(year) > 2019):
            print("Invalid Year")
            return
    except:
        print("Invalid year")
        return
    #requiredDays = calculationObject.monthsOfYear(year)
    result = calculationObject.calculateForGivenDays()
    report.yearReport(result)

#generate month's report
def monthReport(yearMonth):
    month, year = extractMonthYear(yearMonth)
    if (month == None or year == None):
        return
    #daysofMonth = calculationObject.daysOfMonth(month, year)
    resultMonthavg = calculationObject.avgCalculation()
    report.monthReport(resultMonthavg)

#draw charts
def barChart(yearMonth):
    month, year = extractMonthYear(yearMonth)
    if (month == None or year == None):
        return
    #daysofMonth = calculationObject.daysOfMonth(month, year)
    report.drawBarCharts(calculationObject.weatherData,month,year)
    report.drawSingleChart(calculationObject.weatherData,month,year)


'''
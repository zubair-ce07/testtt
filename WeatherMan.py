import FileReader, CalculationsResults, ReportGenerator, ResultStorage, WeatherReadings
import sys
check = CalculationsResults.CalculationsResults()
requiredDays = check.monthsOfYear("2007")
result = check.calculateForGivenDays(requiredDays)
report = ReportGenerator.ReportGenerator()
report.yearReport(result)

daysofMonth = check.daysOfMonth("6","2007")
resultMonthavg = check.avgCalculation(daysofMonth)
report.monthReport(resultMonthavg)

monthHighestNLowest = check.calculateForGivenDays(daysofMonth)
report.monthReport(monthHighestNLowest) #change

report.drawBarCharts(daysofMonth,check.weatherData)
report.drawSingleChart(daysofMonth,check.weatherData)

print(sys.argv)
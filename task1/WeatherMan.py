import WeatherDataExtractor, CalculationsResults, ReportGenerator, ResultStorage, WeatherReadings
import sys

calculation_object = CalculationsResults.CalculationsResults()


def extract_month_year(year_month):
    try:
        required_year = year_month[:4]
        required_month = year_month[5:]
        int(required_year)
        int_month = int(required_month)
        if int_month in range(13):
            return int_month, required_year
    except ValueError:
        print("Invalid month or year")
        return None, None


i = 1
while i < len(sys.argv):
    if (len(sys.argv)-1) < i+1:
        print("Invalid Command")
    elif sys.argv[i] == "-e":
        report = ReportGenerator.ReportGenerator(sys.argv[i + 1][:4], None, calculation_object)
        report.year_report()
    elif sys.argv[i] == "-a":
        month, year = extract_month_year(sys.argv[i + 1])
        report = ReportGenerator.ReportGenerator(year, month, calculation_object)
        report.month_report()
    elif sys.argv[i] == "-c":
        month, year = extract_month_year(sys.argv[i + 1])
        report = ReportGenerator.ReportGenerator(year, month, calculation_object)
        report.draw_bar_charts()
        report.draw_single_chart()
    else:
        print("Invalid Command")
    i += 2

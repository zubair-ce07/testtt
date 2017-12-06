import sys
from Reports.yearlyreport import YearlyReport
from Reports.monthlyreport import MonthlyReport
from Reports.monthlybarreport import MonthlyBarReport
from Parsers.weatherparser import WeatherParser


class WeatherMan:

    @staticmethod
    def main():

        parser = WeatherParser()
        yearly_reports = []
        monthly_reports = []
        monthly_bar_reports = []
        if len(sys.argv) < 2:
            print("Incomplete arguments")
            return
        path = sys.argv[1]

        for index in range(2, len(sys.argv), 2):
            if sys.argv[index] == "-e":
                yearly_reports.append(sys.argv[index+1])
            elif sys.argv[index] == "-a":
                monthly_reports.append(sys.argv[index+1])
            elif sys.argv[index] == "-c":
                monthly_bar_reports.append(sys.argv[index + 1])

        for report_year in yearly_reports:

            if len(report_year.split('/')) != 1:
                print("Argument "+report_year+" is invalid for option -e.")

            weather = parser.parse(path, report_year)
            if(weather is not None):
                report = YearlyReport()
                report.print(weather)

        for report_month in monthly_reports:

            if len(report_month.split('/')) != 2:
                print("Argument "+report_month+" is invalid for option -a.")
                continue

            year = report_month.split('/')[0]
            month = report_month.split('/')[1]
            weather = parser.parse(path, year, int(month))
            if (weather is not None):
                report = MonthlyReport()
                report.print(weather)

        for report_month in monthly_bar_reports:

            if len(report_month.split('/')) != 2:
                print("Argument "+report_month+" is invalid for option -c.")
                continue

            year = report_month.split('/')[0]
            month = report_month.split('/')[1]
            weather = parser.parse(path, year, int(month))
            
            if (weather is not None):
                report = MonthlyBarReport()
                report.print(weather, year)

        return

if __name__ == "__main__":
    WeatherMan.main()

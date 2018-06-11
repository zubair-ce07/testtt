from PopulateWeatherData import WeatherFilesData
from AnnualResultCalculator import AnnualResultCalculator
from MonthlyResultCalculator import MonthlyResutCalculator
import argparse
from DrawMonthlyPlot import DrawMonthlyPlot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processing weather report ')
    parser.add_argument('YearDate', type=str, nargs='+',
                        help='Weather Data Report')
    args = parser.parse_args()
    print(args.YearDate)
    weatherData = WeatherFilesData()
    weatherData.populate_file_names_list()
    wdata = weatherData.populate_data_structures()
    for i in args.YearDate:
        checkstr = i.split('/')
        if len(checkstr) == 1:
            resultCalc = AnnualResultCalculator()
            resultCalc.do_year_wise_calculation(wdata, i)
        else:
            resultCalc = MonthlyResutCalculator()
            resultCalc.do_month_wise_calculation(wdata, i)
            drawPlot = DrawMonthlyPlot()
            drawPlot.draw(wdata, i)

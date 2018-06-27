from PopulateWeatherData import WeatherFilesData
from AnnualResultCalculator import AnnualResultCalculator
from MonthlyResultCalculator import MonthlyResutCalculator
import argparse
from DrawMonthlyPlot import DrawMonthlyPlot


def get_args():
    parser = argparse.ArgumentParser(description='Processing weather report ')
    parser.add_argument('-a')
    parser.add_argument('-c')
    parser.add_argument('-e')
    parser.add_argument('path')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    weatherData = WeatherFilesData()
    wdata = weatherData.populate_data_structures(args.path)
    if args.a:
        resultCalc = AnnualResultCalculator()
        resultCalc.do_year_wise_calculation(wdata, args.a)
    if args.e:
        resultCalc = MonthlyResutCalculator()
        resultCalc.do_month_wise_calculation(wdata, args.e)
    if args.c:
        drawPlot = DrawMonthlyPlot()
        drawPlot.draw(wdata, args.c)

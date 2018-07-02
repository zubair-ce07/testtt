import sys
import argparse

import WeatherCalc
import WeatherDataReader
import Results
import ReportGenerator


def process_e(argument, data):
    highestTemp = WeatherCalc.WeatherCalc().highest_temp_of_year(argument, data)
    lowestTemp = WeatherCalc.WeatherCalc().lowest_temp_of_year(argument, data)
    highestHum = WeatherCalc.WeatherCalc().highest_hum_of_year(argument, data)
    dateMaxAnnualHum = [data[highestHum[0]][highestHum[1]].day,
                        data[highestHum[0]][highestHum[1]].month,
                        data[highestHum[0]][highestHum[1]].year]
    dateMaxAnnualTemp = [data[highestTemp[0]][highestTemp[1]].day,
                        data[highestTemp[0]][highestTemp[1]].month,
                        data[highestTemp[0]][highestTemp[1]].year]
    dateMinAnnualTemp = [data[lowestTemp[0]][lowestTemp[1]].day,
                        data[lowestTemp[0]][lowestTemp[1]].month,
                        data[lowestTemp[0]][lowestTemp[1]].year]
    maxAnnualHum = data[highestHum[0]][highestHum[1]].highestH
    minAnnualTemp = data[lowestTemp[0]][highestHum[1]].lowestT
    maxAnnualTemp = data[highestTemp[0]][highestTemp[1]].highestT
    result = Results.Results(date_max_annual_temp=dateMaxAnnualTemp,
                             date_max_annual_hum=dateMaxAnnualHum,
                             date_min_annual_temp=dateMinAnnualTemp,
                             max_annual_hum=maxAnnualHum,
                             max_annual_temp=maxAnnualTemp,
                             min_annual_temp=minAnnualTemp)
    ReportGenerator.ReportGenerator().report_e(result)


def process_a(argument, data):
    maxavgTemp = WeatherCalc.WeatherCalc().highest_avg_temp_of_month(
        int(argument[0]), int(argument[1]), data)
    minavgTemp = WeatherCalc.WeatherCalc().lowest_avg_temp_of_month(
        int(argument[0]), int(argument[1]), data)
    meanavgHum = WeatherCalc.WeatherCalc().average_mean_humidity_of_month(
        int(argument[0]), int(argument[1]), data)
    result = Results.Results(mean_avg_hum=meanavgHum,
                             min_avg_temp=minavgTemp,
                             max_avg_temp=maxavgTemp)
    ReportGenerator.ReportGenerator().report_a(result)


def process_c(argument, data):
    ReportGenerator.ReportGenerator().report_c(int(argument[0]), int(argument[1]), data)


def process_d(argument, data):
    ReportGenerator.ReportGenerator().report_d(int(argument[0]), int(argument[1]), data)


def run(mypath, args):
    weather_data = WeatherDataReader.WeatherDataReader().read(mypath)
    if args.type_e:
        process_e(args.type_e, weather_data)
    if args.type_a:
        arguments = args.type_a.split('/')
        process_a(arguments, weather_data)
    if args.type_c:
        arguments = args.type_c.split('/')
        process_c(arguments, weather_data)
    if args.type_d:
        arguments = args.type_d.split('/')
        process_d(arguments, weather_data)


def main():
    my_path = 'weatherfiles'
    parser = argparse.ArgumentParser(
        description="Report will be generated according to the Arguments")
    parser.add_argument("-e", "--type_e", type=int, help="Annual Report")
    parser.add_argument("-a", "--type_a", type=str, help="Monthly Report")
    parser.add_argument("-c", "--type_c", type=str, help="Dual Bar Chart")
    parser.add_argument("-d", "--type_d", type=str, help="Single Bar Chart")
    args = parser.parse_args()
    run(my_path, args)


if __name__ == '__main__':
    main()

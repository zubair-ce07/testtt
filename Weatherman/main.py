import sys
import WeatherCalc
import WeatherDataReader
import Results
import ReportGenerator


def process(data, arguments):
    for argument in arguments:
        if argument[0] == 'e':
            process_e(argument, data)
        elif argument[0] == 'a':
            process_a(argument, data)
        elif argument[0] == 'c':
            process_c(argument, data)
        elif argument[0] == 'd':
            process_d(argument, data)
        else:
            print("There is something wrong with the arguments")


def process_e(argument, data):
    highestTemp = WeatherCalc.WeatherCalc().highest_temp_of_year(argument[1], data)
    lowestTemp = WeatherCalc.WeatherCalc().lowest_temp_of_year(argument[1], data)
    highestHum = WeatherCalc.WeatherCalc().highest_hum_of_year(argument[1], data)
    result = Results.Results()
    result.dateMaxAnnualHum = [data[highestHum[0]][highestHum[1]].day,
                               data[highestHum[0]][highestHum[1]].month,
                               data[highestHum[0]][highestHum[1]].year]
    result.dateMaxAnnualTemp = [data[highestTemp[0]][highestTemp[1]].day,
                               data[highestTemp[0]][highestTemp[1]].month,
                               data[highestTemp[0]][highestTemp[1]].year]
    result.dateMinAnnualTemp = [data[lowestTemp[0]][lowestTemp[1]].day,
                               data[lowestTemp[0]][lowestTemp[1]].month,
                               data[lowestTemp[0]][lowestTemp[1]].year]
    result.maxAnnualHum = data[highestHum[0]][highestHum[1]].highestH
    result.minAnnualTemp = data[lowestTemp[0]][highestHum[1]].lowestT
    result.maxAnnualTemp = data[highestTemp[0]][highestTemp[1]].highestT
    ReportGenerator.ReportGenerator().report_e(result)


def process_a(argument, data):
    maxavgTemp = WeatherCalc.WeatherCalc().highest_avg_temp_of_month(argument[1], argument[2], data)
    minavgTemp = WeatherCalc.WeatherCalc().lowest_avg_temp_of_month(argument[1], argument[2], data)
    meanavgHum = WeatherCalc.WeatherCalc().average_mean_humidity_of_month(argument[1], argument[2], data)
    result = Results.Results()
    result.avgMeanHumOfMonth = meanavgHum
    result.minAvgTempOfMonth = minavgTemp
    result.maxAvgTempOfMonth = maxavgTemp
    ReportGenerator.ReportGenerator().report_a(result)


def process_c(argument, data):
    ReportGenerator.ReportGenerator().report_c(argument[1], argument[2], data)


def process_d(argument, data):
    ReportGenerator.ReportGenerator().report_d(argument[1], argument[2], data)


def run(mypath, args):
    my_args = []
    for a in range(0, len(args), 2):
        my_args.append(args[a:a + 2])
    for arguments in my_args:
        arguments[0] = arguments[0][1]
        if arguments[1].isdigit():
            arguments[1] = int(arguments[1])
        else:
            second = arguments[1].split('/')
            arguments[1] = int(second[0])
            arguments.append(int(second[1]))
    data = WeatherDataReader.WeatherDataReader().read(mypath)
    process(data, my_args)


def main():
    my_path = 'weatherfiles'
    args = sys.argv
    args = args[1:]
    run(my_path, args)


main()

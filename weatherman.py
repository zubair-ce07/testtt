import os
import sys
import datetime


class WeatherReading:
    def __init__(self, pkt, max_tempc, mean_tempc, min_tempc, dewpointc, mean_dewpointc, min_dewpointc, max_humidity,
                 mean_humidity, min_humidity, max_sealevelpressurehpa, mean_sealevelpressurehpa,
                 min_sealevelpressurehpa,
                 max_visibilitykm, mean_visibilitykm, min_visibilitykm, max_windspeedkmh, mean_windspeedkmh,
                 max_gustspeedkmh, precipitationcm, cloudcover, events, windirdegrees):
        self.pkt = pkt
        self.max_tempc = max_tempc
        self.mean_tempc = mean_tempc
        self.min_tempc = min_tempc
        self.dewpointc = dewpointc
        self.mean_dewpointc = mean_dewpointc
        self.min_dewpointc = min_dewpointc
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sealevelpressurehpa = max_sealevelpressurehpa
        self.mean_sealevelpressurehpa = mean_sealevelpressurehpa
        self.min_sealevelpressurehpa = min_sealevelpressurehpa
        self.max_visibilitykm = max_visibilitykm
        self.mean_visibilitykm = mean_visibilitykm
        self.min_visibilitykm = min_visibilitykm
        self.max_windspeedkmh = max_windspeedkmh
        self.mean_windspeedkmh = mean_windspeedkmh
        self.max_gustspeedkmh = max_gustspeedkmh
        self.precipitationcm = precipitationcm
        self.cloudcover = cloudcover
        self.events = events
        self.windirdegrees = windirdegrees


class WeatherCalculations:
    def __init__(self, max_temp, max_temp_day, min_temp, min_temp_day, humidity, humidity_day):
        self.max_temp = max_temp
        self.max_temp_day = max_temp_day
        self.min_temp = min_temp
        self.min_temp_day = min_temp_day
        self.humidity = humidity
        self.humidity_day = humidity_day


class ParseAndPopulate:
    def read_file(self, filename):
        file_data = {}
        with open("weatherdata/" + filename, 'r') as fp:
            temp_line = fp.readline()
            while temp_line == "\n":
                temp_line = fp.readline()
            for line in fp.readlines():
                reading = self.create_weather_reading(line)
                if reading is not None:
                    file_data[reading.pkt] = reading
        return file_data

    def create_weather_reading(self, data):
        data = data.strip().split(',')
        if len(data) is 23:
            return WeatherReading(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],
                                  data[9],
                                  data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17],
                                  data[18],
                                  data[19], data[20], data[21], data[22])

    def read_data(self, year, directory_name):
        year_data = {}
        files = os.listdir(directory_name)
        for file in files:
            if str(year) in file:
                year_data[file] = self.read_file(file)
        return year_data


class Calculate:
    def get_day(self, date):
        date_splitted = date.split('-')
        months = (
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December")
        month = months[int(date_splitted[1]) - 1] + ' ' + date_splitted[2]
        return month

    def case_generic(self, readings):
        # highest and lowest temprature and day, most humid day and its humidity
        max_temp = 0
        max_temp_day = ""
        min_temp = 1000
        min_temp_day = ""
        humidity = 0
        humidity_day = ""
        for reading in readings:
            for date in readings[reading]:
                if readings[reading][date].max_tempc != '' and int(readings[reading][date].max_tempc) > max_temp:
                    max_temp = int(readings[reading][date].max_tempc)
                    max_temp_day = self.get_day(date)
                if readings[reading][date].min_tempc != '' and int(readings[reading][date].min_tempc) < min_temp:
                    min_temp = int(readings[reading][date].min_tempc)
                    min_temp_day = self.get_day(date)
                if readings[reading][date].max_humidity != '' and int(readings[reading][date].max_humidity) > humidity:
                    humidity = int(readings[reading][date].max_humidity)
                    humidity_day = self.get_day(date)

        return WeatherCalculations(max_temp, max_temp_day, min_temp, min_temp_day, humidity, humidity_day)

    def case_average(self, readings, year, month):
        # average highest and lowest temprature and day, average mean humid day and its humidity
        file_name = "lahore_weather_" + year + "_" + datetime.date(year=int(year), month=int(month), day=1).strftime(
            '%b') + ".txt"
        max_temp = 0
        max_temp_mean = 0
        min_temp = 1000
        min_temp_mean = 0
        humidity = 0
        count = 0
        mean = 0
        for date in readings[file_name]:
            if readings[file_name][date].mean_tempc != '' and int(readings[file_name][date].mean_tempc) > max_temp:
                max_temp_mean += int(readings[file_name][date].max_tempc)
            if readings[file_name][date].mean_tempc != '' and int(readings[file_name][date].mean_tempc) < min_temp:
                min_temp_mean += int(readings[file_name][date].min_tempc)
            if readings[file_name][date].mean_humidity != '' and int(
                    readings[file_name][date].mean_humidity) > humidity:
                    mean += int(readings[file_name][date].max_humidity)
                    count += 1
        max_temp = int(max_temp_mean / count)
        min_temp = int(min_temp_mean / count)
        humidity = int(mean / count)

        return WeatherCalculations(max_temp, "", min_temp, "", humidity, "")

    def case_bar_charts(self, readings, year, month):
        file_name = "lahore_weather_" + year + "_" + datetime.date(year=int(year), month=int(month), day=1).strftime(
            '%b') + ".txt"
        day = 1
        print(datetime.date(month=int(month), year=int(year), day=1).strftime('%B'), year)
        print()
        for date in readings[file_name]:
            if readings[file_name][date].max_tempc != '':
                print(day, sep=' ', end='', flush=True)
                for i in range(int(readings[file_name][date].max_tempc)):
                    print("\033[01;31;40m +", sep=' ', end='', flush=True)
                print(' ' + readings[file_name][date].max_tempc + 'C', sep=' ', end='', flush=True)
                print()
            if readings[file_name][date].min_tempc != '':
                print(day, sep=' ', end='', flush=True)
                for i in range(int(readings[file_name][date].min_tempc)):
                    print("\033[1;34;40m +", sep=' ', end='', flush=True)
                print(' ' + readings[file_name][date].min_tempc + 'C', sep=' ', end='', flush=True)
                print()
                print()
            day += 1
        print("\033[0;34;39m", sep=' ', end='', flush=True)

    def calculate_report(self, readings, case, year, month):
        if case == '-e':
            return self.case_generic(readings)
        elif case == '-a':
            return self.case_average(readings, year, month)
        elif case == '-c':
            self.case_bar_charts(readings, year, month)
            return 0
        else:
            return -1


class ReportGeneration:
    def case_generic(self, calculations):
        print("Highest:", calculations.max_temp, "C on", calculations.max_temp_day)
        print("Lowest:", calculations.min_temp, "C on", calculations.min_temp_day)
        print("Humidity:", calculations.humidity, "% on", calculations.humidity_day)

    def case_average(self, calculations):
        print("Highest Average:", calculations.max_temp, "C")
        print("Lowest Average:", calculations.min_temp, "C")
        print("Mean Humidity:", calculations.humidity, "%")

    def print_report(self, calculations, case):
        if case == '-e':
            self.case_generic(calculations)
        elif case == '-a':
            self.case_average(calculations)
        elif case == '-c':
            print("No report to be generated")
        else:
            print("Invalid case provided!")


def main():
    dir_path = sys.argv[1]
    i = 2
    report = 1
    while i < len(sys.argv):
        print("REPORT ", report)
        case = sys.argv[i]
        year = 0
        month = 0
        if case == '-e':
            year = int(sys.argv[i + 1])
        elif case == '-c' or case == '-a':
            year = sys.argv[i + 1].split('/')[0]
            month = sys.argv[i + 1].split('/')[1]

        # multiple reports as well

        parser = ParseAndPopulate()
        data = parser.read_data(year, dir_path)
        calculator = Calculate()
        calculations = calculator.calculate_report(data, case, year, month)
        if calculations != -1:
            reportgen = ReportGeneration()
            reportgen.print_report(calculations, case)
        else:
            print("Invalid case was provided!")
        i += 2
        report += 1
        print()


main()

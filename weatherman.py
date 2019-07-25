import csv
import glob
from datetime import datetime
import argparse


class ReportGenerator:
    def __init__(self, weather_record):
        self.weather_record = weather_record
        self.cal = Calculations()

    def report_for_year(self):
        self.cal.calculations_for_year(self.weather_record)
        print("Highest: %dC on %s" % (self.cal.maxTemp.MaxTemperature, self.cal.maxTemp.PKT.strftime('%B %-d')))
        print("Lowest: %dC on %s" % (self.cal.minTemp.MinTemperature, self.cal.minTemp.PKT.strftime('%B %-d')))
        print("Humidity: {}% on {}".format(self.cal.maxHumidity.MaxHumidity, self.cal.maxHumidity.PKT.strftime('%B %-d')))

    def report_for_month(self):
        self.cal.calculations_for_month(self.weather_record)
        print("Highest Average: {}C".format(self.cal.avgHighestTemp))
        print("Lowest Average: {}C".format(self.cal.avgLowestTemp))
        print("Average Mean Humidity: {}%".format(self.cal.avgMeanHumidity))

    def bar_charts(self):
        for r in self.weather_record.records:
            max_t = r.MaxTemperature
            min_t = r.MinTemperature
            if max_t:
                bar = ''
                for i in range(0, self.cal.take_mod(max_t)):
                    bar += '+'
                print(r.PKT.strftime('%d') + "\033[1;31m " + bar + "\033[0;37m " + str(r.MaxTemperature)+"C")
            if min_t:
                bar = ''
                for i in range(0, self.cal.take_mod(min_t)):
                    bar += '+'
                print(r.PKT.strftime('%d') + "\033[1;34m " + bar + "\033[0;37m " + str(r.MinTemperature)+"C")


class Calculations:

    def __init__(self):
        # for yearly reports
        self.maxTemp = None
        self.minTemp = None
        self.maxHumidity = None
        # for monthly reports
        self.avgHighestTemp = None
        self.avgLowestTemp = None
        self.avgMeanHumidity = None

    def calculations_for_year(self, weather_record):
        self.maxTemp = max([r for r in weather_record.records if r.MaxTemperature is not None],
                           key=lambda x: x.MaxTemperature)
        self.minTemp = min([r for r in weather_record.records if r.MinTemperature is not None],
                           key=lambda x: x.MinTemperature)
        self.maxHumidity = max([r for r in weather_record.records if r.MaxHumidity is not None],
                               key=lambda x: x.MaxHumidity)

    def calculations_for_month(self, weather_record):
        readings1 = [r.MaxTemperature for r in weather_record.records if r.MaxTemperature is not None]
        self.avgHighestTemp = sum(readings1)/float(len(readings1))
        readings2 = [r.MinTemperature for r in weather_record.records if r.MinTemperature is not None]
        self.avgLowestTemp = sum(readings2)/float(len(readings2))
        readings3 = [r.MeanHumidity for r in weather_record.records if r.MeanHumidity is not None]
        self.avgMeanHumidity = sum(readings3)/float(len(readings3))

    def take_mod(self, x):
        if x < 0:
            return x * -1
        else:
            return x


class WeatherData:

    def __init__(self, row):
        if row.get("PKT"):
            self.PKT = datetime.strptime(row.get('PKT'), '%Y-%m-%d')
        elif row.get("PKST"):
            self.PKT = datetime.strptime(row.get('PKST'), '%Y-%m-%d')
        if row['Max TemperatureC']:
            self.MaxTemperature = int(row['Max TemperatureC'])
        else:
            self.MaxTemperature = None
        if row['Mean TemperatureC']:
            self.MeanTemperature = int(row['Mean TemperatureC'])
        else:
            self.MeanTemperature = None
        if row['Min TemperatureC']:
            self.MinTemperature = int(row['Min TemperatureC'])
        else:
            self.MinTemperature = None
        if row['Max Humidity']:
            self.MaxHumidity = int(row['Max Humidity'])
        else:
            self.MaxHumidity = None
        if row[' Mean Humidity']:
            self.MeanHumidity = int(row[' Mean Humidity'])
        else:
            self.MeanHumidity = None
        if row[' Min Humidity']:
            self.MinHumidity = int(row[' Min Humidity'])
        else:
            self.MinHumidity = None


class WeatherRecord:

    def __init__(self, year, month='*'):
        self.year = year
        self.month = month
        self.records = []

        for file in glob.glob("weatherfiles/Murree_weather_"+self.year+"_"+self.month+".txt"):
            for row in csv.DictReader(open(file)):
                self.records.append(WeatherData(row))


if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument('-e', nargs='*')
    argParser.add_argument('-a', nargs='*')
    argParser.add_argument('-c', nargs='*')
    args = argParser.parse_args()

    if(args.e):
        for arg in args.e:
            print("For {}:".format(arg))
            weather_record = WeatherRecord(year=arg)
            report = ReportGenerator(weather_record)
            report.report_for_year()
            print("\n")

    if(args.a):
        for arg in args.a:
            print("For {}:".format(arg))
            year, month = arg.split("/")
            date = datetime(int(year), int(month), 20)
            month = date.strftime('%b')
            weather_record = WeatherRecord(year, month)
            report = ReportGenerator(weather_record)
            report.report_for_month()
            print("\n")

    if(args.c):
        for arg in args.c:
            print("For {}:".format(arg))
            year, month = arg.split("/")
            date = datetime(int(year), int(month), 20)
            month = date.strftime('%b')
            weather_record = WeatherRecord(year, month)
            report = ReportGenerator(weather_record)
            report.bar_charts()
            print("\n")

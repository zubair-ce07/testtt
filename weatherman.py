import argparse
import calendar
import csv
import os


WEATHER_READINGS = []


class Weather:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class FileParser:
    def __init__(self, directory_path):
        file_path = directory_path + '/'
        self.file_names = os.listdir(file_path)
        for file in self.file_names:
            read_file = csv.DictReader(open(file_path + file)
                                       , skipinitialspace=True, delimiter=',')
            for row in read_file:
                if 'PKT' in row:
                    w = Weather(row['PKT'], row['Max TemperatureC'], row['Min TemperatureC'], row['Max Humidity'],
                                row['Mean Humidity'])
                    WEATHER_READINGS.append(w)
                else:
                    w = Weather(row['PKST'], row['Max TemperatureC'], row['Min TemperatureC'], row['Max Humidity'],
                                row['Mean Humidity'])
                    WEATHER_READINGS.append(w)


class ResultComputer:
    def give_year_data(self, year):
        highest_temp = 0
        highest_temp_date = 0
        lowest_temp = 100
        lowest_temp_date = 0
        humidity = 0
        humidity_date = 0
        for reading in WEATHER_READINGS:
            if year == reading.date[0:4]:
                if reading.max_temp != '':
                    if int(reading.max_temp) > highest_temp:
                        highest_temp = int(reading.max_temp)
                        highest_temp_date = reading.date
                if reading.min_temp != '':
                    if int(reading.min_temp) < lowest_temp:
                        lowest_temp = int(reading.min_temp)
                        lowest_temp_date = reading.date
                if reading.max_humidity != '':
                    if int(reading.max_humidity) > humidity:
                        humidity = int(reading.max_humidity)
                        humidity_date = reading.date
        weather_dict = {
            "HighestTemp": str(highest_temp),
            "HighestTempMonth": calendar.month_name[int(highest_temp_date[5:6])],
            "HighestTempDay": highest_temp_date[7:],
            "LowestTemp": str(lowest_temp),
            "LowestTempMonth": calendar.month_name[int(lowest_temp_date[5:6])],
            "LowestTempDay": lowest_temp_date[7:],
            "Humidity": str(humidity),
            "HumidityMonth": calendar.month_name[int(humidity_date[5:6])],
            "HumidityDay": humidity_date[7:]
        }
        return weather_dict

    def give_month_data(self, year_month):
        highest_cumulative = 0
        highest_counter = 0
        lowest_cumulative = 0
        lowest_counter = 0
        humidity_cumulative = 0
        humidity_counter = 0
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6]:
                if reading.max_temp != '':
                    highest_cumulative = highest_cumulative + int(reading.max_temp)
                    highest_counter = highest_counter + 1
                if reading.min_temp != '':
                    lowest_cumulative = lowest_cumulative + int(reading.min_temp)
                    lowest_counter = lowest_counter + 1
                if reading.mean_humidity != '':
                    humidity_cumulative = humidity_cumulative + int(reading.mean_humidity)
                    humidity_counter = humidity_counter + 1
        highest_average = int(highest_cumulative / highest_counter)
        lowest_average = int(lowest_cumulative / lowest_counter)
        humidity_average = int(humidity_cumulative / humidity_counter)
        return highest_average, lowest_average, humidity_average


class GenerateReports:
    def generate_average_weather_report(self, highest_average, lowest_average, humidity_average):
        print("Highest Average: {}C".format(highest_average))
        print("Lowest Average: {}C".format(lowest_average))
        print("Average Mean Humidity: {}C".format(humidity_average))

    def generate_extreme_weather_report(self, highest_temp, highest_temp_month, highest_temp_day,
                                        lowest_temp, lowest_temp_month, lowest_temp_day,
                                        humidity, humidity_month, humidity_day):
        print("Highest: {}C on {} {}".format(highest_temp, highest_temp_month, highest_temp_day))
        print("Lowest: {}C on {} {}".format(lowest_temp, lowest_temp_month, lowest_temp_day))
        print("Humidity: {}C on {} {}".format(humidity, humidity_month, humidity_day))

    def generate_extreme_single_bar_report(self, year_month):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6]:
                if reading.max_temp != '':
                    print(reading.max_temp[7:] + ' ' + '\033[91m' + '+' * int(reading.max_temp)
                          + '\033[94m' + '+' * int(reading.min_temp) + '\033[0m' +
                          " " + reading.max_temp + "C" + " " + reading.min_temp + "C")

    def generate_extreme_double_bar_report(self, year_month):
        print(calendar.month_name[int(year_month[-1:])] + " " + year_month[:4])
        for reading in WEATHER_READINGS:
            if year_month[0:4] == reading.date[0:4] and year_month[-1:] == reading.date[5:6]:
                if reading.max_temp != '':
                    print(reading.date[7:] + ' ' + '\033[91m' + '+' * int(reading.max_temp) +
                          '\033[0m' + " " + reading.max_temp + "C")
                if reading.min_temp != '':
                    print(reading.date[7:] + ' ' + '\033[94m' + '+' * int(reading.min_temp)
                          + '\033[0m' + " " + reading.min_temp + "C")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', help='Insert path of the files')
    parser.add_argument('-e', '--extreme', help='Insert year e.g 2005')
    parser.add_argument('-a', '--average', help='Insert year and month e.g 2006/4')
    parser.add_argument('-c', '--bar', help='Insert year and month e.g 2006/4')
    parser.add_argument('-b', '--bonus', help='Insert year and month e.g 2006/4')
    args = parser.parse_args()

    if not os.path.isdir(args.dir_path):
        print("Error, file path not found")
    else:
        f = FileParser(args.dir_path)

        c = ResultComputer()

        g = GenerateReports()

        if args.extreme:
            weather_dict = c.give_year_data(args.extreme)
            g.generate_extreme_weather_report(weather_dict["HighestTemp"], weather_dict["HighestTempMonth"],
                                              weather_dict["HighestTempDay"], weather_dict["LowestTemp"],
                                              weather_dict["LowestTempMonth"], weather_dict["LowestTempDay"],
                                              weather_dict["Humidity"], weather_dict["HumidityMonth"],
                                              weather_dict["HumidityDay"])
        if args.average:
            highest_average, lowest_average, humidity_average = c.give_month_data(args.average)
            g.generate_average_weather_report(highest_average, lowest_average, humidity_average)
        if args.bar:
            g.generate_extreme_double_bar_report(args.bar)
        if args.bonus:
            g.generate_extreme_single_bar_report(args.bonus)


if '__main__' == __name__:
    main()

import os
import sys
import datetime


class WeatherReading:
    """
    Data structure for storing weather readings that have been read and parsed by the parser

    """

    def __init__(self, pakistan_time="", max_tempc=0, mean_tempc=0, min_tempc=0, dewpointc=0, mean_dewpointc=0.0,
                 min_dewpointc=0, max_humidity=0,
                 mean_humidity=0.0, min_humidity=0, max_sealevelpressurehpa=0, mean_sealevelpressurehpa=0.0,
                 min_sealevelpressurehpa=0,
                 max_visibilitykm=0, mean_visibilitykm=0.0, min_visibilitykm=0, max_windspeedkmh=0,
                 mean_windspeedkmh=0.0,
                 max_gustspeedkmh=0, precipitationcm=0, cloudcover=0, events="", windirdegrees=0.0):
        self.pakistan_time = pakistan_time
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


class WeatherReportData:
    """
    Data structure for storing report type specific calculations calculated by the weather report calculator on
    weather readings

    """

    def __init__(self, max_temp=0, max_temp_day="", min_temp=0, min_temp_day="", humidity=0, humidity_day=""):
        self.max_temp = max_temp
        self.max_temp_day = max_temp_day
        self.min_temp = min_temp
        self.min_temp_day = min_temp_day
        self.humidity = humidity
        self.humidity_day = humidity_day


class WeatherDataParser:
    """
    Receives year and weather data directory path as input and returns weather data of that whole year in a nested
    dictionary. First level of nesting contains month data and second level of nesting contains day wise data each in
    a separate WeatherReading data structure.

    """

    def read_file_from_weather_data(self, filename):
        """
        Receives filename of a weather data file and returns a dictionary of WeatherReading data structures for
        each line in the file (which represents a single day)

        :param filename:
        :return: weather data of that file
        """
        file_data = {}
        with open("weatherdata/{}".format(filename), 'r') as file_cursor:
            temp_line = file_cursor.readline()
            while temp_line == "\n":
                temp_line = file_cursor.readline()
            for line in file_cursor.readlines():
                reading = self.create_weather_reading_from_data(line)
                if reading:
                    file_data[reading.pakistan_time] = reading
        return file_data

    def create_weather_reading_from_data(self, data):
        data = data.strip().split(',')
        if len(data) is 23:
            return WeatherReading(pakistan_time=data[0], max_tempc=data[1], mean_tempc=data[2], min_tempc=data[3],
                                  dewpointc=data[4], mean_dewpointc=data[5], min_dewpointc=data[6],
                                  max_humidity=data[7], mean_humidity=data[8],
                                  min_humidity=data[9],
                                  max_sealevelpressurehpa=data[10], mean_sealevelpressurehpa=data[11],
                                  min_sealevelpressurehpa=data[12], max_visibilitykm=data[13],
                                  mean_visibilitykm=data[14], min_visibilitykm=data[15], max_windspeedkmh=data[16],
                                  mean_windspeedkmh=data[17],
                                  max_gustspeedkmh=data[18],
                                  precipitationcm=data[19], cloudcover=data[20], events=data[21],
                                  windirdegrees=data[22])

    def read_data_year_wise(self, year, directory_name):
        """
        Takes year and the directory path of the weather data directory as input and returns data of that year

        :param year:
        :param directory_name:
        :return: year data
        """
        year_data = {}
        files_in_directory = os.listdir(directory_name)
        for file in files_in_directory:
            if str(year) in file:
                year_data[file] = self.read_file_from_weather_data(file)
        return year_data


class WeatherReportCalculator:
    """
    Receives weather data readings, report type, year and month and calculates required report related
    calculations of the given year and month

    """

    def get_day_from_date(self, date):
        """
        Returns day and month from given date. Month will be the full name of that month
        :param date:
        :return: a string in 'day(in digits) Month(full name)
        """
        date_splitted = date.split('-')
        months = (
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December")
        month = "{} {}".format(months[int(date_splitted[1]) - 1], date_splitted[2])
        return month

    def generate_readings(self):
        pass

    def is_given(self, reading):
        return reading is not ''

    def report_type_generic(self, readings):
        """
        Calculates highest temperature, lowest temperature and the days these temperatures were recorded as well as
        the most humid day in the given data and the humidity on that day
        :param readings:
        :returns: WeatherCalculation data structure populated with calculated values
        """
        max_temp = 0
        max_temp_day = ""
        min_temp = 1000
        min_temp_day = ""
        humidity = 0
        humidity_day = ""
        for key_month_data, month_data in readings.items():
            for key_day_data, day_data in month_data.items():
                if self.is_given(day_data.max_tempc) and int(day_data.max_tempc) > max_temp:
                    max_temp = int(day_data.max_tempc)
                    max_temp_day = self.get_day_from_date(key_day_data)
                if self.is_given(day_data.min_tempc) and int(day_data.min_tempc) < min_temp:
                    min_temp = int(day_data.min_tempc)
                    min_temp_day = self.get_day_from_date(key_day_data)
                if self.is_given(day_data.max_humidity) and int(day_data.max_humidity) > humidity:
                    humidity = int(day_data.max_humidity)
                    humidity_day = self.get_day_from_date(key_day_data)

        return WeatherReportData(max_temp=max_temp, max_temp_day=max_temp_day, min_temp=min_temp,
                                 min_temp_day=min_temp_day, humidity=humidity, humidity_day=humidity_day)

    def report_type_average(self, readings, filename):
        """
        Calculates the highest average temperature, lowest average temperature and the mean humidity recorded in the
        weather readings

        :param filename:
        :param readings:
        :returns: WeatherCalculation data structure populated with calculated values
        """
        max_temp = 0
        max_temp_mean = 0
        min_temp = 1000
        min_temp_mean = 0
        humidity = 0
        count = 0
        mean = 0
        for key_day_data, day_data in readings[filename].items():
            if self.is_given(day_data.mean_tempc) and int(day_data.mean_tempc) > max_temp:
                max_temp_mean += int(day_data.max_tempc)
            if self.is_given(day_data.mean_tempc) and int(day_data.mean_tempc) < min_temp:
                min_temp_mean += int(day_data.min_tempc)
            if self.is_given(day_data.mean_humidity) and int(day_data.mean_humidity) > humidity:
                mean += int(day_data.max_humidity)
                count += 1
        max_temp = int(max_temp_mean / count)
        min_temp = int(min_temp_mean / count)
        humidity = int(mean / count)

        return WeatherReportData(max_temp=max_temp, min_temp=min_temp, humidity=humidity)

    def report_type_bar_charts(self, readings, year, month, filename):
        """
        Prints horizontal bar charts on console for the highest and temperature of each day in a given month and
        year

        :param filename:
        :param readings:
        :param year:
        :param month:
        :return:
        """

        day = 1
        print(datetime.date(month=int(month), year=int(year), day=1).strftime('%B'), year)
        print()
        for date in readings[filename]:
            if readings[filename][date].max_tempc != '':
                print(day, sep=' ', end='', flush=True)
                for i in range(int(readings[filename][date].max_tempc)):
                    print("\033[01;31;40m +", sep=' ', end='', flush=True)
                print(' ' + readings[filename][date].max_tempc + 'C', sep=' ', end='', flush=True)
                print()
            if readings[filename][date].min_tempc != '':
                print(day, sep=' ', end='', flush=True)
                for i in range(int(readings[filename][date].min_tempc)):
                    print("\033[1;34;40m +", sep=' ', end='', flush=True)
                print(' ' + readings[filename][date].min_tempc + 'C', sep=' ', end='', flush=True)
                print()
                print()
            day += 1
        print("\033[0;34;39m", sep=' ', end='', flush=True)
        return 0

    def generate_required_report(self, readings, report_type, year, month):
        """
        Calculates required report from given year and month

        :param readings:
        :param report_type:
        :param year:
        :param month:
        :returns: Calculations or response code (0 for bar chart report and -1 for unknown report type
        """

        file_name = "lahore_weather_{}_{}.txt".format(year,
                                                      datetime.date(year=int(year), month=int(month), day=1).strftime(
                                                          '%b'))
        if report_type == '-e':
            return self.report_type_generic(readings)
        elif report_type == '-a':
            return self.report_type_average(readings, file_name)
        elif report_type == '-c':
            return self.report_type_bar_charts(readings=readings, year=year, month=month, filename=file_name)
        else:
            return -1


class WeatherReportGenerator:
    """
    Prints required report type

    """

    def report_type_generic(self, calculations):
        print("Highest:", calculations.max_temp, "C on", calculations.max_temp_day)
        print("Lowest:", calculations.min_temp, "C on", calculations.min_temp_day)
        print("Humidity:", calculations.humidity, "% on", calculations.humidity_day)

    def report_type_average(self, calculations):
        print("Highest Average:", calculations.max_temp, "C")
        print("Lowest Average:", calculations.min_temp, "C")
        print("Mean Humidity:", calculations.humidity, "%")

    def print_report(self, calculations, report_type):
        """
        Prints required report type


        :param calculations:
        :param report_type:
        :return:
        """
        if report_type == '-e':
            self.report_type_generic(calculations)
        elif report_type == '-a':
            self.report_type_average(calculations)
        elif report_type == '-c':
            print("No report to be generated")
        else:
            print("Invalid case provided!")


def main():
    """
    Driver function

    """
    directory_path = sys.argv[1]
    i = 2
    report = 1
    while i < len(sys.argv):
        print("REPORT ", report)
        report_type = sys.argv[i]
        year = 1
        month = 1
        if report_type == '-e':
            year = int(sys.argv[i + 1])
        elif report_type == '-c' or report_type == '-a':
            year = sys.argv[i + 1].split('/')[0]
            month = sys.argv[i + 1].split('/')[1]

        parser = WeatherDataParser()
        data = parser.read_data_year_wise(year, directory_path)
        calculator = WeatherReportCalculator()
        calculations = calculator.generate_required_report(data, report_type, year, month)
        if calculations != -1:
            report_generator = WeatherReportGenerator()
            report_generator.print_report(calculations, report_type)
        else:
            print("Invalid case was provided!")
        i += 2
        report += 1
        print()


main()

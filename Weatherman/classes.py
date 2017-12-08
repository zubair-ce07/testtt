import datetime


class WeatherReading:

    def __init__(self, row):

        self.pkt = row['PKT'] if 'PKT' in row else row['PKST']

        self.reading_date = datetime.datetime.strptime(self.pkt, '%Y-%m-%d')

        raw_value = row['Max TemperatureC']
        self.max_temp = int(raw_value) if raw_value else raw_value

        raw_value = row['Min TemperatureC']
        self.min_temp = int(raw_value) if raw_value else raw_value

        raw_value = row['Max Humidity']
        self.max_humidity = int(raw_value) if raw_value else raw_value

        raw_value = row[' Mean Humidity']
        self.mean_humidity = int(raw_value) if raw_value else raw_value

    def get_month_day(self):

        return self.reading_date.strftime("%B %d")                 # print(mydate.strftime("%A %d. %b %Y"))

    def get_month_year(self):

        return self.reading_date.strftime("%B %Y")

    def get_day(self):

        return self.reading_date.strftime("%d")


class YearlyWeatherReport:

    def __init__(self):

        self.complete_records = []
        self.max_temp_row = ''
        self.min_temp_row = ''
        self.max_humidity_row = ''

    def print_report(self):

        print "Highest: {0}C on {1}".format(self.max_temp_row.max_temp, self.max_temp_row.get_month_day())
        print "Lowest: {0}C on {1}".format(self.min_temp_row.min_temp, self.min_temp_row.get_month_day())
        print "Humidity: {0}% on {1} \n".format(self.max_humidity_row.max_humidity, self.max_humidity_row.get_month_day())


class MonthlyReport:

    def __init__(self):
        self.complete_records = []
        self.total_max_temp = 0
        self.total_min_temp = 0
        self.total_mean_humidity = 0
        self.max_temp_count = 0
        self.min_temp_count = 0
        self.mean_humidity_count = 0

    def print_report(self):

        print 'Highest Average: {0}C'.format(self.total_max_temp / self.max_temp_count)
        print 'Lowest Average: {0}C'.format(self.total_min_temp / self.min_temp_count)
        print 'Average Mean Humidity: {0}%'.format(self.total_mean_humidity / self.mean_humidity_count)
        print ' '


class MonthlyRecordBars:

    def __init__(self):

        self.max_temp_values = []
        self.min_temp_values = []
        self.days = []
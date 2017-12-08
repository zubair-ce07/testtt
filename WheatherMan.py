import glob
import datetime
import calendar
import argparse
import csv


class ForecastReport:
    maximum_temperature = 0
    minimum_temperature = 0
    maximum_humidity = 0
    maximum_temperature_date = ""
    minimum_temperature_date = ""
    maximum_humidity_date = ""
    maximum_temperature_mean = 0
    minimum_temperature_mean = 0
    average_humidity = 0
    barchart = []
    barchart_bonus = []

    @staticmethod
    def extract_data(file_name):
        with open(file_name, "r") as f:
            file_data = f.readlines()
            return file_data

    def find_max_temp(self, file_name):
        for file in glob.glob(file_name):
            file_data = self.extract_data(file)
            del file_data[0]
            for line in file_data:
                words = line.split(",")
                try:
                    maximum = int(words[1])
                except ValueError:
                    maximum = 0
                if maximum > self.maximum_temperature:
                    self.maximum_temperature = maximum
                    self.maximum_temperature_date = words[0]
                try:
                    minimum = int(words[3])
                except ValueError:
                    minimum = 0
                if minimum < self.minimum_temperature:
                    self.minimum_temperature = minimum
                    self.minimum_temperature_date = words[0]
                try:
                    humidity = int(words[7])
                except ValueError:
                    humidity = 0
                if humidity > self.maximum_humidity:
                    self.maximum_humidity = humidity
                    self.maximum_humidity_date = words[0]

    def report_mean(self, file_name):
        maximum_mean = 0
        minimum_mean = 0
        average_humidity = 0
        total_days = 1
        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    maximum_mean += int(row['Max TemperatureC'])
                except ValueError:
                    maximum_mean += 0
                try:
                    minimum_mean += int(row['Min TemperatureC'])
                except ValueError:
                    minimum_mean += 0
                try:
                    average_humidity += int(row['Max Humidity'])
                except ValueError:
                    average_humidity += 0
                total_days += 1
        self.maximum_temperature_mean = int(maximum_mean/total_days)
        self.minimum_temperature_mean = int(minimum_mean/total_days)
        self.average_humidity = int(average_humidity/total_days)

    def report_barchart(self, file_name):
        red = '\033[31m'
        blue = '\033[34m'
        black = '\033[30m'
        file_data = self.extract_data(file_name)
        del file_data[0]
        index = 1
        for line in file_data:
            day_num = str(index)
            words = line.split(",")
            try:
                maximum_temp = int(words[1])
            except ValueError:
                maximum_temp = 0
            barchart_maximum = '+' * maximum_temp
            self.barchart.append(day_num.zfill(2) + " " + red+barchart_maximum + " " + black + str(maximum_temp) + "C")
            try:
                minimum_temp = int(words[3])
            except ValueError:
                minimum_temp = 0
            barchart_minimum = '+' * minimum_temp
            self.barchart.append(day_num.zfill(2) + " " + blue+barchart_minimum + " " + black + str(minimum_temp) + "C")
            index += 1

    def process_data(self, file_data):
        red = '\033[31m'
        blue = '\033[34m'
        black = '\033[30m'
        index = 1
        del file_data[0]
        for line in file_data:
            words = line.split(",")
            try:
                max_temp = int(words[1])
            except ValueError:
                max_temp = 0
            barchart_maximum = "+" * max_temp
            try:
                min_temp = int(words[3])
            except ValueError:
                min_temp = 0
            barchart_minimum = "+" * min_temp
            day_num = str(index)
            self.barchart_bonus.append(day_num.zfill(2)+" " + blue + barchart_minimum
                                       + red + barchart_maximum + black +
                                       str(min_temp) + "C -" + str(max_temp) + "C")
            index += 1

    def report_bonus(self, file_name):
        file_data = self.extract_data(file_name)
        self.process_data(file_data)
        self.print_barchart_bonus()

    def print_max(self):
        black = '\033[30m'
        mydate_max = datetime.datetime.strptime(self.maximum_temperature_date, '%Y-%m-%d')
        mydate_min = datetime.datetime.strptime(self.minimum_temperature_date, '%Y-%m-%d')
        mydate_hum = datetime.datetime.strptime(self.maximum_humidity_date, '%Y-%m-%d')
        print(black+"Higest:" + str(self.maximum_temperature) + "C on " + mydate_max.strftime('%B %d'))
        print(black+"Lowest:" + str(self.minimum_temperature) + "C on " + mydate_min.strftime('%B %d'))
        print(black+"Humidity:" + str(self.maximum_humidity) + "% on " + mydate_hum.strftime('%B %d'))
        print("")

    def print_average(self):
        black = '\033[30m'
        print(black+"Highest Avergae:"+str(self.maximum_temperature_mean)+"C")
        print(black+"Lowest Avergae:" + str(self.minimum_temperature_mean) + "C")
        print(black+"Avergae Mean Humidity:" + str(self.average_humidity) + "%")
        print("")

    def print_barchart(self):
        for bar in self.barchart:
            print(bar)

    def print_barchart_bonus(self):
        for bar in self.barchart_bonus:
            print(bar)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to files")
    parser.add_argument('-e', metavar='N', nargs='+')
    parser.add_argument('-a', metavar='N', nargs='+')
    parser.add_argument('-c', metavar='N', nargs='+')

    list_parameters = parser.parse_args()
    path = list_parameters.path + "Murree_weather_"
    report = ForecastReport()

    if list_parameters.e is not None:
        year = list_parameters.e[0]
        file_name = path + year + "_*.txt"
        report.find_max_temp(file_name)
        report.print_max()

    if list_parameters.a is not None:
        file_name = ""
        for arguments in list_parameters.a:
            year_month = arguments.split('/')
            year = year_month[0]
            month = year_month[1]
            month = calendar.month_name[int(month)]
            month = month[0:3]
            file_name = path + year + "_" + month + ".txt"
        report.report_mean(file_name)
        report.print_average()

    if list_parameters.c is not None:
        file_name = ""
        for arguments in list_parameters.a:
            year_month = arguments.split('/')
            year = year_month[0]
            month = year_month[1]
            month = calendar.month_name[int(month)]
            month = month[0:3]
            file_name = path + year + "_" + month + ".txt"
        report.report_barchart(file_name)
        report.print_barchart()
        report.report_bonus(file_name)

if __name__ == '__main__':
    main()

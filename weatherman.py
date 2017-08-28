import datetime
import os
import csv
import argparse


class Filling:
    def __init__(self):
        self.file_names = []
        self.datelist = []
        self.max_temp_of_days = []
        self.max_temp_of_months = []
        self.date_max_temp_months = []
        self.lowest_temp_of_months = []
        self.lowest_temp_months_dates = []
        self.min_temp = []
        self.max_humidity = []
        self.max_humidity_month = []
        self.max_humidity_date = []
        self.mean_humidity = []

    def parse_int(self, list):
        return map(int, list)

    def store_filenames(self, directory, year, month_number):
        hasfile = False
        for root, dirs, files in os.walk(directory):
            for file_path in files:
                if month_number is None:
                    if file_path.endswith('.txt'):
                        if year in file_path:
                            self.file_names.append(file_path)
                            hasfile = True
                elif month_number is not None:
                    month_number = int(month_number)
                    yyyy = int(year)
                    month = datetime.date(yyyy, month_number, 1).strftime('%B')
                    if file_path.endswith(month[:3] + '.txt'):
                        if year in file_path:
                            self.file_names.append(file_path)
                            hasfile = True
        if hasfile == False:
            print("No File Found for this year")
            exit()

    def read_file(self, file_path):
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            for row in reader:
                if (row[header[1]] != ''):
                    self.datelist.append(row[header[0]])
                    self.max_temp_of_days.append(row[header[1]])
                    self.min_temp.append(row[header[3]])
                    self.mean_humidity.append(row[header[8]])
                    self.max_humidity.append(row[header[7]])
        self.max_temp_of_days = self.parse_int(self.max_temp_of_days)
        self.max_temp_of_months = self.parse_int(self.max_temp_of_months)
        self.min_temp = self.parse_int(self.min_temp)
        self.mean_humidity = self.parse_int(self.mean_humidity)
        self.max_humidity = self.parse_int(self.max_humidity)


class Computation:
    def __init__(self, filling):
        self.filling = filling

    def convert_date_format(self, datestr):
        datel = datestr.split('-')
        dateint = map(int, datel)
        month = datetime.date(dateint[0],dateint[1],
                                          dateint[1]).strftime('%B')
        return month + " " + str(dateint[2])

    def avg_max_temp(self):
        return sum(self.filling.max_temp_of_days) / len(self.filling.datelist)

    def avg_min_temp(self):
        return sum(self.filling.min_temp) / len(self.filling.datelist)

    def avg_mean_humidity(self):
        return sum(i for i in self.filling.mean_humidity)/len(self.filling.datelist)

    def find_max_temp_of_months(self, path):
        for i in range(0, len(self.filling.file_names) - 1):
            abs_path = path + '/' + self.filling.file_names[i]
            self.filling.read_file(abs_path)
            self.filling.max_temp_of_months.append(max(self.filling.max_temp_of_days))
            self.filling.date_max_temp_months.append(self.filling.datelist[
                                             self.filling.max_temp_of_days.index(max(self.filling.max_temp_of_days))])
            self.filling.lowest_temp_of_months.append(min(self.filling.min_temp))
            self.filling.lowest_temp_months_dates.append(self.filling.
                                              datelist[self.filling.min_temp.index(min(self.filling.min_temp))])
            self.filling.max_humidity_month.append(max(self.filling.max_humidity))
            self.filling.max_humidity_date.append(self.filling.datelist[
                                               self.filling.max_humidity.index(max(self.filling.max_humidity))])
            self.filling.max_temp_of_days = []
            self.filling.min_temp = []
            self.filling.max_humidity = []
            self.filling.datelist = []

    def highest_temp_bar(self, number):
        return "\033[0;31m"  + "+" * number + "\033[0;30m"

    def lowest_temp_bar(self, number):
        return "\033[0;34m" + "+" * number + "\033[0;30m"


class Report:
    filling = Filling()
    computution = Computation(filling)

    def show_monthly_avg(self):
        print("Average Highest Temperature::"
                   + str(self.computution.avg_max_temp()) + "C")
        print("Average Lowest  Temperature::"
                   + str(self.computution.avg_max_temp())+ "C")
        print("Average Mean Humidity::"
                   + str(self.computution.avg_max_temp()) + "%")

    def disjoin_horizontal_bar(self):
        for i in range(0, len(self.filling.max_temp_of_days)):
            print(self.filling.datelist[i]+" "+ self.computution.highest_temp_bar(
                       self.filling.max_temp_of_days[i]) + " " + str(self.filling.max_temp_of_days[i]) + "C")
            print(self.filling.datelist[i] + " " + self.computution.lowest_temp_bar(
                    self.filling.min_temp[i]) + " " + str(self.filling.min_temp[i]) + "C")

    def single_horizontal_bar(self):
        for i in range(0, len(self.filling.max_temp_of_days)):
            print(self.filling.datelist[i]+ " " + self.computution.lowest_temp_bar(
                       self.filling.min_temp[i]) + self.computution.highest_temp_bar( self.filling.max_temp_of_days[i])
                               + " " + str(self.filling.min_temp[i]) + "C-" + str(self.filling.max_temp_of_days[i]) + "C")

    def show_year(self):
        print("Highest: " + str(max(self.filling.max_temp_of_months)) + "C on "
                  + self.computution.convert_date_format(self.filling.date_max_temp_months[
                                 self.filling.max_temp_of_months.index(max(self.filling.max_temp_of_months))]))
        print("Lowest: " + str(min(self.filling.lowest_temp_of_months)) + "C on "
                   + self.computution.convert_date_format(self.filling.lowest_temp_months_dates[
                                 self.filling.lowest_temp_of_months.index(min(self.filling.lowest_temp_of_months))]))
        print("Humidity: " + str(max(self.filling.max_humidity_month)) + "% on "
                   + self.computution.convert_date_format(self.filling.max_humidity_date[
                                 self.filling.max_humidity_month.index(max(self.filling.max_humidity_month))]))

    def given_year(self, path, year, month_number):
        if year.isdigit():
            self.filling.store_filenames(path, year, month_number)
            self.computution.find_max_temp_of_months(path)
            self.show_year()
        else:
            print("\033[0;31m"
                  + "Year should be digit")

    def given_month(self, path, year, month_number, cmd):
        if (year.isdigit() and
                month_number.isdigit()):
            self.filling.store_filenames(path, year, month_number)
            abs_path = os.path.join(path, self.filling.file_names[0])
            self.filling.read_file(abs_path)
            if cmd == "-c":
                self.disjoin_horizontal_bar()
                self.single_horizontal_bar()
            elif cmd == "-a":
                month = datetime.date(int(year), int(month_number), 01)\
                    .strftime('%B')
                print(month + " " + year)
                self.show_monthly_avg()
        else:
            print("\033[0;31m" + "Year and Month should be digit")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help= 'Enter Command', type=str)
    parser.add_argument('-c', type=str)
    parser.add_argument('-a', type=str)
    parser.add_argument('-e', type=str)
    args = parser.parse_args()
    path = args.path
    report = Report()
    cmd = []
    if args.e is not None:
        report.given_year(path, args.e, None)
    if args.a is not None:
        year_month = args.a.split('/')
        report.given_month(path, year_month[0], year_month[1], '-a')
    if args.c is not None:
        year_month = args.c.split('/')
        report.given_month(path, year_month[0], year_month[1], '-c')
    else:
        print("Command is wrong")
else:
    print("path not found")

import calendar
import csv
import datetime


class Reports:

    def show_yearly_results(self, highest_temp_year, lowest_temp_year, most_humid_day_year):

        print("Highest: " + str(highest_temp_year.values()[0]) + "C on "
              + calendar.month_name[datetime.datetime.strptime(str(highest_temp_year.keys()[0]), '%Y-%m-%d').month]
              + " " + str(datetime.datetime.strptime(str(highest_temp_year.keys()[0]), '%Y-%m-%d').day))

        print("Lowest: " + str(lowest_temp_year.values()[0]) + "C on "
              + calendar.month_name[datetime.datetime.strptime(str(lowest_temp_year.keys()[0]), '%Y-%m-%d').month]
              + " " + str(datetime.datetime.strptime(str(lowest_temp_year.keys()[0]), '%Y-%m-%d').day))

        print("Humidity: " + str(most_humid_day_year.values()[0]) + "% on "
              + calendar.month_name[datetime.datetime.strptime(most_humid_day_year.keys()[0], '%Y-%m-%d').month]
              + " " + str(datetime.datetime.strptime(str(most_humid_day_year.keys()[0]), '%Y-%m-%d').day))

    def show_monthly_avgs(self, avg_highest_monthly, avg_lowest_monthly, avg_mean_humidity):

        print("Highest Average: " + str(avg_highest_monthly) + "C")
        print("Lowest Average: " + str(avg_lowest_monthly) + "C")
        print("Average Mean Humidity: " + str(avg_mean_humidity) + "%")

    def show_monthly_temps(self, path, month, bonus):

        month_n = month.split('/')[1]
        temp_path = path + "/Murree_weather_" + month.split('/')[0] + "_" + calendar.month_abbr[int(month_n)] + ".txt"
        csv_file = open(temp_path)
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for day in csv_reader:
            high = ""
            low = ""
            if (day['Max TemperatureC'] != ""):
                for t_max in range(0, int(day['Max TemperatureC'])):
                    high = high + "+"
            if (day['Min TemperatureC'] != ""):
                for t_min in range(0, int(day['Min TemperatureC'])):
                    low = low + "+"
            low = '\033[34m' + low + '\033[30m'
            high = '\033[31m' + high + '\033[30m'
            if (bonus):
                print(str(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d').day) + " " + high +
                      low + day['Max TemperatureC'] + "C - " + day['Min TemperatureC'] + "C ")
            else:
                print(str(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d').day) + " " + high +
                      day['Max TemperatureC'] + "C")
                print(str(datetime.datetime.strptime(day.get('PKT', day.get('PKST')), '%Y-%m-%d').day) + " " + low +
                      day['Min TemperatureC'] + "C")
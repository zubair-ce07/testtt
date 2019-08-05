import copy
import csv
import sys
import os
from data import data  


class read_file:
    def read_year(year,list_month,list_year,day,month_check,dic):
        list_month.clear()
        list_year.clear()
        for count in range(12):
            day.clear()
            try:
                with open("Murree_weather_"+str(year) + '_' +
                        month_check[count]+".txt", "r") as csvFile:
                    reader = csv.reader(csvFile)
                    next(reader)
                    for data in reader:
                        dic.update([('PKT', data[0]),
                                    ('Max TemperatureC',
                                    data[1]), ('Min TemperatureC', data[3]),
                                    ('Max Humidity', data[7]),
                                    ('Mean Humidity',
                                    data[8])])
                        day.append(copy.deepcopy(dic))
                list_month.append(copy.deepcopy(day))
                csvFile.close()
            except IOError:
                list_month.append(None)


    def read_months(month, year,list_month,list_year,dic,day):
        list_month.clear()
        list_year.clear()
        day.clear()
        try:
            with open("Murree_weather_{year}_{month}.txt".format(year=year, month=month), "r") as csvFile:
                reader = csv.reader(csvFile)
                next(reader)
                for data in reader:
                    dic.update([('PKT', data[0]),
                                ('Max TemperatureC',
                                data[1]), ('Min TemperatureC', data[3]),
                                ('Max Humidity', data[7]),
                                ('Mean Humidity',
                                data[8])])
                    day.append(copy.deepcopy(dic))
                list_year.append(copy.deepcopy(day))
                csvFile.close()
        except IOError:
            list_year.append(None)



    def read_one_month(month, year,list_month,list_year,dic,day):
        list_month.clear()
        list_year.clear()
        day.clear()
        try:
            with open("Murree_weather_{year}_{month}.txt".format(year=year, month=month), "r") as csvFile:
                reader = csv.reader(csvFile)
                next(reader)
                for data in reader:
                    dic.update([('PKT', data[0]),
                                ('Max TemperatureC',
                                data[1]), ('Min TemperatureC', data[3]),
                                ('Max Humidity', data[7]),
                                ('Mean Humidity',
                                data[8])])
                    day.append(copy.deepcopy(dic))
            csvFile.close()
        except IOError:
            list_year.append(None)
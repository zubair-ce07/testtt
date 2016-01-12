import glob
import os
import sys
import csv


# calculate the min and max values
def weather_compare(date, max_temp, min_temp,
                    max_humidity, min_humidity, year):
    if max_temp != '':
        if int(max_temp) > int(weather_dic[year]['Max_Temp_Dic']['Max_Temp']):
            weather_dic[year]['Max_Temp_Dic']['Max_Temp'] = max_temp
            weather_dic[year]['Max_Temp_Dic']['date'] = date

    if min_temp != '':
        if int(min_temp) < int(weather_dic[year]['Min_Temp_Dic']['Min_Temp']) or \
                        weather_dic[year]['Min_Temp_Dic']['Min_Temp'] == '':
            weather_dic[year]['Min_Temp_Dic']['Min_Temp'] = min_temp
            weather_dic[year]['Min_Temp_Dic']['date'] = date

    if max_humidity != '':
        if int(max_humidity) > int(weather_dic[year]['Max_Humidity']):
            weather_dic[year]['Max_Humidity'] = max_humidity
    if min_humidity != '':
        if int(min_humidity) < int(weather_dic[year]['Min_Humidity']) or \
                        weather_dic[year]['Min_Humidity'] == '':
            weather_dic[year]['Min_Humidity'] = min_humidity


# assign values to empty parameters
def value_replace(year):
    if weather_dic[year]['Max_Temp_Dic']['Max_Temp'] == '':
        weather_dic[year]['Max_Temp_Dic']['Max_Temp'] = -1000

    if weather_dic[year]['Min_Temp_Dic']['Min_Temp'] == '':
        weather_dic[year]['Min_Temp_Dic']['Min_Temp'] = 1000

    if weather_dic[year]['Max_Humidity'] == '':
        weather_dic[year]['Max_Humidity'] = -1000

    if weather_dic[year]['Min_Humidity'] == '':
        weather_dic[year]['Min_Humidity'] = 1000


# Read data From File
def read_weather_data(data_directory):
    os.chdir(data_directory)

    for file_name in glob.glob("*.txt"):
        with open(file_name) as csvfile:
            next(csvfile, None)
            file_data = csv.DictReader(csvfile)
            for weather_variables in file_data:
                if 'PKT' in weather_variables:
                    collect_results(weather_variables['PKT'], weather_variables)
                else:
                    collect_results(weather_variables['PKST'], weather_variables)


def collect_results(date, weather_variables):
    year = date.split('-')

    if year[0] not in weather_dic and len(year[0]) > 2:
        weather_dic[year[0]] = {'Max_Temp_Dic': {'date': date,
                                                 'Max_Temp': weather_variables['Max TemperatureC']},
                                'Min_Temp_Dic': {'date': date,
                                                 'Min_Temp': weather_variables['Min TemperatureC']},
                                'Max_Humidity': weather_variables['Max Humidity'],
                                'Min_Humidity': weather_variables[' Min Humidity']}

        value_replace(year[0])
    else:
        if len(year[0]) > 2:
            weather_compare(date, weather_variables['Max TemperatureC'],
                            weather_variables['Min TemperatureC'], weather_variables['Max Humidity'],
                            weather_variables[' Min Humidity'], year[0])


def report_annual():
    print "Annual Max/Min Temperature" + '\n'
    print "   Year 	" + "MAX Temp 	" + "MIN Temp 	" + "MAX Humidity 	" + "MIN Humidity 	"
    print '\n' + "   -------------------------------------------------------------------------"

    for key in weather_dic:
        print "   " + key + "		 " + weather_dic[key]['Max_Temp_Dic']['Max_Temp'] + "	 	  " + \
              weather_dic[key]['Min_Temp_Dic']['Min_Temp'] + "		   " + weather_dic[key][
                  'Max_Humidity'] + " 	    	  " + weather_dic[key]['Min_Humidity']
    print '\n'


def report_coolday():
    print "Hottest Day Of Each Year" + '\n'
    print "   Year 	 " + "  Date 	" + "MAX Temp"
    print '\n' + "   ------------------------------------"

    for key in weather_dic:
        print "   " + key + " 	" + weather_dic[key]['Max_Temp_Dic']['date'] + " 	 " + \
              weather_dic[key]['Max_Temp_Dic']['Max_Temp']
    print '\n'


def report_hotday():
    print "Cooldest Day of Each Year" '\n'
    print "   Year 	 " + "  Date 	" + "MIN Temp"
    print '\n' + "   ------------------------------------"

    for key in weather_dic:
        print "   " + key + " 	" + weather_dic[key]['Min_Temp_Dic']['date'] + " 	 " + \
              weather_dic[key]['Min_Temp_Dic']['Min_Temp']
    print '\n'


def main():
    arg_list = []
    for arg in sys.argv:
        arg_list.append(arg)
    if len(arg_list) > 1:

        read_weather_data(arg_list[2])

        if int(arg_list[1]) == 1:
            report_annual()

        if int(arg_list[1]) == 2:
            report_coolday()

        if int(arg_list[1]) == 3:
            report_hotday()
    else:
        read_weather_data('weatherdata')
        report_annual()
        report_coolday()
        report_hotday()


weather_dic = {}
if __name__ == "__main__":
    main()

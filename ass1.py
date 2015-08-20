import sys
import glob
import csv
import argparse
import re
from collections import namedtuple
from weather import Weather

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    
    l.sort(key=alphanum_key)
    return l

		
def read_files(directory):
		
    # Read all files
    list_of_file_names = glob.glob(directory+ "/*.txt")
	
    w = Weather('', '', '', '', '', 0)
    weather_list = [w]
		
    # Traverse all files of all years	
    maximunTemp = None
    minimunTemp = None
    maximumHumidity = None
    minimumHumidity = None
    date = ""
    year = 0

		
    for i in range(len(list_of_file_names)):						
        with open(list_of_file_names[i], 'rb') as csvfile:
            next(csvfile)
            reader1 = csv.DictReader(csvfile)
               
            # Traverse all the lines of a file
            for line in reader1:
		    			
                if(line['Max TemperatureC'] != None):
                    date = line.get('PKT') or line.get('PKST')
                    maximunTemp = line['Max TemperatureC']
                    minimunTemp = line['Min TemperatureC']
                    minimumHumidity = line[' Min Humidity']
                    maximumHumidity = line['Max Humidity']
                    year = date.split('-');
                    year = int(year[0])
                    w1= Weather(maximunTemp, minimunTemp, maximumHumidity, minimumHumidity, date, year)
                    weather_list.append(w1)						
				
    return weather_list
	
	
def min_max_temperature(lowest_year, highest_year, weather_list):
    
    # Min/Max temperature
    print "Year        MAX Temp         MIN Temp         MAX Humidity         MIN Humidity"
    print "--------------------------------------------------------------------------------"

	
    year = lowest_year

    # Traverse for all years
    while (year <= highest_year):
	
        maximunTemp = 0
        minimunTemp = 10000
        maximumHumidity = 0
        minimumHumidity = 10000
        # Calculating for specific year
        for index in range(len(weather_list)):

            if(  weather_list[index].year == year and weather_list[index].max_temp != '' and int(weather_list[index].max_temp) > maximunTemp):
                maximunTemp = int(weather_list[index].max_temp)
            if( weather_list[index].year == year and  weather_list[index].min_temp != '' and int(weather_list[index].min_temp) <= minimunTemp):
                minimunTemp = int(weather_list[index].min_temp)
            if( weather_list[index].year == year and  weather_list[index].max_hum != '' and int(weather_list[index].max_hum) >= maximumHumidity):
                maximumHumidity = int(weather_list[index].max_hum)
            if( weather_list[index].year == year and  weather_list[index].min_hum != '' and int(weather_list[index].min_hum) <= minimumHumidity):
                minimumHumidity = int(weather_list[index].min_hum)
			
	    	
        print '{:4}'.format(year)+"             "+'{:5}'.format(maximunTemp)+"             "+'{:5}'.format(minimunTemp)+"            "+'{:5}'.format(maximumHumidity)+"            "+'{:5}'.format(minimumHumidity)			
        year = year + 1
   
    return None
	
	
def hottest_day(lowest_year, highest_year, weather_list):

    print "Year                Date                Temp"
    print "-----------------------------------------------"
	
    year = lowest_year
	
    # Traverse for all years
    while (year <= highest_year):
	
        maximunTemp = 0
        date = None
        # Calculating for specific year
        for index in range(len(weather_list)):

            if(  weather_list[index].year == year and weather_list[index].max_temp != '' and int(weather_list[index].max_temp) > maximunTemp):
                maximunTemp = int(weather_list[index].max_temp)
                date = weather_list[index].date
			    	
        print '{:4}'.format(year)+"             "+'{:10}'.format(date)+"             "+'{:5}'.format(maximunTemp)
        year = year + 1
		

    return None
	
	
def coolest_day(lowest_year, highest_year, weather_list):


    print "Year                Date                Temp"
    print "-----------------------------------------------"
	
    year = lowest_year
	
    # Traverse for all years
    while (year <= highest_year):
	
        minimunTemp = 10000
        date = None
        # Calculating for specific year
        for index in range(len(weather_list)):

            if(  weather_list[index].year == year and weather_list[index].min_temp != '' and int(weather_list[index].min_temp) < minimunTemp):
                minimunTemp = int(weather_list[index].min_temp)
                date = weather_list[index].date
			    	
        print '{:4}'.format(year)+"             "+'{:10}'.format(date)+"             "+'{:5}'.format(minimunTemp)
        year = year + 1
	

    return None

def application_usage_info():

        print "No arguments have been passed" 
        print "Usage: weatherman <report Number> <data_dir>"

        print "[Report Number]"
        print "1 for Annual Max/Min Temperature" 
        print "2 for Hottest day of each year"
        print "3 for coldest day of each year" 

        print "[data_dir]" 
        print "Directory containing weather data files"
        sys.exit();


def main(argv):
	
    
    if (argv.filename == '' or argv.num == 0):
		
        application_usage_info()
		
    elif(argv.filename != '' and argv.num != 0):
        directory = argv.filename
        reportNumber = argv.num
		
        weather_list = read_files(directory)
        del weather_list[0]
		
		
        # Read first file to get a year with lowest year
        list_of_file_names = glob.glob(directory+ "/*.txt")
        list_of_file_names = sort_nicely(list_of_file_names)
        lowest_year = list_of_file_names[0]
        highest_year = list_of_file_names[-1]
	
        lowest_year = lowest_year.split('/')
        lowest_year = lowest_year[-1]
        lowest_year = lowest_year.split('_')
        lowest_year = lowest_year[-2]
	
        highest_year = highest_year.split('/')
        highest_year = highest_year[-1]
        highest_year = highest_year.split('_')
        highest_year = highest_year[-2]
	
        highest_year = int(highest_year)
        lowest_year = int(lowest_year)
		
		
        if reportNumber == 1:
            min_max_temperature(lowest_year, highest_year, weather_list)
        elif reportNumber == 2:
            hottest_day(lowest_year, highest_year, weather_list)
        elif reportNumber == 3:
            coolest_day(lowest_year, highest_year, weather_list)
		
    return None
		
		
# Call main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Enter the number 1,2,3
    parser.add_argument('num', nargs='?', action="store", default=0, type=int, choices=[1, 2, 3])
    parser.add_argument('filename', nargs='?', action="store", default="", type=str)
    args = parser.parse_args()
    main(args)
	


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
		
    # Read first file to get a year with lowest year
    list1 = glob.glob(directory+ "/*.txt")
    list1 = sort_nicely(list1)
    lowest_year = list1[0]
    highest_year = list1[-1]
	
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
	
    year = lowest_year
	
    w = Weather(0, 0, 0, 0, "", "", 0)
    list2 = [w]
		
    # Traverse all files of all years
    while (year <= highest_year):
	
        list1 = glob.glob(directory+ "/*"+str(year)+ "*.txt");
			
        maximunTemp = 0
        minimunTemp = 10000
        maximumHumidity = 0
        minimumHumidity = 10000
        hottet_day_date = ""
        coolest_day_date = ""
		
        # Traverse all the files of a specific year
        for i in range(len(list1)):						
            with open(list1[i], 'rb') as csvfile:
                reader1 = csv.reader(csvfile, delimiter=',', quotechar='|')
                # Skip first two lines
                reader1.next()
                reader1.next()
               
                # Traverse all the lines of a file
                for line in reader1:
                    currentline = line
		    				
                    # Maximun temperature	
                    if((len(currentline) > 1) and currentline[1] != '' and (int(currentline[1]) >= maximunTemp)):
                        maximunTemp = int(currentline[1])
                        hottet_day_date = currentline[0]
				    	
                    # Min temperature
                    if(len(currentline) > 1 and currentline[3] != '' and int(currentline[3]) < minimunTemp):
                        minimunTemp = int(currentline[3])
                        coolest_day_date = currentline[0]
					
                    # Minimum Humidity
                    if(len(currentline) > 1 and currentline[9] != '' and int(currentline[9]) < minimumHumidity):
                        minimumHumidity = int(currentline[9])
				
                    # Maximum Humidity
                    if((len(currentline) > 1) and currentline[7] != '' and (int(currentline[7]) >= maximumHumidity)):
                        maximumHumidity = int(currentline[7])

        w1= Weather(maximunTemp, minimunTemp, maximumHumidity, minimumHumidity, hottet_day_date, coolest_day_date, year)
        list2.append(w1)
			
        year = year + 1
		
		
    return list2
	
	
def min_max_temperature(list2):

    # Min/Max temperature
    print "Year        MAX Temp         MIN Temp         MAX Humidity         MIN Humidity"
    print "--------------------------------------------------------------------------------"
	
    for index in range(len(list2)):
        print '{:4}'.format(list2[index].year)+"             "+'{:5}'.format(list2[index].max_temp)+"             "+'{:5}'.format(list2[index].min_temp)+"            "+'{:5}'.format(list2[index].max_hum)+"            "+'{:5}'.format(list2[index].min_hum)			

   
    return None
	
	
def hottest_day(list2):

    print "Year                Date                Temp"
    print "-----------------------------------------------"
	
    for index in range(len(list2)):
        print '{:4}'.format(list2[index].year)+"             "+'{:10}'.format(list2[index].hot_day)+"             "+'{:5}'.format(list2[index].max_temp)

    return None
	
	
def coolest_day(list2):


    print "Year                Date                Temp"
    print "-----------------------------------------------"
	
    for index in range(len(list2)):
        print '{:4}'.format(list2[index].year)+"             "+'{:10}'.format(list2[index].cool_day)+"             "+'{:5}'.format(list2[index].min_temp)

    return None


def main(argv):
	
    
    if (argv.filename == '' or argv.num == 0):
		
        print "No arguments have been passed" 
        print "Usage: weatherman <report Number> <data_dir>"

        print "[Report Number]"
        print "1 for Annual Max/Min Temperature" 
        print "2 for Hottest day of each year"
        print "3 for coldest day of each year" 

        print "[data_dir]" 
        print "Directory containing weather data files"
        sys.exit();
		
    elif(argv.filename != '' and argv.num != 0):
        directory = argv.filename
        reportNumber = argv.num
		
        list2 = read_files(directory)
        del list2[0]
		
        if reportNumber == 1:
            min_max_temperature(list2)
        elif reportNumber == 2:
            hottest_day(list2)
        elif reportNumber == 3:
            coolest_day(list2)
		
    return None
		
		
# Call main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Enter the number 1,2,3
    parser.add_argument('num', nargs='?', action="store", default=0, type=int, choices=[1, 2, 3])
    parser.add_argument('filename', nargs='?', action="store", default="", type=str)
    args = parser.parse_args()
    main(args)
	


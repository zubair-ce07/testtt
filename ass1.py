import sys
import glob
import csv
import argparse
import re

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

def min_max_temperature(lowest_year, highest_year, directory):

    year = lowest_year
    # Min/Max temperature
    print "Year        MAX Temp         MIN Temp         MAX Humidity         MIN Humidity"
    print "--------------------------------------------------------------------------------"
    # Traverse all files of all years
    while (year <= highest_year):
	
        list1 = glob.glob(directory+ "/*"+str(year)+ "*.txt");
			
        maximunTemp = 0
        minimunTemp = 10000
        maximumHumidity = 0
        minimumHumidity = 10000
		
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
				    	
                    # Min temperature
                    if(len(currentline) > 1 and currentline[3] != '' and int(currentline[3]) < minimunTemp):
                        minimunTemp = int(currentline[3])				
					
                    # Minimum Humidity
                    if(len(currentline) > 1 and currentline[9] != '' and int(currentline[9]) < minimumHumidity):
                        minimumHumidity = int(currentline[9])
				
                    # Maximum Humidity
                    if((len(currentline) > 1) and currentline[7] != '' and (int(currentline[7]) >= maximumHumidity)):
                        maximumHumidity = int(currentline[7])
							
        # Print the maximun temperature in specified format
        print '{:4}'.format(year)+"             "+'{:5}'.format(maximunTemp)+"             "+'{:5}'.format(minimunTemp)+"            "+'{:5}'.format(maximumHumidity)+"            "+'{:5}'.format(minimumHumidity)			
			
        year = year + 1;
    
    return None
	
	
def hottest_day(lowest_year, highest_year, directory):

    year = lowest_year
    print "Year                Date                Temp"
    print "-----------------------------------------------"
    # Traverse all files of all years
    while (year <= highest_year):
	
        list1 = glob.glob(directory+ "/*"+str(year)+ "*.txt");
			
        maximunTemp = 0
        hottet_day_date = ""
		
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
						
        # Print the maximun temperature in specified format
        print '{:4}'.format(year)+"             "+'{:10}'.format(hottet_day_date)+"             "+'{:5}'.format(maximunTemp)
			
        year = year + 1;
				    	

    return None
	
	
def coolest_day(lowest_year, highest_year, directory):

    year = lowest_year
    print "Year                Date                Temp"
    print "-----------------------------------------------"
    # Traverse all files of all years
    while (year <= highest_year):
	
        list1 = glob.glob(directory+ "/*"+str(year)+ "*.txt");
			
        minimunTemp = 10000
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
		    				
                    # Min temperature
                    if(len(currentline) > 1 and currentline[3] != '' and int(currentline[3]) < minimunTemp):
                        minimunTemp = int(currentline[3])
                        coolest_day_date = currentline[0]
						
        # Print the coolest day in specified format
        print '{:4}'.format(year)+"             "+'{:10}'.format(coolest_day_date)+"             "+'{:5}'.format(minimunTemp)
			
        year = year + 1;
				    	

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
		
        if reportNumber == 1:
            min_max_temperature(lowest_year, highest_year, directory)
        elif reportNumber == 2:
            hottest_day(lowest_year, highest_year, directory)
        elif reportNumber == 3:
            coolest_day(lowest_year, highest_year, directory)
		
    return None
		
		
# Call main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Enter the number 1,2,3
    parser.add_argument('num', nargs='?', action="store", default=0, type=int, choices=[1, 2, 3])
    parser.add_argument('filename', nargs='?', action="store", default="", type=str)
    args = parser.parse_args()
    main(args)
	


import sys
import glob
import csv


def generate_report(reportNumber, directory):
		
    # Read first file to get a year with lowest year
    list = glob.glob(directory+ "/*.txt")
    # sorted(list, key=numericalSort)
    print list
    lowest_year = list[0]
    highest_year = list[-1]	
    print highest_year
    year = 1996;
    if reportNumber == '1' :
        # Min/Max temperature
        print "Year        MAX Temp         MIN Temp         MAX Humidity         MIN Humidity"
        print "--------------------------------------------------------------------------------"
		
    elif reportNumber == '2' :
        print "Year                Date                Temp"
        print "-----------------------------------------------"

    elif reportNumber == '3' :
        print "Year                Date                Temp"
        print "-----------------------------------------------"

    #with open('/home/rosheen/Assignemnts/weatherdata/lahore_weather_1996_Dec.txt', 'rb') as csvfile:
     #   spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
      #  for row in spamreader:
       #         print ', '.join(row)
    # Traverse all files of all years
    while (year < 2012):
	
        list = glob.glob(directory+ "/*"+str(year)+ "*.txt");
			
        maximunTemp = 0
        minimunTemp = 10000
        maximumHumidity = 0
        minimumHumidity = 10000
        hottet_day_date = ""
        coolest_day_date = ""
		
        # Traverse all the files of a specific year
        for i in range(len(list)):						
            file = open(list[i], "r");
            with open(list[i], 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                # Skip first two lines
                spamreader.next()
                spamreader.next()
               
                # Traverse all the lines of a file
                for line in spamreader:
                    str1 = line[0]
                    line = str1
                    currentline = line.split(",");
		    				
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

        if reportNumber == '1' :			
            # Print the maximun temperature in specified format
            print '{:4}'.format(year)+"             "+'{:5}'.format(maximunTemp)+"             "+'{:5}'.format(minimunTemp)+"            "+'{:5}'.format(maximumHumidity)+"            "+'{:5}'.format(minimumHumidity)			
			
        elif reportNumber == '2' :
            print '{:4}'.format(year)+"             "+'{:10}'.format(hottet_day_date)+"             "+'{:5}'.format(maximunTemp)
			
        elif reportNumber == '3' :
            print '{:4}'.format(year)+"             "+'{:10}'.format(coolest_day_date)+"             "+'{:5}'.format(minimunTemp)
			
        year = year + 1;
		
		
    return None
		
	
def main(*argv):
	
    total = 0
	
    for i in argv:
        total = total + 1
	
    if (total < 2):
		
        print "No arguments have been passed" 
        print "Usage: weatherman <report Number> <data_dir>"

        print "[Report Number]"
        print "1 for Annual Max/Min Temperature" 
        print "2 for Hottest day of each year"
        print "3 for coldest day of each year" 

        print "[data_dir]" 
        print "Directory containing weather data files"
        sys.exit();
		
    elif(total >= 2):
        generate_report(argv[1], argv[2])
		
    return None
		
		
# Call main function
if __name__ == "__main__":
    main(*sys.argv)
	
	
# main();		
# main(1,"/home/rosheen/Assignemnts/weatherdata");

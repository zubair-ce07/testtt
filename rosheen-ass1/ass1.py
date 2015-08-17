import sys
import re
from os import walk
import glob;



def generateReport(reportNumber,directory):
	
	
	year=1996;
	if reportNumber== 1 :
		#Min /Max temperature
		print("Year        MAX Temp         MIN Temp         MAX Humidity         MIN Humidity")
		print ("---------------------------------------------------------------------------------------")
		
	elif reportNumber== 2 :
		print("Year                Date                Temp")
		print("-----------------------------------------------")

	elif reportNumber== 3 :
		print("Year                Date                Temp")
		print("-----------------------------------------------")
	
	while (year<2012):
		#list=glob.glob("/home/rosheen/Assignemnts/weatherdata/*"+str(year)+"*.txt");
		list=glob.glob(directory+"/*"+str(year)+"*.txt");
		
		
		maximunTemp=0;
		minimunTemp=10000;
		maximumHumidity=0;
		minimumHumidity=10000;
		Hottet_day_date="";
		Coolest_day_date="";
		for i in range(len(list)):

			file = open(list[i], "r");
			#Skip first two lines
			next(file)
			next(file)
			#read file line by line
			for line in file:
				currentline =line.split(",");
						
				#maximun temperature	
				if((len(currentline)>1)   and currentline[1]!='' and (int(currentline[1])>=maximunTemp)):
					maximunTemp=int(currentline[1])
					Hottet_day_date=currentline[0]
					
				#min temperature
				if(len(currentline)>1 and currentline[3]!='' and int(currentline[3])<minimunTemp):
					minimunTemp=int(currentline[3])
					Coolest_day_date=currentline[0]
					
				#minimum Humidity
				if(len(currentline)>1 and currentline[9]!='' and int(currentline[9])<minimumHumidity):
					minimumHumidity=int(currentline[9])
				
				#maximum Humidity
				if((len(currentline)>1)   and currentline[7]!='' and (int(currentline[7])>=maximumHumidity)):
					maximumHumidity=int(currentline[7])

		if reportNumber== 1 :			
			#Print the maximun temperature in specific format
			#print(str(year)+"             "+str(maximunTemp)+"               "+str(minimunTemp)+"               "+str(maximumHumidity)+"               "+str(minimumHumidity));
			print('{:4}'.format(year)+"             "+'{:5}'.format(maximunTemp)+"             "+'{:5}'.format(minimunTemp)+"            "+'{:5}'.format(maximumHumidity)+"            "+'{:5}'.format(minimumHumidity));			
			
		elif reportNumber== 2 :
			#print(str(year)+"             "+Hottet_day_date+"             "+str(maximunTemp))
			print('{:4}'.format(year)+"             "+'{:10}'.format(Hottet_day_date)+"             "+'{:5}'.format(maximunTemp))
			
		elif reportNumber== 3 :
			#print(str(year)+"             "+Coolest_day_date+"             "+str(minimunTemp))
			print('{:4}'.format(year)+"             "+'{:10}'.format(Coolest_day_date)+"             "+'{:5}'.format(minimunTemp))
			
		year=year+1;
		
	# Close opend file
	file.close();
		
	return;
		
	



def main(*argv):
	
	total=0;
	for i in argv:
			total=total+1
	
	if  (total!=2):
		
		print("No arguments have been passed")
		print("Usage: weatherman <report Number> <data_dir>")

		print("[Report Number]")
		print("1 for Annual Max/Min Temperature")
		print("2 for Hottest day of each year")
		print("3 for coldest day of each year")

		print("[data_dir]")
		print("Directory containing weather data files")
		sys.exit();
		
	elif(total==2):
		generateReport(argv[0],argv[1])
		
	return;
		
#main();		
main(1,"/home/rosheen/Assignemnts/weatherdata");
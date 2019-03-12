from sys import stdout

import sys

date = 0
max = 1
min = 3
humidity = 7 

maxTemp = -50
minTemp = 80
maxTempD = ''
minTempD = ''
maxHumidity = 0
maxHumidityD = ''


months = ['Jan', 'Feb' , 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def printBar(n, m, count):

	stdout.write(str(count))
	stdout.write('- ')
	for x in range(0, n):	
		stdout.write('+')
	stdout.write(str(n) + 'C' )

	print(' ')

	stdout.write(str(count))
	stdout.write('- ')

	for x in range(0, m):	
		stdout.write('+')	
	stdout.write(str(m) + 'C' )
	print(' ')	


def printBarInOneRow(n, m, count):

	stdout.write(str(count))
	stdout.write('- ')
	for x in range(0, n):
		if x < m :	
			stdout.write('+')
		else :
			stdout.write('*')
	stdout.write(str(m) + 'C - ' + str(n) + 'C' )

	print(' ')



def findMinMax(filename) :
	global maxTemp, minTemp, maxTempD, minTempD, maxHumidity, maxHumidityD 
	try :
		f = open(filename)


		line = f.readline()
		line = f.readline()

		s = line.split(',')

		if int(s[max]) > maxTemp :	
			maxTemp = int(s[max])
			maxTempD = s[date]
	
		if int(s[min]) < minTemp :

			minTemp = int(s[min])		
			minTempD = s[date]
		if int(s[humidity]) > maxHumidity :	
			
			maxHumidity = int(s[humidity])
			maxHumidityD = s[date]
	
		line = f.readline()

		while line :
		
			s = line.split(',')
			if s[max] :
				
				if int(s[max]) > maxTemp :	
					maxTemp = int(s[max])
					maxTempD = s[date]
				
			if s[min] :
				if int(s[min]) < minTemp :
					minTemp = int(s[min])		
					minTempD = s[date]
				
			if s[humidity] :
				if int(s[humidity]) > maxHumidity :	
					maxHumidity = int(s[humidity])
					maxHumidityD = s[date]
	
				
			line = f.readline()
	
		f.close()
	
	except :
		print('file ' + filename  + 'does not exist')


def minMaxAverage(filename) :
	minAvg = 0
	maxAvg = 0 
	humAvg = 0
	count=0
	try : 
		f = open(filename)


		line = f.readline()
		line = f.readline()
		s = line.split(',')


		maxAvg  = maxAvg +int(s[max])				
		minAvg  = minAvg + int(s[min])		
		humAvg = humAvg + int(s[humidity])
		count = count + 1
		
		line = f.readline()

		while line :
		
			s = line.split(',')
			
			if s[max] :
				maxAvg  = maxAvg +int(s[max])
			if s[min] :					
				minAvg  = minAvg + int(s[min])	
			if s[humidity] :		
				humAvg = humAvg + int(s[humidity])
				count = count + 1

			line = f.readline()
	
		f.close()
		print('Highest Average : ' +  str(maxAvg/count) + 'C' )
		print('Lowest Average : ' +  str(minAvg/count) + 'C' )
		print('Average Humidity : ' +  str(humAvg/count) + 'C' )


	except :
		print('file ' + filename  + 'does not exist')

def dailyReport(filename, option) :
	count = 1

	try : 
		f = open(filename)


		line = f.readline()
		line = f.readline()
		
		while line :
		
			s = line.split(',')
			
			if s[max] :
				if option == 3  :
					printBar(int(s[max]) , int(s[min]), count)
				elif option == 4 :
					printBarInOneRow(int(s[max]) , int(s[min]), count)
				count = count +1

			line = f.readline()
	
		f.close()

	except :
		print('file ' + filename  + 'does not exist')




#dailyReport('./weatherfiles/Murree_weather_2004_Aug.txt') 

if int(sys.argv[1]) == 1 :
	
	for s in months :
		s1 = './weatherfiles/Murree_weather_' +  str(sys.argv[2]) + '_' + s + '.txt'
		findMinMax(s1)
	print ('Maximum temperature details : ')
	print(maxTemp) 
	print(maxTempD)
	print ('Minimum temperature details : ')
	print ( minTemp ) 
	print (minTempD )
	print ('Humidity details : ')
	print (maxHumidity)
	print ( maxHumidityD)	

elif int(sys.argv[1]) == 2 :
	s1 = './weatherfiles/Murree_weather_' +  str(sys.argv[2]) + '_' + months[int(sys.argv[3])] + '.txt'
	minMaxAverage(s1)	

elif int(sys.argv[1]) == 3 :
	s1 = './weatherfiles/Murree_weather_' +  str(sys.argv[2]) + '_' + months[int(sys.argv[3])] + '.txt'
	dailyReport(s1, int(sys.argv[1]) )	

elif int(sys.argv[1]) == 4 :
	s1 = './weatherfiles/Murree_weather_' +  str(sys.argv[2]) + '_' + months[int(sys.argv[3])] + '.txt'
	dailyReport(s1, int(sys.argv[1]) )	


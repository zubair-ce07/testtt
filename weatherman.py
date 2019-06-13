""" This is the driver program for the weatherman task.


"""
import sys
from weatherHolder import weatherHolder

mypath = sys.argv[1]

# print(mypath)

instance = weatherHolder(mypath)
# retrievedData = instance.get_month_data("2009_Feb")
retrievedData = (instance.data['2009']['Jul'])
print(retrievedData)
if retrievedData:
    for day in retrievedData:
        print(day.weatherDataForTheDay)
else:
    print("There is no value for the given date available")
# print(instance.total_files())
# print(instance.data[])

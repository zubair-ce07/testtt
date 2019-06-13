""" This is the driver program for the weatherman task.


"""
import sys
from weatherHolder import weatherHolder

mypath = sys.argv[1]

# print(mypath)

instance = weatherHolder(mypath)
print(instance.get_month_data("2006_Jul")[2].weatherDataForTheDay)
print(instance.total_files())

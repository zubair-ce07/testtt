""" This is the driver program for the weatherman task.


"""
import sys
from weatherReader import weatherReader
from weatherReader import results
# from weatherReader import calculate

mypath = sys.argv[1]
option = sys.argv[2]
req = sys.argv[3]

instance = weatherReader(mypath, req)
print(instance.data[0].weatherDataForTheDay)
print(len(instance.data))

# ca = calculate(instance.data, option)

res = results()
res.addResult({'type': 'Highest', 'value': 321, 'day': '2014-3-2'})
res.addResult({'type': 'Average Humidity', 'value': 32, 'day': '2014-5-12'})
print(res.printResult())
# elif option == '-a'
 

# elif option == '-c'


# print(instance.data[0].weatherDataForTheDay)
# print(instance.data[1].weatherDataForTheDay)
# print(instance.data[2].weatherDataForTheDay)


""" This is the driver program for the weatherman task.


"""
import sys
from weatherReader import weatherReader
from weatherReader import results
from weatherReader import calculate

mypath = sys.argv[1]
option = sys.argv[2]
req = sys.argv[3]

instance = weatherReader(mypath, req)

if not len(instance.data):
    print("No values are available for the given time period!")
    exit()

calc = calculate()
resultt = calc.compute(instance.data, option, req)

if resultt:
    print(resultt.printResult())
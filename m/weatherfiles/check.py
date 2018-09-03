import csv
import os

for file in os.listdir('/home/tauseeq/Desktop/Repo/the-lab/m/weatherfiles'):
    if '.txt' in file:
        with open(file) as csvfile:
            a=csv.reader(csvfile)
            for row in a:
                print(row)

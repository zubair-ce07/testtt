import sys
import os
from itertools import islice
import populate_weather_readings as parser

def main():
    given_path=sys.argv[1]
    for i in islice(range(len(sys.argv)),2,None):
        if sys.argv[i] in ["-a","-c"]:
            i+=1
            given_date=sys.argv[i].split("/")
            given_year=given_date[0]
            given_month=int(given_date[1])
            weather_file_parser = parser.WeatherReadingsPopulator()
            weather_file_parser.list_files(given_path, sys.argv[i-1],
                                           given_year, given_month)
            weather_file_parser.populate_weather_readings(given_path)
            print(weather_file_parser.weather_readings)
            print ("*******************************\n")
        elif sys.argv[i] == "-e":
            i+=1
            given_year=sys.argv[i]
            weather_file_parser = parser.WeatherReadingsPopulator()
            weather_file_parser.list_files(given_path,
                                           sys.argv[i-1], given_year)
            weather_file_parser.populate_weather_readings(given_path)
            print(weather_file_parser.weather_readings)
            print ("*******************************\n")
    exit()

if __name__=="__main__":
    main()
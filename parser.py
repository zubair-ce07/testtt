import os
import sys
from readings import Reading

class Parser:

    def parse_files_for_yearwise_record(self, directory, year):
        """This function will parse files based on given year"""
        file_readings = []
        for file in os.listdir(directory):
            if (year in file):
                file_object = open(directory + "/" + file)
                file_object.readline()
                for line in file_object:
                    data = line.split(',')
                    reading = Reading(data[0], data[1], data[2],
                                        data[3], data[4], data[5],
                                        data[6], data[7], data[8],
                                        data[9], data[10], data[11],
                                        data[12], data[13], data[14],
                                        data[15], data[16], data[17],
                                        data[18], data[19], data[20],
                                        data[21], data[22])
                    file_readings.append(reading)
                file_object.close()
        return file_readings

    def parse_files_for_monthwise_records(self, directory, month):
        """This function will parse a file based on given month"""
        file_readings = []
        for file in os.listdir(directory):
            if (month in file):
                file_object = open(directory + "/" + file)
                file_object.readline()
                for line in file_object:
                    data = line.split(',')
                    reading = Reading(data[0], data[1], data[2],
                                        data[3], data[4], data[5],
                                        data[6], data[7], data[8],
                                        data[9], data[10], data[11],
                                        data[12], data[13], data[14],
                                        data[15], data[16], data[17],
                                        data[18], data[19], data[20],
                                        data[21], data[22])
                    file_readings.append(reading)
                file_object.close()
        return file_readings
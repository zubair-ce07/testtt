import os
import csv

class FileHandler:

    #This function will recieve list of data, header of file and file name to write
    @staticmethod
    def file_writer(file_name, fields_name, data_list):
        if not os.path.exists("WeatherFiles"):
            os.makedirs("WeatherFiles")
        with open(file_name, "w") as file:
            writer = csv.DictWriter(file , fieldnames=fields_name)
            writer.writeheader()
            writer.writerows(data_list)
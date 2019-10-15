import os
import csv


class Record_File:
    """
    This class will work to read a file from directory and hold records
    """

    
    def __init__(self):
        self.weather_records = []   
        
    def read_file(self):
        filenames = [f for f in os.listdir('.')
                    if os.path.isfile(os.path.join('.', f)) and f.endswith('.txt')]
        for entry in filenames:
            with open(entry, "r") as file_open:
                fileread = csv.reader(file_open)
                keys = fileread.__next__()
                for row in fileread:
                    self.weather_records.append(dict(zip(keys,row)))
                    
                file_open.close()
        return self.weather_records     

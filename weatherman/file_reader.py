import os.path
import csv

from weather_calc import get_max_value


month_lst = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class FileReader:
    def __init__(self, file_path, date = None):
        self.file_path = file_path
        self.date = date
        

    def get_record(self,header):
        file_name = self.file_path + "_" + month_lst[self.date] + ".txt"
        record = []

        try:
            with open(file_name, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    record.append(row[header])
                return record
        except:
            return False                
        
    def get_yearly_record(self,header,month):
        file_name = self.file_path + "_" + month + ".txt"
        temp_list = []

        try:
            with open(file_name, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    temp_list.append(row[header])
                return temp_list
        except:
            return False           
import glob
import csv
from weather_records import Weather_record

class file_reader:

    def read_files(self, basepath):
        all_content = []
        for f in glob.glob(f'{basepath}{"/"}{"*.txt"}'):
            for record in csv.DictReader(open(f)):
                if (record.get("PKST") or record.get("PKT")) and self.is_valid(record):                    
                    all_content.append(Weather_record(record))        
        return all_content

    def is_valid(self, record):
        if record.get("Max TemperatureC") and record.get("Min TemperatureC") and \
            record.get("Max Humidity") and record.get(" Mean Humidity"):
            return True
        else:
            False

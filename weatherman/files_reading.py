import glob
import csv
from weather_records import WeatherRecord

class FileReader:

    def read_files(self, basepath):
        all_content = []
        for f in glob.glob(f'{basepath}{"/"}{"*.txt"}'):
            for record in csv.DictReader(open(f)):
                if self.is_valid_record(record):                    
                    all_content.append(WeatherRecord(record))        
        return all_content

    def is_valid_record(self, record):
        return (record.get("PKST") or record.get("PKT")) and record.get("Max TemperatureC") and \
               record.get("Min TemperatureC") and record.get("Max Humidity") and record.get(" Mean Humidity")
                
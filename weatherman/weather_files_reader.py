import csv
import fnmatch
import os

from weather_record import WeatherRecord


class WeatherDataReader:
    
   
    @staticmethod
    def read_yearly_file_names(path, year):

        """ Returns list of file names for given year """

        file_names = []

        for file in os.listdir(path):
            if fnmatch.fnmatch(file, f'*_{year}_*'):
                file_names.append(path + '/' + file)

        return file_names

    @staticmethod
    def read_monthly_file_names(path, year, month):

        """ Returns file name for given month """

        files_names = []

        for file in os.listdir(path):
            if fnmatch.fnmatch(file, f'*_{year}_{month}.txt'):
                full_path = path + '/' + file
                files_names.append(full_path)

        return files_names

    def validate_record_value(self, weather_record):
        if weather_record != '':
            return weather_record  
   
    def required_data(self, record):
        weather_record = {
            'max_temp':record['Max TemperatureC']
        }
        return weather_record


    def read_files(self, files):

        """ Reads weather files and returns dictionary containing required weather records """

        max_temperature = []
        min_temperature = []
        max_humidity = []
        mean_humidity = []
        max_temp_date = []
        min_temp_date = []        
        max_humidity_date = []
        for file in files:
            with open(file) as weather_file:
                reader = csv.DictReader(weather_file)                
                for row in reader:
                    max_temperature.append(int(self.validate_record_value(int(row['Max TemperatureC']))))
                    max_temp_date.append(self.validate_record_value(row['PKT']))                
                    min_temperature.append(int(self.validate_record_value(int(row['Min TemperatureC']))))
                    min_temp_date.append(self.validate_record_value(row['PKT']))                
                    max_humidity.append(int(self.validate_record_value(int(row['Max Humidity']))))
                    max_humidity_date.append(self.validate_record_value(row['PKT']))                
                    mean_humidity.append(int(self.validate_record_value(int(row[' Mean Humidity']))))

        weather_record = WeatherRecord(max_temperature, min_temperature,
            max_humidity, mean_humidity,max_temp_date, min_temp_date, max_humidity_date)
        weather_record_dict = weather_record.__dict__   

        return weather_record_dict['weather_record']
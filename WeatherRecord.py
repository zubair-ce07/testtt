from Parser import parse_reading as psr
import glob
import csv


class WeatherRecord:
    def __init__(self):
        self.date = None
        self.min_temperature = None
        self.max_temperature = None
        self.mean_temperature = None
        self.max_humidity = None
        self.mean_humidity = None


class WeatherRegister:
    def __init__(self):
        self.__data = {}

    def read_dir(self, directory_path):
        for file_path in glob.glob(directory_path + 'Murree_weather_*_*.txt'):
            year_month = str.split(file_path, '_')
            if year_month[2] not in self.__data:
                self.__data[year_month[2]] = {}
            with open(file_path, newline='\n') as file:
                self.__data[year_month[2]][year_month[3][:3]] = []
                for row in csv.DictReader(file):
                    weather_record = WeatherRecord()
                    if "PKT" in row:
                        weather_record.date = psr(row["PKT"])
                    elif "PKST" in row:
                        weather_record.date = psr(row["PKST"])
                    weather_record.max_temperature = psr(row["Max TemperatureC"])
                    weather_record.min_temperature = psr(row["Min TemperatureC"])
                    weather_record.mean_temperature = psr(row["Mean TemperatureC"])
                    weather_record.max_humidity = psr(row["Max Humidity"])
                    weather_record.mean_humidity = psr(row[" Mean Humidity"])
                    self.__data[year_month[2]][year_month[3][:3]].append(weather_record)


wr = WeatherRegister()
wr.read_dir("weatherfiles/")
print(wr)

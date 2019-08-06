from read_file import ReadFile
from data import data


class YearReport(data):

    def generate_year_report(self, file_names):

        ReadFile.read_file(file_names, self.day_record, self.weather_data)

        print(max(self.day_record,key=lambda a: int(a["Max TemperatureC"]))["Max TemperatureC"])
        print(min(self.day_record,key=lambda a: int(a["Min TemperatureC"]))["Min TemperatureC"])
        print(max(self.day_record,key=lambda a: int(a["Max Humidity"]))["Max Humidity"])


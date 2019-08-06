from read_file import read_file
from data import data


class year_report(data):

    def generate_year_report(self, file_names):
        read_file.read_file(file_names,
                            self.day_record, self.weather_data)

        Max_TemperatureC = -999999
        Max_TemperatureC_day_record = None
        Min_TemperatureC = 999999
        Min_TemperatureC_day_record = None
        Max_Humidity = -99999
        Max_Humidity_day_record = None

        for data in self.day_record:
            if data["Max TemperatureC"] != '':
                if Max_TemperatureC < int(data["Max TemperatureC"]):
                    Max_TemperatureC = int(data["Max TemperatureC"])
                    Max_TemperatureC_day_record = data["PKT"]
            if data["Min TemperatureC"] != '':
                if Min_TemperatureC > int(data["Min TemperatureC"]):
                    Min_TemperatureC = int(data["Min TemperatureC"])
                    Min_TemperatureC_day_record = data["PKT"]
            if data["Max Humidity"] != '':
                if Max_Humidity < int(data["Max Humidity"]):
                    Max_Humidity = int(data["Max Humidity"])
                    Max_Humidity_day_record = data["PKT"]

        print(Max_TemperatureC, "C ", Max_TemperatureC_day_record)
        print(Min_TemperatureC, "C ", Min_TemperatureC_day_record)
        print(Max_Humidity, "% ", Max_Humidity_day_record)


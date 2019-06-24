import os
import WeatherReadings
import csv
import calendar


class WeatherDataExtractor:

    def __init__(self, year, month=0):
        self.all_data_objects = []
        self.month = month
        self.year = year

    def read_all_files(self):
        if self.month == None:
            for i in range(1, 13):
                local_month = calendar.month_name[i]
                try:
                    csv_file = csv.DictReader(open("weatherfiles/Murree_weather_"+self.year+"_"+local_month[:3]+".txt"))
                    for row in csv_file:
                        if row['PKT']:
                            reading = WeatherReadings.WeatherReadings(row)
                            self.all_data_objects.append(reading)
                except:
                    continue
        else:
            local_month = calendar.month_name[self.month]
            try:
                csv_file = csv.DictReader(open("weatherfiles/Murree_weather_" + self.year + "_" + local_month[:3] + ".txt"))
            except:
                raise ("Data not available")
            for row in csv_file:
                if row.has_key('PKT'):
                    reading = WeatherReadings.WeatherReadings(row)
                    self.all_data_objects.append(reading)
        return self.all_data_objects

from abc import ABC, abstractmethod
import os
import calendar

class WeatherData:
    """
    WeatherData holds all the necessary properties and methods for
    report generation
    """

    def __init__(self, pkt='',max_temp=0, mean_temp=0, min_temp=0,
                 max_humidity=0, mean_humidity=0, min_humidity=0):
        self.pkt = pkt
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.year = pkt[0:4]
        self.month_name = calendar.month_name[int(pkt[5:7].replace('-', ''))]
        self.day = pkt[7:].replace('-', '')


class WeatherRecordResult:

    def __init__(self, value, day):
        self.value = value
        self.day = day


class WeatherParser(ABC):

    @abstractmethod
    def parse(self):
        pass


class YearlyWeatherParser(WeatherParser):
    """
    YearlyWeatherParser
    """

    def __init__(self, path, year):
        self.path = path
        self.year = year
        self.weather_data = []

    def parse(self):
        file_names = os.listdir(path=self.path)

        for file_name in file_names:
            current_file_year = int(file_name.split('_')[2])
            if current_file_year == self.year:
                current_file_path = os.path.join(self.path, file_name)
                with open(current_file_path, mode='r') as file_data:
                    file_contents = file_data.read()
                    records = file_contents.split('\n')
                    records = records[1:-1]
                    for record in records:
                        record = record.split(',')
                        self.weather_data.append(WeatherData(
                            pkt=record[0],
                            max_temp=int(record[1]) if record[1] is not '' else None,
                            min_temp=int(record[3]) if record[3] is not '' else None,
                            max_humidity=int(record[7])  if record[7] is not '' else None
                        ))
        return self.weather_data


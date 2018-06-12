import os
import csv
from typing import List
from abc import ABC, abstractmethod

_months_full_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                      5: 'May', 6: 'June', 7: 'July', 8: 'August',
                      9: 'September', 10: 'October', 11: 'November',
                      12: 'December'}

_months_short_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
                       6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                       11: 'Nov', 12: 'Dec'}


def int_(number):
    return int(number) if number is not (None or "") else None


class WeatherReading:
    def __init__(self, date, max_temperature, mean_temperature,
                 min_temperature, max_humidity, mean_humidity, min_humidity):
        self.date = date
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.mean_humidity = mean_humidity
        self.max_humidity = max_humidity
        self.min_humidity = min_humidity


class ReportStrategy(ABC):
    @abstractmethod
    def print_report(self, given_results: dict):
        pass

    @abstractmethod
    def generate_results(self, weather_readings: List[WeatherReading]):
        pass

    @abstractmethod
    def list_files(self, date, files_path):
        pass


class AveragesReport(ReportStrategy):

    def print_report(self, given_results):
        print("\nHighest Average: ", end="")
        print(f"{given_results['AverageHighestTemperature']:.2f}C")
        print("Lowest Average: ", end="")
        print(f"{given_results['AverageLowestTemperature']:.2f}C")
        print("Average Mean Humidity: ", end="")
        print(f"{given_results['AverageMeanHumidity']:.2f}%")

    def generate_results(self, weather_readings: List[WeatherReading]):
        max_temps = list(filter(None, [reading.max_temperature for reading
                                  in weather_readings]))
        min_temps = list(filter(None, [reading.min_temperature for reading
                                  in weather_readings]))
        mean_humidity = list(filter(None, [reading.mean_humidity for reading
                                  in weather_readings]))
        return {
            "AverageHighestTemperature": sum(max_temps) / len(max_temps),
            "AverageLowestTemperature": sum(min_temps) / len(min_temps),
            "AverageMeanHumidity": sum(mean_humidity) / len(mean_humidity)
        }

    def list_files(self, date, files_path):
        try:
            year = date.split("/")[0]
            month = _months_short_names[int(date.split("/")[1])]
        except IndexError:
            print("Provide year and month in this format: yyyy/mm\n")
        except KeyError:
            print("Provide year and month in this format: yyyy/mm\n")
        return list(filter(lambda x: year in x and month in x,
                           os.listdir(files_path)))


class ExtremesReport(ReportStrategy):

    def print_report(self, given_results):
        date = given_results["HighestTemperature"][0].split("-")
        print(f"\nHighest: {given_results['HighestTemperature'][1]}"
              f"C on { _months_full_names[int(date[1])]}, {date[2]}")
        date = given_results["LowestTemperature"][0].split("-")
        print(f"Lowest: {given_results['LowestTemperature'][1]}"
              f"C on {_months_full_names[int(date[1])]}, {date[2]}")
        date = given_results["HighestHumidity"][0].split("-")
        print(f"Humidity: {given_results['HighestHumidity'][1]}"
              f"% on {_months_full_names[int(date[1])]}, {date[2]}")

    def generate_results(self, weather_readings: List[WeatherReading]):
        hottest = max(weather_readings, key=lambda x: x.max_temperature)
        coolest = min(weather_readings, key=lambda x: x.min_temperature)
        most_humid = max(weather_readings, key=lambda x: x.max_humidity)
        return {
            "HighestTemperature": (hottest.date, hottest.max_temperature),
            "LowestTemperature": (coolest.date, coolest.min_temperature),
            "HighestHumidity": (most_humid.date, most_humid.max_humidity)
        }

    def list_files(self, date, files_path):
        return list(filter(lambda x: date in x, os.listdir(files_path)))


class ChartsReport(ReportStrategy):

    def print_report(self, given_results):
        month_and_year = given_results["DataOfMonth/Year"]
        print(f"\n{_months_full_names[month_and_year[0]]}", end="")
        print(f", {month_and_year[1]}")
        for record in given_results["MonthsTemperatureRecord"]:
            print(f"\n{record[0]}", end=" ")
            if record[1] and record[1] > 0:
                print('\33[31m'+'+'*int(record[1]), end="")
            if record[2] and record[2] > 0:
                print('\33[34m'+'+'*int(record[2])+'\33[0m', end="")
            print(f"{record[1] if record[1] is not None else 'N/A'}C", end="")
            print(" - ", end="")
            print(f"{record[2] if record[2] is not None else 'N/A'}C", end="")

    def generate_results(self, weather_readings: List[WeatherReading]):
        return {"DataOfMonth/Year": [
            int(weather_readings[0].date.split("-")[1]),
            weather_readings[0].date.split("-")[0]
        ], "MonthsTemperatureRecord": [
            (reading.date.split("-")[2], reading.min_temperature,
             reading.max_temperature) for reading in weather_readings
        ]}

    def list_files(self, date, files_path):
        try:
            year = date.split("/")[0]
            month = _months_short_names[int(date.split("/")[1])]
        except IndexError:
            print("Provide year and month in this format: yyyy/mm\n")
        except KeyError:
            print("Provide year and month in this format: yyyy/mm\n")
        return list(filter(lambda x: year in x and month in x,
                           os.listdir(files_path)))


class WeatherReadingsPopulator:

    def __init__(self, strategy, files_path):
        self.strategy = strategy
        self.files_path = files_path
        self.weather_readings = []
        self.files = []

    def list_files(self, date: str):
        self.files.clear()
        self.files = self.strategy.list_files(self.strategy, date,
                                              self.files_path)
        if not self.files:
            raise FileNotFoundError("The record of "+date+" is not available")

    def populate_weather_readings(self):
        self.weather_readings.clear()
        for file in self.files:
            with open(self.files_path+"/"+file) as weather_file:
                reader = csv.DictReader(weather_file)
                date_field = 'PKT' if 'PKT' in reader.fieldnames else 'PKST'
                for record in reader:
                    self.weather_readings.append(WeatherReading(
                        record[date_field], int_(record['Max TemperatureC']),
                        int_(record['Mean TemperatureC']),
                        int_(record['Min TemperatureC']),
                        int_(record['Max Humidity']),
                        int_(record[' Mean Humidity']),
                        int_(record[' Min Humidity'])
                    ))


class ResultsGenerator:

    def __init__(self, strategy):
        self.generated_results = dict()
        self.strategy = strategy

    def generate_results(self, weather_readings: List[WeatherReading]):
        self.generated_results = \
            self.strategy.generate_results(self.strategy, weather_readings)


class ReportGenerator:

    def __init__(self, strategy, given_results: dict):
        self.given_results = given_results
        self.strategy = strategy

    def print_report(self):
        self.strategy.print_report(self.strategy, self.given_results)

import os
import csv
from itertools import islice
from typing import List
from abc import ABC, abstractmethod

_months_full_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                      5: 'May', 6: 'June', 7: 'July', 8: 'August',
                      9: 'September', 10: 'October', 11: 'November',
                      12: 'December'}

_months_short_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
                       6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                       11: 'Nov', 12: 'Dec'}


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


class ReportStrategyA(ReportStrategy):

    def print_report(self, given_results):
        print("\nHighest Average: ", end="")
        print(f"{given_results['AverageHighestTemperature']:.2f}C")
        print("Lowest Average: ", end="")
        print(f"{given_results['AverageLowestTemperature']:.2f}C")
        print("Average Mean Humidity: ", end="")
        print(f"{given_results['AverageMeanHumidity']:.2f}%")

    def generate_results(self, weather_readings: List[WeatherReading]):
        generated_results = dict()
        highest_temperature_sum = 0.0
        lowest_temperature_sum = 0.0
        mean_humidity_sum = 0.0
        no_of_highest_temperature_readings = 0
        no_of_lowest_temperature_readings = 0
        no_of_mean_humidity_readings = 0
        for reading in weather_readings:
            if reading.max_temperature:
                highest_temperature_sum += reading.max_temperature
                no_of_highest_temperature_readings += 1
            if reading.min_temperature:
                lowest_temperature_sum += reading.min_temperature
                no_of_lowest_temperature_readings += 1
            if reading.mean_humidity:
                mean_humidity_sum += reading.mean_humidity
                no_of_mean_humidity_readings += 1
        generated_results["AverageHighestTemperature"] \
            = highest_temperature_sum / no_of_highest_temperature_readings
        generated_results["AverageLowestTemperature"] \
            = lowest_temperature_sum / no_of_lowest_temperature_readings
        generated_results["AverageMeanHumidity"] \
            = mean_humidity_sum / no_of_mean_humidity_readings
        return generated_results

    def list_files(self, date, files_path):
        names_of_all_files = os.listdir(files_path)
        year = date.split("/")[0]
        month = _months_short_names[int(date.split("/")[1])]
        return list(filter(lambda x: year in x and month in x,
                           names_of_all_files))


class ReportStrategyE(ReportStrategy):

    def print_report(self, given_results):
        date = given_results["HighestTemperature"][0].split("-")
        print(f"\nHighest: {given_results['HighestTemperature'][1]}"
              f"C on { _months_full_names[int(date[1])]}, {date[2]}")
        date = given_results["LowestTemperature"][0].split("-")
        print(f"Lowest: {given_results['LowestTemperature'][1]}"
              f"C on {_months_full_names[int(date[1])]}, {date[2]}")
        date = given_results["HighestHumidity"][0].split("-")
        print(f"Humidity: {given_results['HighestHumidity'][1]}"
              f" on {_months_full_names[int(date[1])]}, {date[2]}")

    def generate_results(self, weather_readings: List[WeatherReading]):
        generated_results = dict()
        lowest_temperature = 100
        lowest_temperature_day = ""
        highest_humidity = 0
        highest_humidity_day = ""
        highest_temperature = -100
        highest_temperature_day = ""
        for reading in weather_readings:
            if (reading.max_temperature
                    and reading.max_temperature >= highest_temperature):
                highest_temperature = reading.max_temperature
                highest_temperature_day = reading.date
            if (reading.max_humidity
                    and reading.max_humidity >= highest_humidity):
                highest_humidity = reading.max_humidity
                highest_humidity_day = reading.date
            if (reading.min_temperature
                    and reading.min_temperature <= lowest_temperature):
                lowest_temperature = reading.min_temperature
                lowest_temperature_day = reading.date
        generated_results["HighestTemperature"] \
            = (highest_temperature_day, highest_temperature)
        generated_results["LowestTemperature"] \
            = (lowest_temperature_day, lowest_temperature)
        generated_results["HighestHumidity"] \
            = (highest_humidity_day, highest_humidity)
        return generated_results

    def list_files(self, date, files_path):
        names_of_all_files = os.listdir(files_path)
        return list(filter(lambda x: date in x, names_of_all_files))


class ReportStrategyC(ReportStrategy):

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
        generated_results = dict()
        generated_results["DataOfMonth/Year"] = [
            int(weather_readings[0].date.split("-")[1]),
            weather_readings[0].date.split("-")[0]
        ]
        generated_results["MonthsTemperatureRecord"] = [
            (reading.date.split("-")[2], reading.min_temperature,
             reading.max_temperature) for reading in weather_readings
        ]
        return generated_results

    def list_files(self, date, files_path):
        names_of_all_files = os.listdir(files_path)
        year = date.split("/")[0]
        month = _months_short_names[int(date.split("/")[1])]
        return list(filter(lambda x: year in x and month in x,
                           names_of_all_files))


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

    def populate_weather_readings(self):
        self.weather_readings.clear()
        for file in self.files:
            with open(self.files_path+"/"+file) as weather_file:
                reader = csv.DictReader(weather_file)
                for row in islice(reader, 1, None):
                    weather_reading = WeatherReading(
                        row['PKT'],
                        int(row['Max TemperatureC'])
                        if row['Max TemperatureC'] else None,
                        int(row['Mean TemperatureC'])
                        if row['Mean TemperatureC'] else None,
                        int(row['Min TemperatureC'])
                        if row['Min TemperatureC'] else None,
                        int(row['Max Humidity'])
                        if row['Max Humidity'] else None,
                        int(row[' Mean Humidity'])
                        if row[' Mean Humidity'] else None,
                        int(row[' Min Humidity'])
                        if row[' Min Humidity'] else None
                    )
                    self.weather_readings.append(weather_reading)


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
        super().__init__()

    def print_report(self):
        self.strategy.print_report(self.strategy, self.given_results)

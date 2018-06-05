from weather_reading_data_structure import WeatherReading,List


class ResultsGenerator:

    def __init__(self):
        self.generated_results = dict()

    def generate_results(
            self,
            result_type: str,
            weather_readings: List[WeatherReading]):
        self.generated_results.clear()
        if result_type == "-e":
            lowest_temperature = 100
            lowest_temperature_day = ""
            highest_humidity = 0
            highest_humidity_day = ""
            highest_temperature = -100
            highest_temperature_day = ""
            for reading in weather_readings:
                if (reading.max_temperature is not None
                        and reading.max_temperature >= highest_temperature):
                    highest_temperature = reading.max_temperature
                    highest_temperature_day = reading.date
                if (reading.max_humidity is not None
                        and reading.max_humidity >= highest_humidity):
                    highest_humidity = reading.max_humidity
                    highest_humidity_day = reading.date
                if (reading.min_temperature is not None
                        and reading.min_temperature <= lowest_temperature):
                    lowest_temperature = reading.min_temperature
                    lowest_temperature_day = reading.date
            self.generated_results["HighestTemperature"] \
                = (highest_temperature_day, highest_temperature)
            self.generated_results["LowestTemperature"] \
                = (lowest_temperature_day, lowest_temperature)
            self.generated_results["HighestHumidity"] \
                = (highest_humidity_day, highest_humidity)
        elif result_type == "-a":
            highest_temperature_sum = 0.0
            lowest_temperature_sum = 0.0
            mean_humidity_sum = 0.0
            no_of_highest_temperature_readings = 0
            no_of_lowest_temperature_readings = 0
            no_of_mean_humidity_readings = 0
            for reading in weather_readings:
                if reading.max_temperature is not None:
                    highest_temperature_sum += reading.max_temperature
                    no_of_highest_temperature_readings += 1
                if reading.min_temperature is not None:
                    lowest_temperature_sum += reading.min_temperature
                    no_of_lowest_temperature_readings += 1
                if reading.mean_humidity is not None:
                    mean_humidity_sum += reading.mean_humidity
                    no_of_mean_humidity_readings += 1
            self.generated_results["AverageHighestTemperature"] \
                = highest_temperature_sum / no_of_highest_temperature_readings
            self.generated_results["AverageLowestTemperature"] \
                = lowest_temperature_sum / no_of_lowest_temperature_readings
            self.generated_results["AverageMeanHumidity"] \
                = mean_humidity_sum / no_of_mean_humidity_readings
        elif result_type == "-c":
            self.generated_results["MonthsTemperatureRecord"] = []
            self.generated_results["DataOfMonth/Year"] = [
                int(weather_readings[0].date.split("-")[1]),
                weather_readings[0].date.split("-")[0]
            ]
            for reading in weather_readings:
                self.generated_results["MonthsTemperatureRecord"].append(
                    (reading.date.split("-")[2],
                     reading.min_temperature,
                     reading.max_temperature)
                )

class ResultsGenerator:

    def __init__(self):
        self.generated_results = dict()

    def generate_results(self, weather_readings, result_type):
        if result_type == "-e":
            lowest_temperature = 50
            lowest_temperature_day = ""
            highest_humidity = 0
            highest_humidity_day = ""
            highest_temperature = 0
            highest_temperature_day = ""
            for i in range(len(weather_readings)):
                if (weather_readings[i][1][0] is not None
                        and weather_readings[i][1][0] >= highest_temperature):
                    highest_temperature = weather_readings[i][1][0]
                    highest_temperature_day = weather_readings[i][0]
                if (weather_readings[i][2][0] is not None
                        and weather_readings[i][2][0] >= highest_humidity):
                    highest_humidity = weather_readings[i][2][0]
                    highest_humidity_day = weather_readings[i][0]
                if (weather_readings[i][1][2] is not None
                        and weather_readings[i][1][2] <= lowest_temperature):
                    lowest_temperature = weather_readings[i][1][2]
                    lowest_temperature_day = weather_readings[i][0]
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
            no_of_highest_temperature_readings=0
            no_of_lowest_temperature_readings=0
            no_of_mean_humidity_readings=0
            for i in range(len(weather_readings)):
                if weather_readings[i][1][0] is not None:
                    highest_temperature_sum += weather_readings[i][1][0]
                    no_of_highest_temperature_readings += 1
                if weather_readings[i][1][2] is not None:
                    lowest_temperature_sum += weather_readings[i][1][2]
                    no_of_lowest_temperature_readings += 1
                if weather_readings[i][2][1] is not None:
                    mean_humidity_sum += weather_readings[i][2][1]
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
                weather_readings[0][0].split("-")[1],
                weather_readings[0][0].split("-")[0]
            ]
            for i in range(len(weather_readings)):
                highest_temperature = weather_readings[i][1][0]
                lowest_temperature = weather_readings[i][1][2]
                date = weather_readings[i][0]
                self.generated_results["MonthsTemperatureRecord"].append(
                    (date.split("-")[2], lowest_temperature,
                     highest_temperature)
                )








from read_file import ReadFile
from data import data
import statistics


class MonthReport(data):

    def generate_month_report(self, file_names):

        ReadFile.read_file(file_names, self.day_record, self.weather_data)

        average_highest_temperature = []
        average_lowest_temperature = []
        average_mean_humidity = []

        for data in self.day_record:
            average_highest_temperature.append(int(data["Max TemperatureC"]))
            average_lowest_temperature.append(int(data["Min TemperatureC"]))
            average_mean_humidity.append(int(data["Mean Humidity"]))


        print(f"Average high temprature :{statistics.mean(average_highest_temperature)}")
        print(f"Average Low temprature :{statistics.mean(average_lowest_temperature)}")
        print(f"Average Mean humidity :{statistics.mean(average_mean_humidity)}")


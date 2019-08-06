from read_file import read_file
from data import data
import statistics


class month_report(data):

    def generate_month_report(self, file_names):
        read_file.read_file(file_names,
                            self.day_record, self.weather_data)

        average_highest_temperature = []
        average_lowest_temperature = []
        average_mean_humidity = []

        for data in self.day_record:
            if data["Max TemperatureC"] != '':
                average_highest_temperature.append(
                    int(data["Max TemperatureC"]))
            if data["Min TemperatureC"] != '':
                average_lowest_temperature.append(
                    int(data["Min TemperatureC"]))
            if data["Mean Humidity"] != '':
                average_mean_humidity.append(int(data["Mean Humidity"]))

        print("Average high temprature :{temp}".format(
            temp=statistics.mean(average_highest_temperature)))
        print("Average Low temprature :{temp}".format(
            temp=statistics.mean(average_lowest_temperature)))
        print("Average Mean humidity :{temp}".format(
            temp=statistics.mean(average_mean_humidity)))


import datetime
from readings import Reading

class Calculations:
    
    def calulate_year_wise_record(self, weather_readings):
        highest_temp_record = weather_readings[0]
        lowest_temp_record = weather_readings[0]
        max_humidity_record = weather_readings[0]

        for reading in weather_readings:
            if (reading.max_temprature is not ''
                    and reading.max_temprature > highest_temp_record.max_temprature):
                highest_temp_record = reading
            if (reading.min_temprature is not ''
                    and reading.min_temprature < lowest_temp_record.min_temprature):
                lowest_temp_record = reading
            if (reading.max_humidity is not ''
                    and reading.max_humidity > max_humidity_record.max_humidity):
                max_humidity_record = reading

        result = {"Highest:":str(highest_temp_record.max_temprature) + "C on "
                    + datetime.datetime.strptime(highest_temp_record.day, "%Y-%m-%d").strftime("%B %d"),
                    "Lowest:":str(lowest_temp_record.min_temprature) + "C on "
                    + datetime.datetime.strptime(lowest_temp_record.day, "%Y-%m-%d").strftime("%B %d"),
                    "Most Humid:":str(max_humidity_record.max_humidity) + "% on "
                    + datetime.datetime.strptime(max_humidity_record.day, "%Y-%m-%d").strftime("%B %d")}
        return result

    def calulate_average_record(self, weather_readings):
        sum_highest_temprature = 0
        count_highest_temprature = 0
        sum_lowest_temprature = 0
        count_lowest_temprature = 0
        sum_mean_humidity = 0
        count_mean_humidity = 0

        for reading in weather_readings:
            if (reading.max_temprature is not ''):
                sum_highest_temprature += reading.max_temprature
                count_highest_temprature += 1

            if (reading.min_temprature is not ''):
                sum_lowest_temprature += reading.min_temprature
                count_lowest_temprature += 1

            if (reading.mean_humidity is not ''):
                sum_mean_humidity += reading.mean_humidity
                count_mean_humidity += 1

        results = {"Highest Average:":str(sum_highest_temprature / count_highest_temprature) + "C",
                    "Lowest Average:":str(sum_lowest_temprature / count_lowest_temprature) + "C",
                    "Average Mean Humidity:":str(sum_mean_humidity / count_mean_humidity) + "%"}

        return results
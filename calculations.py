import datetime

class Calculations:

    def calculate_average(column_to_be_averaged, weather_readings):
        sum = 0
        count = 0
        for reading in weather_readings:
            if reading[column_to_be_averaged]:
                sum += int(reading[column_to_be_averaged])
                count += 1
        return sum / count
    
    def calulate_year_wise_record(self, weather_readings):

        highest_temp_record = max(weather_readings, key=lambda x:x["Max TemperatureC"])
        lowest_temp_record = min(weather_readings, key=lambda x:x["Min TemperatureC"])
        max_humidity_record = max(weather_readings, key=lambda x:x["Max Humidity"])

        results = {"Highest Temprature":highest_temp_record,
                    "Lowest Temprature":lowest_temp_record,
                    "Max Humidity":max_humidity_record}
       
        return results

    def calulate_average_record(self, weather_readings):
        Calculations.calculate_average
        results = {"Highest Average":Calculations.calculate_average("Max TemperatureC", weather_readings),
                    "Lowest Average":Calculations.calculate_average("Min TemperatureC", weather_readings),
                    "Average Mean Humidity":Calculations.calculate_average(" Mean Humidity", weather_readings)}

        return results
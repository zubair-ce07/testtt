import datetime

class Calculations:

    @staticmethod
    def calculate_max (column_name, weather_readings):
        return max(weather_readings, key=lambda x:x[column_name])


    @staticmethod
    def calculate_min (column_name, weather_readings):
        return min(weather_readings, key=lambda x:x[column_name])

    @staticmethod
    def calculate_average(column_name, weather_readings):
        sum_column = sum(int(reading[column_name]) for reading in weather_readings if reading[column_name])
        len_column = len([int(reading[column_name]) for reading in weather_readings if reading[column_name]])

        return sum_column / len_column

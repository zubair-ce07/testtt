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
        data_list = []
        for reading in weather_readings:
            if reading[column_name]:
                data_list.append(int(reading[column_name])) 
        sum_column = sum(data_list)
        len_column = len(data_list)

        return sum_column / len_column

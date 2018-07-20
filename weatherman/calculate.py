import sys


class Calculate():
    """class for computing the calculations given the readings data structure"""
    def __init__(self, readings):
        self.readings = readings
        self.parameters = ['PKT', 'Max TemperatureC', 'Mean TemperatureC',
                          'Min TemperatureC', 'Dew PointC', 'MeanDew PointC',
                          'Min DewpointC', 'Max Humidity', 'Mean Humidity',
                          'Min Humidity', 'Max Sea Level PressurehPa', 'Mean Sea Level PressurehPa',
                          'Min Sea Level PressurehPa', 'Max VisibilityKm', 'Mean VisibilityKm',
                          'Min VisibilitykM', 'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h',
                          'Max Gust SpeedKm/h', 'PrecipitationCm', 'CloudCover',
                          'Events', 'WindDirDegrees']
        self.index_max_temp = self.parameters.index('Max TemperatureC')
        self.index_min_temp = self.parameters.index('Min TemperatureC')
        self.index_max_humidity = self.parameters.index('Max Humidity')
        self.index_mean_humidity = self.parameters.index('Mean Humidity')

    def year_calculation(self):
        max_temp = {'Month': None, 'Day': None, 'Value': 0}
        min_temp = {'Month': None, 'Day': None, 'Value': sys.maxsize}
        max_humidity = {'Month': None, 'Day': None, 'Value': 0}
        for month, month_entry in self.readings.items():
            for day_entry in month_entry:
                high_temp = day_entry[self.index_max_temp]
                if high_temp and high_temp > max_temp['Value']:
                    max_temp['Value'] = high_temp
                    max_temp['Month'] = month
                    max_temp['Day'] = month_entry.index(day_entry) + 1
                low_temp = day_entry[self.index_min_temp]
                if low_temp and low_temp < min_temp['Value']:
                    min_temp['Value'] = low_temp
                    min_temp['Month'] = month
                    min_temp['Day'] = month_entry.index(day_entry) + 1
                high_humid = day_entry[self.index_max_humidity]
                if high_humid and high_temp > max_humidity['Value']:
                    max_humidity['Value'] = high_humid
                    max_humidity['Month'] = month
                    max_humidity['Day'] = month_entry.index(day_entry) + 1
        return max_temp, min_temp, max_humidity

    def month_calculation(self):
        avg_highest_temp, avg_lowest_temp, avg_mean_humidity = 0, 0, 0
        for month_entry in self.readings.values():
            for day_entry in month_entry:
                high_temp = day_entry[self.index_max_temp]
                low_temp = day_entry[self.index_min_temp]
                humidity = day_entry[self.index_mean_humidity]
                if high_temp:  # Check if high temperature was recorded for this day entry
                    avg_highest_temp += high_temp
                if low_temp:
                    avg_lowest_temp += low_temp
                if humidity:
                    avg_mean_humidity += humidity
            days = len(month_entry)
            avg_highest_temp /= days
            avg_lowest_temp /= days
            avg_mean_humidity /= days
        return avg_highest_temp, avg_lowest_temp, avg_mean_humidity

    def day_calculation(self):
        max_temp, min_temp = [], []
        for month_entry in self.readings.values():
            for day_entry in month_entry:
                max_temp.append(day_entry[self.index_max_temp])
                min_temp.append(day_entry[self.index_min_temp])
        return max_temp, min_temp


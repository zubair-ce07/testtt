from task2.result import Result
import numpy


class Calculation:
    """ Calculating average of min, mean and max temperatures in a given time period """
    @staticmethod
    def calculate_report(month, year, weathers):
        result = Result(month, year)
        if month == '':
            filtered = [weather for weather in weathers if weather.year == year]
        else:
            filtered = [weather for weather in weathers if weather.month == month and weather.year == year]

        if filtered:
            result.set_report(
                numpy.mean([float(reading.min_temperature_c) if reading.min_temperature_c else 0 for weather in filtered for reading in weather.readings]),
                numpy.mean([float(reading.mean_temperature_c) if reading.mean_temperature_c else 0 for weather in filtered for reading in weather.readings]),
                numpy.mean([float(reading.max_temperature_c) if reading.max_temperature_c else 0 for weather in filtered for reading in weather.readings])
            )
        return result

from task2.result import Result
import numpy


class Calculation:

    def __calculate_report_whole_year(year, weathers):
        result = Result(0, year)
        filterd = [weather for weather in weathers if weather.year == year]
        if filterd:
            result.set_report(
                numpy.mean([float(reading.min_temperature_c) if reading.min_temperature_c else 0 for weather in filterd for reading in weather.readings]),
                numpy.mean([float(reading.mean_temperature_c) if reading.mean_temperature_c else 0 for weather in filterd for reading in weather.readings]),
                numpy.mean([float(reading.max_temperature_c) if reading.max_temperature_c else 0 for weather in filterd for reading in weather.readings])
            )
        return result

    @staticmethod
    def calculate_report(month, year, weathers):
        if month == '':
            return Calculation.__calculate_report_whole_year(year, weathers)
        result = Result(month, year)
        filterd = [weather for weather in weathers if weather.month == month and weather.year == year]
        if filterd:
            result.set_report(
                numpy.mean([float(reading.min_temperature_c) if reading.min_temperature_c else 0 for reading in filterd[0].readings]),
                numpy.mean([float(reading.mean_temperature_c) if reading.mean_temperature_c else 0 for reading in filterd[0].readings]),
                numpy.mean([float(reading.max_temperature_c) if reading.max_temperature_c else 0 for reading in filterd[0].readings])
            )
        return result

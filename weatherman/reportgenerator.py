"""
Module contains all the necessary classes and data-structures
for the generation of reports
"""

from abc import ABC, abstractmethod
from operator import attrgetter

from colorprint import ColorPrint


class ReportGenerator(ABC):
    """
    Contract for all the classes that want to generate reports of
    weatherman dataset
    """

    @abstractmethod
    def generate(self, weather_data):
        """
        Abstract method for the inheriting class to implement that will
        be responsible for generating and printing report

        Arguments:
            weather_data (list): List of WeatherData type
        """
        raise NotImplementedError()


class HighLowReportGenerator(ReportGenerator):
    """
    Generates a report for Highest temperature, Lowest Temperature and
    Highest Humidity from the given weather data

    This is the first type of report. Generated from the -e flag
    """

    def generate(self, weather_data):

        # the dataset contains many None parameters, so it is a good time
        # to remove all the Nones
        max_temp_records = [data for data in weather_data if data.max_temp is not None]
        min_temp_records = [data for data in weather_data if data.min_temp is not None]
        max_humidity_records = [data for data in weather_data if data.max_humidity is not None]

        # gets a single record
        # first argument to the max/min function is an iterable and the
        # attrgetter will return a callable object from which the provided
        # attribute can be accessed
        max_temp_record = max(max_temp_records, key=attrgetter('max_temp'))
        max_humidity_record = max(max_humidity_records, key=attrgetter('max_humidity'))
        min_temp_record = min(min_temp_records, key=attrgetter('min_temp'))

        # to store the result
        final_report = HighLowReport(max_temp_record, max_humidity_record, min_temp_record)

        format_str = 'Highest: {}C on {} {}\nLowest: {}C on {} {}\nHumidity: {}% on {} {}'
        print(format_str.format(max_temp_record.max_temp,
                                max_temp_record.month_name,
                                max_temp_record.day,
                                min_temp_record.min_temp,
                                min_temp_record.month_name,
                                min_temp_record.day,
                                max_humidity_record.max_humidity,
                                max_humidity_record.month_name,
                                max_humidity_record.day,
                                ))


class AverageTemperatureReportGenerator(ReportGenerator):
    """
    Generates a report for Average Highest temperature, Average Lowest
    Temperature and Average Mean Humidity from the given weather data

    This is the second type of report. It is generated using the -a flag
    from command-line
    """

    def _mean(self, arr):
        return int(sum(arr) / len(arr))

    def generate(self, weather_data):

        # removing nones by a pythonic way
        max_temps = [data.max_temp for data in weather_data if data.max_temp is not None]
        min_temps = [data.min_temp for data in weather_data if data.min_temp is not None]
        mean_humidities = [data.mean_humidity for data in weather_data if data.mean_humidity is not None]

        # mean calculations
        avg_max_temp = self._mean(max_temps)
        avg_min_temp = self._mean(min_temps)
        avg_mean_humidity = self._mean(mean_humidities)

        final_result = AverageTemperatureReport(avg_max_temp, avg_mean_humidity, avg_min_temp)

        format_str = 'Highest Average: {}C\nLowest Average: {}C\n' \
                     'Average Mean Humidity: {}%'
        print(format_str.format(avg_max_temp, avg_min_temp, avg_mean_humidity))


class HighLowTemperatureSingleGraphReportGenerator(ReportGenerator):
    """
    Generates a report for Highest temperature, Lowest Temperature in
    the form of a single graph from the given weather data

    This is the last(BONUS) type of report. It is generated using the -b flag
    from command-line
    """

    def generate(self, weather_data):
        print('{} {}'.format(weather_data[0].month_name, weather_data[0].year))

        # data needs to be sorted in increasing order based on day
        sorted_weather_records = sorted(weather_data, key=lambda x: x.day)

        for record in sorted_weather_records:

            color_input_max_temp = '+' * record.max_temp if record.max_temp is not None else ' '
            color_input_min_temp = '+' * record.min_temp if record.min_temp is not None else ' '

            print('{} {}{} {}C - {}C'.format(record.day,
                                             ColorPrint.blue_raw(color_input_min_temp),
                                             ColorPrint.red_raw(color_input_max_temp),
                                             record.min_temp, record.max_temp))


class HighLowTemperatureGraphReportGenerator(ReportGenerator):
    """
    Generates a report for Highest temperature, Lowest Temperature in
    the form of a two-lined graph from the given weather data

    This is the third type of report. It is generated using the -c flag
    from command-line
    """

    def generate(self, weather_data):

        print('{} {}'.format(weather_data[0].month_name, weather_data[0].year))

        # data needs to be sorted in increasing order based on day
        sorted_weather_records = sorted(weather_data, key=lambda x: x.day)

        for record in sorted_weather_records:

            # '+' to be colored as red
            color_print_input = '+' * record.max_temp if record.max_temp is not None else 'Data NA'
            print('{} {} {}C'.format(record.day,
                                     ColorPrint.red_raw(color_print_input),
                                     record.max_temp))

            # '+' to be colored as blue
            color_print_input = '+' * record.min_temp if record.min_temp is not None else 'Data NA'
            print('{} {} {}C'.format(record.day,
                                     ColorPrint.blue_raw(color_print_input),
                                     record.min_temp))


class HighLowReport:
    """
    Data-structure for holding the output of HighLowReportGenerator
    """

    def __init__(self, max_temp_record, max_humidity_record, min_temp_record):
        self.max_temp_record = max_temp_record
        self.max_humidity_record = max_humidity_record
        self.min_temp_record = min_temp_record


class AverageTemperatureReport:
    """
    Data-structure for holding the output of AverageTemperatureReportGenerator
    """

    def __init__(self, avg_max_temp, avg_mean_humidity, avg_min_temp):
        self.avg_max_temp = avg_max_temp
        self.avg_mean_humidity = avg_mean_humidity
        self.avg_min_temp = avg_min_temp

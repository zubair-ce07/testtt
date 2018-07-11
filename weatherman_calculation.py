from operator import attrgetter
from weatherman_ds import WeatherResult


class WeatherReport:

    @staticmethod
    def calculate_extreme_for_year(weather_records):
        mean_records = WeatherReport.filter_by_attribute(weather_records, 'mean_temperature')
        humidity_records = WeatherReport.filter_by_attribute(weather_records, 'mean_humidity')

        minimum_reading = min(mean_records, key=attrgetter('mean_temperature'))
        maximum_reading = max(mean_records, key=attrgetter('mean_temperature'))
        humidity_reading = max(humidity_records, key=attrgetter('mean_humidity'))

        return WeatherResult(minimum_reading.pkt, minimum_reading.mean_temperature,
                             maximum_reading.pkt, maximum_reading.mean_temperature,
                             humidity_reading.pkt, humidity_reading.mean_humidity)

    @staticmethod
    def calculate_average_for_month(weather_records):
        high_records = WeatherReport.filter_by_attribute(weather_records, 'max_temperature')
        low_records = WeatherReport.filter_by_attribute(weather_records, 'min_temperature')
        humidity_records = WeatherReport.filter_by_attribute(weather_records, 'mean_humidity')
        avg_high = sum(reading.max_temperature for reading in high_records) // len(high_records)
        avg_low = sum(reading.min_temperature for reading in low_records) // len(low_records)
        avg_humid = sum(reading.mean_humidity for reading in humidity_records) // len(humidity_records)

        return WeatherResult('', avg_low, '', avg_high, '', avg_humid)

    @staticmethod
    def filter_by_attribute(weather_records, attribute):
        return list(filter(attrgetter(attribute), weather_records))

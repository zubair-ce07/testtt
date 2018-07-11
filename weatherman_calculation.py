from operator import attrgetter
from weatherman_ds import ReportResult


class WeatherReport:

    @staticmethod
    def year_extreme_calculate(weather_records):
        mean_records = list(filter(lambda reading: reading.mean_temperature, weather_records))
        humidity_records = list(filter(lambda reading: reading.mean_humidity, weather_records))

        minimum_reading = min(mean_records, key=attrgetter('mean_temperature'))
        maximum_reading = max(mean_records, key=attrgetter('mean_temperature'))
        humidity_reading = max(humidity_records, key=attrgetter('mean_humidity'))

        return ReportResult(minimum_reading.pkt, minimum_reading.mean_temperature,
                            maximum_reading.pkt, maximum_reading.mean_temperature,
                            humidity_reading.pkt, humidity_reading.mean_humidity)

    @staticmethod
    def month_average_calculate(weather_records):
        high_records = list(filter(lambda reading: reading.max_temperature, weather_records))
        low_records = list(filter(lambda reading: reading.min_temperature, weather_records))
        humidity_records = list(filter(lambda reading: reading.mean_humidity, weather_records))

        avg_high = sum(reading.max_temperature for reading in high_records) // len(high_records)
        avg_low = sum(reading.min_temperature for reading in low_records) // len(low_records)
        avg_humid = sum(reading.mean_humidity for reading in humidity_records) // len(humidity_records)

        return ReportResult('', avg_low, '', avg_high, '', avg_humid)

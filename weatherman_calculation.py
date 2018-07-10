from operator import attrgetter
from weatherman_ds import ReportResult


class WeatherReport:

    @staticmethod
    def yearly_results(readings):
        mean_temp_filtered = list(filter(lambda reading: reading.mean_temperature, readings))
        humidity_filtered = list(filter(lambda reading: reading.mean_humidity, readings))

        minimum_reading = min(mean_temp_filtered, key=attrgetter('mean_temperature'))
        maximum_reading = max(mean_temp_filtered, key=attrgetter('mean_temperature'))
        humidity_reading = max(humidity_filtered, key=attrgetter('mean_humidity'))

        return ReportResult(minimum_reading.pkt, minimum_reading.mean_temperature,
                            maximum_reading.pkt, maximum_reading.mean_temperature,
                            humidity_reading.pkt, humidity_reading.mean_humidity)

    @staticmethod
    def monthly_results(readings):
        high_temp_filtered = list(filter(lambda reading: reading.max_temperature, readings))
        low_temp_filtered = list(filter(lambda reading: reading.min_temperature, readings))
        mean_humidity_filtered = list(filter(lambda reading: reading.mean_humidity, readings))

        avg_high = sum(reading.max_temperature for reading in high_temp_filtered) // len(high_temp_filtered)
        avg_low = sum(reading.min_temperature for reading in low_temp_filtered) // len(low_temp_filtered)
        avg_humid = sum(reading.mean_humidity for reading in mean_humidity_filtered) // len(mean_humidity_filtered)

        return ReportResult('', avg_low, '', avg_high, '', avg_humid)

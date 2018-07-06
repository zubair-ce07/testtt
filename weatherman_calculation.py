from operator import attrgetter
from weatherman_ds import ReportResult


class WeatherReport:

    @staticmethod
    def yearly_results(readings):
        humidity_filtered = []
        mean_temp_filtered = []
        for reading in readings:
            if reading.mean_temperature:
                mean_temp_filtered.append(reading)
            if reading.mean_humidity:
                humidity_filtered.append(reading)
        minimum_reading = min(mean_temp_filtered, key=attrgetter('mean_temperature'))
        maximum_reading = max(mean_temp_filtered, key=attrgetter('mean_temperature'))
        humidity_reading = max(humidity_filtered, key=attrgetter('mean_humidity'))

        return ReportResult(minimum_reading.pkt, minimum_reading.mean_temperature,
                            maximum_reading.pkt, maximum_reading.mean_temperature,
                            humidity_reading.pkt, humidity_reading.mean_humidity)

    @staticmethod
    def monthly_results(readings):
        high_temp_filtered = []
        low_temp_filtered = []
        mean_humidity_filtered = []
        for reading in readings:
            if reading.min_temperature:
                low_temp_filtered.append(reading)
            if reading.mean_humidity:
                mean_humidity_filtered.append(reading)
            if reading.max_temperature:
                high_temp_filtered.append(reading)
        sum_high = 0
        for reading in high_temp_filtered:
            sum_high = sum_high + reading.max_temperature

        sum_low = 0
        for reading in low_temp_filtered:
            sum_low = sum_low + reading.min_temperature

        sum_humidity = 0
        for reading in mean_humidity_filtered:
            sum_humidity = sum_humidity + reading.mean_humidity

        return ReportResult('', sum_low//len(low_temp_filtered),
                            '', sum_high//len(high_temp_filtered),
                            '', sum_humidity//len(mean_humidity_filtered))


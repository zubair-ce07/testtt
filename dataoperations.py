import calendar
from dateutil import parser


class DataOperations:
    __PKT = 'PKT'
    __MAX_TEMPERATURE = 'Max TemperatureC'
    __MIN_TEMPERATURE = 'Min TemperatureC'
    __MAX_HUMIDITY = 'Max Humidity'
    __MEAN_HUMIDITY = ' Mean Humidity'

    @staticmethod
    def to_int(text, default):
        text = text.strip()
        return int(text) if text else default

    @staticmethod
    def data_type_conversion(weather_records):
        for row in weather_records:
            row[DataOperations.__PKT] = parser.parse(row[DataOperations.__PKT])
            row[DataOperations.__MAX_TEMPERATURE] = DataOperations. \
                to_int(row[DataOperations.__MAX_TEMPERATURE], -55)
            row[DataOperations.__MIN_TEMPERATURE] = DataOperations. \
                to_int(row[DataOperations.__MIN_TEMPERATURE], 63)
            row[DataOperations.__MAX_HUMIDITY] = DataOperations. \
                to_int(row[DataOperations.__MAX_HUMIDITY], 0)
            row[DataOperations.__MEAN_HUMIDITY] = DataOperations. \
                to_int(row[DataOperations.__MEAN_HUMIDITY], 33)
        return weather_records

    @staticmethod
    def average(weather_records, key):
        sum_weather_parameter = sum(
            single_day[key] for single_day in weather_records)
        return sum_weather_parameter / len(weather_records)

    @staticmethod
    def find_max(weather_records, key):
        max_record = weather_records[max(xrange(
            len(weather_records)),
            key=lambda day: weather_records[day][key])]

        return {
            'key': max_record[key],
            'month': calendar.month_name[max_record[DataOperations.__PKT].month],
            'day': max_record[DataOperations.__PKT].day
        }

    @staticmethod
    def find_min(weather_records, key):
        min_record = weather_records[min(xrange(
            len(weather_records)),
            key=lambda day: weather_records[day][key])]

        return {
            'key': min_record[key],
            'month': calendar.month_name[min_record[DataOperations.__PKT].month],
            'day': min_record[DataOperations.__PKT].day
        }

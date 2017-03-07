import calendar
from dateutil import parser


class DataOperations:
    def __init__(self):
        pass

    PKT = 'PKT'
    MAX_TEMPERATURE = 'Max TemperatureC'
    MIN_TEMPERATURE = 'Min TemperatureC'
    MAX_HUMIDITY = 'Max Humidity'
    MEAN_HUMIDITY = ' Mean Humidity'

    @staticmethod
    def convert_string_to_int(text, default):
        text = text.strip()
        return int(text) if text else default

    @staticmethod
    def data_type_conversion(weather_records):
        for row in weather_records:
            row[DataOperations.PKT] = parser.parse(row[DataOperations.PKT])
            row[DataOperations.MAX_TEMPERATURE] = DataOperations.\
                convert_string_to_int(row[DataOperations.MAX_TEMPERATURE], -55)
            row[DataOperations.MIN_TEMPERATURE] = DataOperations.\
                convert_string_to_int(row[DataOperations.MIN_TEMPERATURE], 63)
            row[DataOperations.MAX_HUMIDITY] = DataOperations.\
                convert_string_to_int(row[DataOperations.MAX_HUMIDITY], 0)
            row[DataOperations.MEAN_HUMIDITY] = DataOperations.\
                convert_string_to_int(row[DataOperations.MEAN_HUMIDITY], 33)
        return weather_records

    @staticmethod
    def calculate_average(weather_records, key):
        sum_weather_parameter = sum(
            single_day[key] for single_day in weather_records)
        return sum_weather_parameter / len(weather_records)

    @staticmethod
    def find_max(tmp_record, weather_records, key):

        single_weather_record = weather_records[max(xrange(
            len(weather_records)),
            key=lambda day: weather_records[day][key])]

        if tmp_record['key'] < single_weather_record[key]:
            tmp_record['key'] = single_weather_record[key]
            tmp_record['month'] = calendar.month_name[
                single_weather_record[DataOperations.PKT].month]
            tmp_record['day'] = single_weather_record[DataOperations.PKT].day
        return tmp_record

    @staticmethod
    def find_min(tmp_record, weather_records, key):

        single_weather_record = weather_records[min(xrange(
            len(weather_records)),
            key=lambda day: weather_records[day][key])]

        if tmp_record['key'] > single_weather_record[key]:
            tmp_record['key'] = single_weather_record[key]
            tmp_record['month'] = calendar.month_name[
                single_weather_record[DataOperations.PKT].month]
            tmp_record['day'] = single_weather_record[DataOperations.PKT].day
        return tmp_record

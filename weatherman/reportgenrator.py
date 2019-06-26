from abc import ABC, abstractmethod
from operator import itemgetter, attrgetter


class ReportGenerator:
    @abstractmethod
    def generate(self):
        pass


class HighLowReportGenerator(ReportGenerator):

    def __init__(self, weather_data):
        self.weather_data = weather_data

    def generate(self):
        max_temp_records = [data for data in self.weather_data if data.max_temp is not None]
        min_temp_records = [data for data in self.weather_data if data.min_temp is not None]
        max_humidity_records = [data for data in self.weather_data if data.max_humidity is not None]
        max_temp_record = max(max_temp_records, key=attrgetter('max_temp'))
        max_humidity_record = max(max_humidity_records, key=attrgetter('max_humidity'))
        min_temp_record = min(min_temp_records, key=attrgetter('min_temp'))
        final_report = HighLowReport(max_temp_record, max_humidity_record, min_temp_record)
        format_str = 'Highest: {}C on {} {}\nLowest {}C on {} {}\nHumidity {}% on {} {}'
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


class HighLowReport:
    def __init__(self, max_temp_record, max_humidity_record, min_temp_record):
        self.max_temp_recod = max_temp_record
        self.max_humidity_record = max_humidity_record
        self.min_temp_record = min_temp_record

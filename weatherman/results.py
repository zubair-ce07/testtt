from operator import attrgetter
from csvparser import CsvParser


class ComputeResult:
    """Compute results from data-set created by CsvParser"""
    def __init__(self):
        self.results_dict = {}

    @staticmethod
    def get_max(data_set, attr):
        """Compute and Return max value object in data-set column"""
        return max(data_set, key=attrgetter(attr))

    @staticmethod
    def get_min(data_set, attr):
        """Compute and Return min value object in data-set column"""
        return min(data_set, key=attrgetter(attr))

    @staticmethod
    def get_avg(data_set, attr):
        """Compute and Return avg value object in data-set column"""
        return sum(getattr(row, attr) for row in data_set) // len(data_set)

    def compute_extreme_weather(self, file_dir, year, month=0):
        csv_parser = CsvParser(file_dir, year, month)
        self.results_dict['max_temp'] = self.get_max(csv_parser.data_set, 'max_temp')
        self.results_dict['min_temp'] = self.get_min(csv_parser.data_set, 'min_temp')
        self.results_dict['max_humidity'] = self.get_max(csv_parser.data_set, 'max_humidity')

    def compute_average_weather(self, file_dir, year, month):
        csv_parser = CsvParser(file_dir, year, month)
        self.results_dict['max_temp'] = self.get_avg(csv_parser.data_set, 'max_temp')
        self.results_dict['min_temp'] = self.get_avg(csv_parser.data_set, 'min_temp')
        self.results_dict['mean_humidity'] = self.get_avg(csv_parser.data_set, 'mean_humidity')


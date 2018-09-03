""" Module for the calculation of month and year """
from statistics import mean
from datetime import datetime
from file_handler import FileHandler
from model_classes import MonthReport, YearReport
from printer import PrintReports
from constants import MONTHS


def get_max_temp_entry(record_list):
    """ return element from list contating maximum temperature """
    return max(([y for y in record_list
                 if y and y.max_temperature is not None]),
               key=lambda x: x.max_temperature)


def get_min_temp_entry(record_list):
    """ return element from list contating minimum temperature """
    return min(([y for y in record_list
                 if y and y.min_temperature is not None]),
               key=lambda x: x.min_temperature)


def get_humidity_entry(record_list):
    """ return element from list contating max humidity """
    return max(([y for y in record_list
                 if y and y.max_humidity is not None]),
               key=lambda x: x.max_humidity)


class ReportGenerator:
    """Generate reports: graph or Avg Report"""

    def month_controller(self, path, year_month, graph):
        """ handle 2 modules of month (display graph, month report) with graph
            flag """
        try:
            [year, month] = year_month.split('/')
            month = int(month)
            month = month - 1

            month_str = datetime.strptime(str(month+1), '%m')
            month_str = (month_str.strftime('%b'))
            file_handler = FileHandler(path)
            month_list = []
            file_handler.get_month_list(month_str, year, month_list)
            month_str = datetime.strptime(year_month,
                                          "%Y/%m").strftime('%B %Y')
            printer = PrintReports()
            if graph is False:
                printer.print_month_graph(month_list, month_str)
            else:
                avg_report = self.generate_month_avg_report(
                    month_list,
                    month_str
                )
                printer.print_report(avg_report)

        except ValueError:
            print("\n<< Invalid month or year [required: year/month]\n")

    def generate_month_avg_report(self, rec_list, month_str):
        """ calculate and return month average report """
        if len(rec_list) > 0:
            max_temp_data = [int(y.max_temperature) for y in rec_list
                             if y.max_temperature is not None]
            max_temp_avg = mean(max_temp_data)

            min_temp_data = [int(y.min_temperature) for y in rec_list
                             if y.min_temperature is not None]
            min_temp_avg = mean(min_temp_data)

            humidity_avg_data = [int(y.mean_humidity) for y in rec_list
                                 if y.mean_humidity is not None]
            humidity_avg = mean(humidity_avg_data)
            avg_report = MonthReport(max_temp_avg, min_temp_avg,
                                     humidity_avg, month_str)
            return avg_report
        else:
            return None

    def year_controller(self, path, year, graph):
        """ handle 2 modules of year (display graph, month report) with graph
            flag """
        file_handler = FileHandler(path)
        year_record_list = []
        printer = PrintReports()
        if graph is False:
            year_record_list = file_handler.get_year_list(year)
            year_report = self.generate_year_report(year_record_list)
            printer.print_report(year_report)

        else:
            year_graph_dict = self.generate_year_graph_data(file_handler, year)
            printer.print_year_graph(year_graph_dict, year)

    def generate_year_graph_data(self, file_handler, year):
        """ generate dictioney d containing data required for graph
            of year """
        cursor = 1
        d = {}
        for month in MONTHS:
            month = MONTHS.get(month)
            month_list = []
            file_handler.get_month_list(month, year, month_list)
            entries = self.handle_year_graph(month_list)
            d[cursor] = entries
            cursor = cursor + 1
        return d

    def handle_year_graph(self, month_list):
        """ return maximum and minimum temperature entries from given list """
        if len(month_list) > 0:
            max_temp_entry = get_max_temp_entry(month_list)
            min_temp_entry = get_min_temp_entry(month_list)
            entries = [max_temp_entry.max_temperature,
                       min_temp_entry.min_temperature]
            return entries
        else:
            return None

    def generate_year_report(self, year_list):
        """ form year report of max temp min temp and humidity"""
        if len(year_list) > 0:
            max_temp_entry = get_max_temp_entry(year_list)
            min_temp_entry = get_min_temp_entry(year_list)
            humidity_entry = get_humidity_entry(year_list)

            year_report = YearReport(
                max_temp_entry.max_temperature,
                max_temp_entry.date,
                min_temp_entry.min_temperature,
                min_temp_entry.date,
                humidity_entry.max_humidity,
                humidity_entry.date
            )
            return year_report
        else:
            return None

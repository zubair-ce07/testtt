""" Module for the calculation of year """
from file_handler import FileHandler
from constants import FILE_MONTHS
from statistics import mean
from datetime import datetime
from model_classes import YearReport
from printer import PrintReports


def get_max_temp_entry(record_list):
    return max(([y for y in record_list
                 if y and y.max_temperature is not None]),
               key=lambda x: x.max_temperature)

def get_min_temp_entry(record_list):
    return min(([y for y in record_list
                 if y and y.min_temperature is not None]),
               key=lambda x: x.min_temperature)


def get_humidity_entry(record_list):
    return max(([y for y in record_list
                 if y and y.max_humidity is not None]),
               key=lambda x: x.max_humidity)


class YearReportGenerator:
    """Generate year reports: graph or Avg Report"""
 
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
            printer.print_year_graph(year_graph_dict,year)


    def generate_year_graph_data(self, file_handler, year):
        cursor = 1
        d ={}
        for month in FILE_MONTHS:
            month = FILE_MONTHS.get(month)
            month_list = []
            file_handler.get_month_list(month, year, month_list)
            entries = self.handle_year_graph(month_list)
            d[cursor] = entries
            cursor = cursor + 1
        return d


    def handle_year_graph(self, month_list):
        if len(month_list) > 0:
            max_temp_entry = get_max_temp_entry(month_list)
            min_temp_entry = get_min_temp_entry(month_list)
            entries = {max_temp_entry.max_temperature,
                       min_temp_entry.min_temperature}
            return entries
        else:
            return None
            
                                     
    def generate_year_report(self, year_list):
        """ Form year report of max temp min temp and humidity"""
        if len(year_list) > 0:
            max_temp_entry = get_max_temp_entry(year_list)
            min_temp_entry =  get_min_temp_entry(year_list)
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

    

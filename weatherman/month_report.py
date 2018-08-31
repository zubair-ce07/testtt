""" Module for the calculation of month """
from file_handler import FileHandler
from statistics import mean
from datetime import datetime
from model_classes import MonthReport
from printer import PrintReports


class MonthReportGenerator:
    """Generate month reports: graph or Avg Report"""
 
    def month_controller(self, path, year_month, graph):
        """ handle 2 modules of month (display graph, month report) with graph
            flag """
        try:
            [year, month] = year_month.split('/')
            month = int(month)
            month = month - 1
            if month > -1 and month < 12:
                month_str = (datetime.strptime(str(month+1),'%m')).strftime('%b')
                file_handler = FileHandler(path)
                month_list = []
                file_handler.get_month_list(month_str, year, month_list)
                month_str = datetime.strptime(year_month,
                                                  "%Y/%m").strftime('%B %Y')
                printer = PrintReports()
                if graph is False:
                    printer.print_month_graph(month_list, month_str)
                else:
                    avg_report = self.generate_month_avg_report(month_list, month_str)
                    printer.print_report(avg_report)
            else:
                print("\n<< Invalid input: month value is not in range\n")

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

    

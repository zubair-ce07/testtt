import sys

from forecast.core.average_report_generator import AverageReportGenerator
from forecast.core.extremes_report_generator import ExtremesReportGenerator
from forecast.core.cumulative_report_generator import CumulativeReportGenerator


class ReportGeneratorFactory:

    __report_generator_dict = {
        'E': ExtremesReportGenerator(),
        'A': AverageReportGenerator(),
        'C': CumulativeReportGenerator(),
        'B': CumulativeReportGenerator(),
    }

    @staticmethod
    def get_report_generator(option):
        try:
            return ReportGeneratorFactory.__report_generator_dict[option]
        except KeyError:
            sys.stderr.write("Invalid command option, %s\n" % option)
            sys.exit(1)
import sys

from a_report_generator import AReportGenerator
from b_report_generator import BReportGenerator
from c_report_generator import CReportGenerator
from e_report_generator import EReportGenerator


class ReportGeneratorFactory:

    __report_generator_dict = {
        '-e': EReportGenerator(),
        '-a': AReportGenerator(),
        '-c': CReportGenerator(),
        '-b': BReportGenerator(),
    }

    @staticmethod
    def get_report_generator(option):
        try:
            return ReportGeneratorFactory.__report_generator_dict[option]
        except KeyError:
            sys.stderr.write("Invalid command option\n")
            sys.exit(1)
import sys

from a_report_generator import AReportGenerator
from b_report_generator import BReportGenerator
from c_report_generator import CReportGenerator
from e_report_generator import EReportGenerator


class ReportGeneratorFactory:
    @staticmethod
    def get_report_generator(option):
        if option == '-e':
            return EReportGenerator()
        elif option == '-a':
            return AReportGenerator()
        elif option == '-c':
            return CReportGenerator()
        elif option == '-b':
            return BReportGenerator()
        else:
            sys.stderr.write("Invalid command option\n")
            sys.exit(1)
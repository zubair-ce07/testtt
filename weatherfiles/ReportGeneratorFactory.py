from AReportGenerator import AReportGenerator
from BReportGenerator import BReportGenerator
from CReportGenerator import CReportGenerator
from EReportGenerator import EReportGenerator


class ReportGeneratorFactory:
    def get_report_generator(self, option):
        if option == '-e':
            return EReportGenerator()
        elif option == '-a':
            return AReportGenerator()
        elif option == '-c':
            return CReportGenerator()
        elif option == '-b':
            return BReportGenerator()
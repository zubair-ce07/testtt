from a_report_generator import AReportGenerator
from b_report_generator import BReportGenerator
from c_report_generator import CReportGenerator
from e_report_generator import EReportGenerator


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
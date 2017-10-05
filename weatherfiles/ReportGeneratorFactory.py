from EReportGenerator import EReportGenerator


class ReportGeneratorFactory:
    def get_report_generator(self, option):
        if option == '-e':
            return EReportGenerator()
import reports
import reportgenerator


def computation_analysis(files_data, report_name, time_period):
    result = []
    if report_name == 'e':
        result = reports.yearly_report(files_data, time_period)
    elif report_name == 'a':
        result = reports.monthly_report(files_data, time_period)
    elif report_name == 'c':
        result = reports.bar_chart_report(files_data, time_period)

    if result:
        reportgenerator.report_generator(report_name, result)


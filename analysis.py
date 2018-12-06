from datetime import datetime
import reports


def computation_analysis(data_set, report_name, time_period):
    result = []
    year, month, complete_date = '', '', ''

    if report_name == 'yearly':
        year = int(time_period)
    elif report_name != 'path':
        date_params = time_period.split('/')
        year = int(date_params[0])
        month = datetime.strptime(time_period, '%Y/%m').strftime('%b')

    if report_name == 'yearly':
        result = reports.yearly_report(data_set, year)
    elif report_name == 'monthly':
        result = reports.monthly_report(data_set, year, month)
    elif report_name == 'bar_chart':
        result = reports.bar_chart_report(data_set, year, month)

    return result

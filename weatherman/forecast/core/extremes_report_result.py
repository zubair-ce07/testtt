from forecast.core.date_utils import DateUtils
from forecast.core.report_result import ReportResult


class ExtremesReportResult(ReportResult):
    def __init__(self, year, month, high_temp_info, low_temp_info, max_humidity_info):
        ReportResult.__init__(self, year, month)
        self.high_temp = high_temp_info[0]
        self.high_temp_on = DateUtils.get_month_and_day(high_temp_info[1])
        self.low_temp = low_temp_info[0]
        self.low_temp_on = DateUtils.get_month_and_day(low_temp_info[1])
        self.max_humidity = max_humidity_info[0]
        self.max_humidity_on = DateUtils.get_month_and_day(max_humidity_info[1])
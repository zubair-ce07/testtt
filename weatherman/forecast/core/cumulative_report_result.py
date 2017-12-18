from forecast.core.report_result import ReportResult


class DayInfo:
    def __init__(self, day_info):
        self.day = day_info.get_day_as_string()
        self.max_temp = day_info.max_temp
        self.min_temp = day_info.min_temp


class CumulativeReportResult(ReportResult):
    def __init__(self, year, month, daily_weathers_info):
        ReportResult.__init__(self, year, month)
        self.daily_weathers_info = [DayInfo(day) for day in daily_weathers_info]

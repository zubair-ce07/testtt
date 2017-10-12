from forecast.core.report_result import ReportResult


class AverageReportResult(ReportResult):
    def __init__(self, year, month, high_temp_average, low_temp_average, average_mean_humidity):
        ReportResult.__init__(self, year, month)
        self.high_temp_average = high_temp_average
        self.low_temp_average = low_temp_average
        self.average_mean_humidity = average_mean_humidity

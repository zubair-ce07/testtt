from ReportModel import MonthlyResult, ChartResult, YearlyResult


class ReportGenerator:
    @staticmethod
    def calculate_monthly_report(reading_list):
        """This function will receive a list of weather obj of a month and returns the DS for monthly report. """
        if not reading_list:
            return None
        highest_avg, lowest_avg, humidity_avg = 0, 0, 0
        for item in reading_list:
            highest_avg += item.highest
            lowest_avg += item.lowest
            humidity_avg += item.mean_humidity
        highest_avg /= len(reading_list)
        lowest_avg /= len(reading_list)
        humidity_avg /= len(reading_list)
        return MonthlyResult(highest_avg, lowest_avg, humidity_avg)

    @staticmethod
    def calculate_yearly_report(reading_list):
        """This function will receive a list of weather obj of a year and returns the DS for Yearly report. """
        if not reading_list:
            return None
        highest = max(reading_list, key=lambda x: x.highest)
        lowest = min(reading_list, key=lambda x: x.lowest)
        humidity = max(reading_list, key=lambda x: x.max_humidity)
        return YearlyResult(highest, lowest, humidity)

    @staticmethod
    def calculate_chart_report(reading_list):
        """This function will receive a list of weather obj of a month and returns the DS for Chart report. """
        if not reading_list:
            return None
        month_chart = ''
        for item in reading_list:
            month_chart += str(ChartResult(item)) + '\n'
        return month_chart

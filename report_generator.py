class ReportGenerator:
    # The variables defined for displaying colored output
    CRED = '\033[91m'
    CBLUE = '\33[94m'
    CEND = '\033[0m'

    def __init__(self):
        self.__report = "NA"

    @property
    def report(self):
        return self.__report

    @report.setter
    def report(self, r):
        self.__report = r

    def set_report_for_e(self, result):
        self.report = "Highest: {}C {}\nLowest: {}C {}\nHumidity: " \
                      "{}% {}".format(
                                result.highest_temperature,
                                result.highest_temperature_day,
                                result.lowest_temperature,
                                result.lowest_temperature_day,
                                result.highest_humidity,
                                result.most_humid_day
                                )

    def set_report_for_a(self, result):
        self.report = "Highest Average: {}C\nLowest Average: {}C" \
                      "\nAverage Mean Humidity: " \
                      "{}%".format(
                            result.highest_temperature,
                            result.lowest_temperature,
                            result.highest_humidity
                            )

    def set_report_for_c(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp, min_temp = abs(temperatures[0]), abs(temperatures[1])
            self.report += "{:02} {} {}\n".format(
                idx+1,ReportGenerator.CRED
                + ''.join(['+' for _ in range(max_temp)])
                + ReportGenerator.CEND,
                max_temp
            )
            self.report += "{:02} {} {}\n".format(
                idx+1, ReportGenerator.CBLUE
                + ''.join(['+' for _ in range(min_temp)])
                + ReportGenerator.CEND,
                min_temp
            )

    def set_report_for_c_bonus(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp, min_temp = abs(temperatures[0]), abs(temperatures[1])
            self.report += "{:02} {}{} {} {}\n".format(
                idx+1, ReportGenerator.CRED
                + ''.join(['+' for _ in range(max_temp)])
                + ReportGenerator.CEND,
                ReportGenerator.CBLUE + ''.join(['+' for _ in range(min_temp)])
                + ReportGenerator.CEND, max_temp, min_temp
            )

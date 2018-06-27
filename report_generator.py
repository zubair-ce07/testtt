class ReportGenerator:
    """The class generates reports according to the provided command and result"""
    # The variables defined for displaying colored output
    CRED = '\033[91m'
    CBLUE = '\33[94m'
    CEND = '\033[0m'

    def __init__(self):
        self.report = "NA"

    def get_report(self, result):
        """The function gets the report depending upon the command provided"""
        if result.get_result_type() == "-e":
            self._get_report_for_e(result)
        elif result.get_result_type() == "-a":
            self._get_report_for_a(result)
        elif result.get_result_type() == "-c":
            self._get_report_for_c(result)
        elif result.get_result_type() == "-cb":
            self._get_report_for_c_bonus(result)
        else:
            self.report = "Invalid command, results not computed!"

    def _get_report_for_e(self, result):
        self.report = "Highest: {}C {}\nLowest: {}C {}" \
                                 "\nHumidity: {}% {}".format(result.get_highest_temperature(),
                                                             result.get_highest_temperature_day(),
                                                             result.get_lowest_temperature(),
                                                             result.get_lowest_temperature_day(),
                                                             result.get_highest_humidity(),
                                                             result.get_most_humid_day())

    def _get_report_for_a(self, result):
        self.report = "Highest Average: {}C\nLowest Average: {}C" \
                                 "\nAverage Mean Humidity: {}%".format(result.get_highest_temperature(),
                                                                       result.get_lowest_temperature(),
                                                                       result.get_highest_humidity())

    def _get_report_for_c(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp, min_temp = temperatures
            self.report += "{:02} {} {}\n".format(idx+1, ReportGenerator.CRED
                                                  + self.__get_starts(max_temp)+ReportGenerator.CEND, max_temp)
            self.report += "{:02} {} {}\n".format(idx+1, ReportGenerator.CBLUE
                                                  + self.__get_starts(min_temp)+ReportGenerator.CEND, min_temp)

    def _get_report_for_c_bonus(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp, min_temp = temperatures
            self.report += "{:02} {}{} {} {}\n".format(idx+1, ReportGenerator.CRED
                                                       + self.__get_starts(max_temp)+ReportGenerator.CEND,
                                                       ReportGenerator.CBLUE+self.__get_starts(min_temp)
                                                       + ReportGenerator.CEND, max_temp, min_temp)

    @staticmethod
    def __get_starts(value):
        stars_str = ""

        try:
            value = int(value)
            # converting value to positive to create bar for -ve values
            value = -1*value if value < 0 else value
            for i in range(value):
                stars_str += "+"
        except ValueError:
            stars_str = ""

        return stars_str

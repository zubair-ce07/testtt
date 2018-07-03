class WeatherReportGenerator:
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
        self.report = f"Highest: {result.highest_temperature}C {result.highest_temperature_day:%B %d}\n" \
                      f"Lowest: {result.lowest_temperature}C {result.lowest_temperature_day:%B %d}\n" \
                      f"Humidity: {result.highest_humidity}% {result.most_humid_day:%B %d}"

    def set_report_for_a(self, result):
        self.report = f"Highest Average: {result.highest_temperature}C\n" \
                      f"Lowest Average: {result.lowest_temperature}C\n" \
                      f"Average Mean Humidity: {result.mean_humidity:.0f}%"

    def set_report_for_c(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp = abs(0 if temperatures[0] == "NA" else abs(temperatures[0]))
            min_temp = abs(0 if temperatures[0] == "NA" else abs(temperatures[1]))

            red_stars = WeatherReportGenerator.CRED+''.join(['+' for _ in range(max_temp)])\
                + WeatherReportGenerator.CEND
            blue_stars = WeatherReportGenerator.CBLUE+''.join(['+' for _ in range(min_temp)])\
                + WeatherReportGenerator.CEND

            self.report += f"{idx+1:02} {red_stars} {max_temp}\n"
            self.report += f"{idx+1:02} {blue_stars} {min_temp}\n"

    def set_report_for_c_bonus(self, result):
        self.report = ""
        for idx, temperatures in enumerate(result.temperature_list):
            max_temp = abs(0 if temperatures[0] == "NA" else abs(temperatures[0]))
            min_temp = abs(0 if temperatures[0] == "NA" else abs(temperatures[1]))

            red_stars = WeatherReportGenerator.CRED+''.join(['+' for _ in range(max_temp)])\
                + WeatherReportGenerator.CEND
            blue_stars = WeatherReportGenerator.CBLUE+''.join(['+' for _ in range(min_temp)])\
                + WeatherReportGenerator.CEND

            self.report += f"{idx+1:02} {red_stars} {blue_stars} {max_temp} {min_temp}\n"

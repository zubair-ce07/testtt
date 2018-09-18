from math import inf
import calendar


class YearReport:

    def __init__(self):
        self.maxTempDate = ""
        self.maxTemp = -inf
        self.minTempDate = ""
        self.minTemp = +inf
        self.maxHumidityDate = ""
        self.maxHumidity = -inf

    def set_accurate_date(self, weatherDict):
        if weatherDict["Max TemperatureC"] is not '':
            if self.maxTemp <= int(weatherDict["Max TemperatureC"]):
                self.maxTempDate = weatherDict["PKT"]
                self.maxTemp = int(weatherDict["Max TemperatureC"])
        if weatherDict["Min TemperatureC"] is not '':
            if self.minTemp >= int(weatherDict["Min TemperatureC"]):
                self.minTempDate = weatherDict["PKT"]
                self.minTemp = int(weatherDict["Min TemperatureC"])
        if weatherDict["Max Humidity"] is not '':
            if self.maxHumidity <= int(weatherDict["Max Humidity"]):
                self.maxHumidityDate = weatherDict["PKT"]
                self.maxHumidity = int(weatherDict["Max Humidity"])

    def print_year_report(self):
                            # Highest: 45C on June 23
                            # Lowest: 01C on December 22
                            # Humidity: 95% on August 14

        print(
            "Highest: " + str(self.maxTemp) + "C " +
            "on " + str(self.date_format(self.maxTempDate))
            )
        print(
            "Lowest: " + str(self.minTemp) + "C " +
            "on " + str(self.date_format(self.minTempDate))
            )
        print(
            "Humidity: " + str(self.maxHumidity) + "% " +
            "on " + str(self.date_format(self.maxHumidityDate))
                )

    def date_format(self, date):
        splitDate = date.split("-")
        return calendar.month_name[int(splitDate[1])] + " " + splitDate[2]
_months_dictionary = {1: "January", 2: "February", 3: "March", 4: "April",
                      5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November",
                      12: "December"}


def _print_sign(num, is_red):
    if is_red is True:
        print('\33[31m', end="")
        for i in range(num):
            print("+", end="")
    else:
        print('\33[34m', end="")
        for i in range(num):
            print("+", end="")
    print('\033[0m', end="")


class ReportGenerator:

    def __init__(self, report_type, given_results):
        self.given_results = given_results
        self.report_type = report_type

    def print_report(self):
        print()
        if self.report_type == "-e":
            date=self.given_results["HighestTemperature"][0].split("-")
            month=_months_dictionary[int(date[1])]
            date=date[2]
            print("Highest: {}C on {}, {}".format(
                int(self.given_results["HighestTemperature"][1]),
                month, date))
            date = self.given_results["LowestTemperature"][0].split("-")
            month = _months_dictionary[int(date[1])]
            date = date[2]
            print("Lowest: {}C on {}, {}".format(
                int(self.given_results["LowestTemperature"][1]),
                month, date))
            date = self.given_results["HighestHumidity"][0].split("-")
            month = _months_dictionary[int(date[1])]
            date = date[2]
            print("Humidity: {}% on {}, {}".format(
                int(self.given_results["HighestHumidity"][1]),
                month, date))

        elif self.report_type == "-a":
            print("Highest Average: ", end="")
            print("%.2fC" % self.given_results["AverageHighestTemperature"])
            print("Lowest Average: ", end="")
            print("%.2fC" % self.given_results["AverageLowestTemperature"])
            print("Average Mean Humidity: ", end="")
            print("%.2f%%" % self.given_results["AverageMeanHumidity"])

        elif self.report_type == "-c":
            print(_months_dictionary[
                      int(self.given_results["DataOfMonth/Year"][0])
                  ], end="")
            print(", %s" % self.given_results["DataOfMonth/Year"][1])
            for i in range(len(
                    self.given_results["MonthsTemperatureRecord"])):
                print()
                days_record = self.given_results["MonthsTemperatureRecord"][i]
                print(days_record[0], end=" ")
                _print_sign(int(days_record[1])
                            if days_record[1] is not None else 0, False)
                _print_sign(int(days_record[2])
                            if days_record[2] is not None else 0, True)
                print(" %sC" % days_record[1]
                      if days_record[1] is not None else "N/A", end="")
                print(" - ", end="")
                print("%sC" % days_record[2]
                      if days_record[2] is not None else "N/A")

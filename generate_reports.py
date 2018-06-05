from typing import Dict
_months_dictionary = {1: "January", 2: "February", 3: "March", 4: "April",
                      5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November",
                      12: "December"}


def _print_sign(num, is_red):
    if num >= 1:
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

    def __init__(
            self,
            report_type: str,
            given_results: dict()):
        self.given_results = given_results
        self.report_type = report_type

    def print_report(self):
        if self.report_type == "-e":
            date = self.given_results["HighestTemperature"][0].split("-")
            print(f"\nHighest: {self.given_results['HighestTemperature'][1]}"
                  f"C on { _months_dictionary[int(date[1])]}, {date[2]}")
            date = self.given_results["LowestTemperature"][0].split("-")
            print(f"Lowest: {self.given_results['LowestTemperature'][1]}"
                  f"C on {_months_dictionary[int(date[1])]}, {date[2]}")
            date = self.given_results["HighestHumidity"][0].split("-")
            print(f"Humidity: {self.given_results['HighestHumidity'][1]}"
                  f" on {_months_dictionary[int(date[1])]}, {date[2]}")
        elif self.report_type == "-a":
            print("\nHighest Average: ", end="")
            print(f"{self.given_results['AverageHighestTemperature']:.2f}C")
            print("Lowest Average: ", end="")
            print(f"{self.given_results['AverageLowestTemperature']:.2f}C")
            print("Average Mean Humidity: ", end="")
            print(f"{self.given_results['AverageMeanHumidity']:.2f}%")
        elif self.report_type == "-c":
            month_and_year = self.given_results["DataOfMonth/Year"]
            print(f"\n{_months_dictionary[month_and_year[0]]}", end="")
            print(f", {month_and_year[1]}")
            for record in self.given_results["MonthsTemperatureRecord"]:
                print(f"\n{record[0]}", end=" ")
                if record[1] is not None:
                    _print_sign(int(record[1]), False)
                if record[2] is not None:
                    _print_sign(int(record[2]), True)
                print(f"{record[1] if record[1] is not None else 'N/A'}C",
                      end="")
                print(" - ", end="")
                print(f"{record[2] if record[2] is not None else 'N/A'}C",
                      end="")

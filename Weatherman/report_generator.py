import calendar


class ReportGenerator:
    """
    This class generate the reports provided the accurate details
    and display it on the console.
    """
    def generate_report_for_yearly_details(self, details):
        """Printing the requried calculations for yearly details"""
        print("Highest: {}C on {} {}".format(
            int(details["Max Temperature"][0]),
            calendar.month_name[details["Max Temperature"][1].month],
            details["Max Temperature"][1].day))
        print("Lowest: {}C on {} {}".format(
            int(details["Min Temperature"][0]),
            calendar.month_name[details["Min Temperature"][1].month],
            details["Min Temperature"][1].day))
        print("Humidity: {}% on {} {}".format(
            int(details["Max Humidity"][0]),
            calendar.month_name[details["Max Humidity"][1].month],
            details["Max Humidity"][1].day))

    def generate_report_for_monthly_details(self, details):
        """Printing the requried calculations for monthly details"""
        print("Highest Average: {}C".format(round(details[0], 2)))
        print("Lowest Average: {}C".format(round(details[1], 2)))
        print("Average Mean Humidity: {}%".format(round(details[2], 2)))

    def generate_graph(self, details):
        """Printing the temperature graph """
        for i, item in enumerate(details):
            if i == 0:
                print(calendar.month_name[item.month], item.year)
            else:
                pass
            if details[item]["Max Temperature"] != "" and details[item][
                "Min Temperature"
            ] != "":
                print(i+1, " ", end="")
                print(
                    '\033[91m' + "+"*int(details[item]["Max Temperature"]) +
                    '\033[0m' + " (" + details[item]["Max Temperature"] + "C)")
                print(i+1, " ", end="")
                print(
                    '\33[34m' +
                    "-"*abs(int(details[item]["Min Temperature"])) +
                    '\33[0m' + " (" + details[item]["Min Temperature"] +
                    "C)\n"
                    )

    def generate_horizontal_graph(self, details):
        """Printing the horizontal temperature graph """
        for i, item in enumerate(details):
            if i == 0:
                print(calendar.month_name[item.month], item.year)
            else:
                pass
            if details[item]["Max Temperature"] != "" and details[item][
                "Min Temperature"
            ] != "":
                print(i+1, " ", end="")
                print(
                    '\33[34m' + "+"*abs(
                        int(details[item]["Min Temperature"])) +
                    '\33[0m', end="")
                print(
                    '\033[91m' +
                    "+"*int(details[item]["Max Temperature"]) +
                    '\033[0m' + " (" + details[item]["Min Temperature"] +
                    "C - " + details[item]["Max Temperature"] + " C)"
                    )

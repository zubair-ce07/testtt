import calendar


class GenerateReports:
    """
    This class generate the reports provided the accurate data
    and display it on the console.
    """

    def __init__(self):
        self.CRED = '\033[91m'
        self.R_END = '\033[0m'
        self.CBLUE = '\33[34m'
        self.B_END = '\33[0m'
        pass

    def generate_report_for_yearly_data(self, data):
        """Printing the requried calculations for yearly data"""
        
        print("------------------------------------------------")
        print("Highest: {}C on {} {}".format(
            int(data["Max Temperature"][0]),
            calendar.month_name[data["Max Temperature"][1].month],
            data["Max Temperature"][1].day))
        print("Lowest: {}C on {} {}".format(
            int(data["Min Temperature"][0]),
            calendar.month_name[data["Min Temperature"][1].month],
            data["Min Temperature"][1].day))
        print("Humidity: {}% on {} {}".format(
            int(data["Max Humidity"][0]),
            calendar.month_name[data["Max Humidity"][1].month],
            data["Max Humidity"][1].day))
        print("------------------------------------------------")

    def generate_report_for_monthly_data(self, data):
        """Printing the requried calculations for monthly data"""
        
        print("------------------------------------------------")
        print("Highest Average: {}C".format(round(data[0], 2)))
        print("Lowest Average: {}C".format(round(data[1], 2)))
        print("Average Mean Humidity: {}%".format(round(data[2], 2)))
        print("------------------------------------------------")

    def generate_graph(self, data):
        """Printing the temperature graph """

        print("------------------------------------------------")
        for i, item in enumerate(data):
            if i == 0:
                print(calendar.month_name[item.month], item.year)
            else:
                pass
            if data[item]["Max Temperature"] != "" and data[item]["Min Temperature"] != "":
                print(i+1, " ", end="")
                print(
                    self.CRED + "+"*int(data[item]["Max Temperature"]) 
                    + self.R_END
                    + " (" + data[item]["Max Temperature"] + "C)")
                print(i+1, " ", end="")
                print(
                    self.CBLUE + "-"*abs(int(data[item]["Min Temperature"])) 
                    + self.B_END
                    + " (" + data[item]["Min Temperature"] + "C)\n")
        print("------------------------------------------------")

    def generate_horizontal_graph(self, data):
        """Printing the horizontal temperature graph """
        
        print("------------------------------------------------")
        for i, item in enumerate(data):
            if i == 0:
                print(calendar.month_name[item.month], item.year)
            else:
                pass
            if data[item]["Max Temperature"] != "" and data[item]["Min Temperature"] != "":
                print(i+1, " ", end="")
                print(self.CBLUE + "+"*abs(int(data[item]["Min Temperature"]))
                + self.B_END, end="")
                print(
                    self.CRED + "+"*int(data[item]["Max Temperature"])
                    + self.R_END
                    + " (" + data[item]["Min Temperature"] + "C - "
                    + data[item]["Max Temperature"] + " C)")
        print("------------------------------------------------")

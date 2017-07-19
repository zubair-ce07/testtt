import calendar


class Report:
    def __init__(self):
        print("")

    def print_red(self, symbols):
        print("\033[91m {}\033[00m".format(symbols), end="")

    def print_blue(self, symbols):
        print("\033[34m {}\033[00m".format(symbols), end="")

    def yearly_report(self, result):

        print("\n\n\t+++Yearly Report+++")

        year_, month, day = result["max_temp_date"].split("-")
        print("Highest:  {0}C on {1} {2}".format(result["max_temp"], calendar.month_name[int(month)], day))
        year_, month, day = result["min_temp_date"].split("-")
        print("Lowest:  {0}C on {1} {2}".format(result["min_temp"], calendar.month_name[int(month)], day))
        year_, month, day = result["max_humidity_date"].split("-")
        print("Humidity:  {0}% on {1} {2}".format(result["max_humidity"], calendar.month_name[int(month)], day))

    def monthly_report(self, result):

        print("\n\n\t+++Monthly Report+++")

        print("Highest Average:       {0}C".format(result["age_max_temp"]))
        print("Lowest Average:        {0}C".format(result["age_min_temp"]))
        print("Average Mean Humidity: {0}%".format(result["age_mean_humidity"]))

    def monthly_bar_chart(self, result):

        print("\n\n\t+++Monthly Bar Chart+++")

        max_temp_list = result["max_temp"]
        min_temp_list = result["min_temp"]

        for i in range(0, len(max_temp_list)):
            print("{0} ".format(i + 1), end="")
            symbolsred = "+" * max_temp_list[i]
            self.print_red(symbolsred)
            print(" {0}C".format(max_temp_list[i]))
            print("{0} ".format(i + 1), end="")
            symbolsblue = "+" * min_temp_list[i]
            self.print_blue(symbolsblue)
            print(" {0}C".format(min_temp_list[i]))

        print("\n\n\t+++Monthly Bar Chart+++")
        print("\t+++Bonus Task+++\n")
        for i in range(0, len(max_temp_list)):
            print("{0} ".format(i + 1), end="")
            symbolsblue = "+" * min_temp_list[i]
            self.print_blue(symbolsblue)
            symbolsred = "+" * max_temp_list[i]
            self.print_red(symbolsred)
            print(" {0}C - {1}C".format(min_temp_list[i], max_temp_list[i]))

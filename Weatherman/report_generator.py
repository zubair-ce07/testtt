class ReportGenerator:
    """ This class generate the reports provided the accurate details
    and display it on the console """

    RED_START = "\033[91m"
    BLUE_START = "\33[34m"
    RED_END = "\033[0m"
    BLUE_END = "\33[0m"

    def generate_yearly_report(self, calculated_records):
        print("Highest: {}C on {} {}".format(
            calculated_records[0].max_temperature,
            calculated_records[0].date.strftime("%B"),
            calculated_records[0].date.day))
        print("Lowest: {}C on {} {}".format(
            calculated_records[1].min_temperature,
            calculated_records[1].date.strftime("%B"),
            calculated_records[1].date.day))
        print("Humidity: {}% on {} {}".format(
            calculated_records[2].max_humidity,
            calculated_records[2].date.strftime("%B"),
            calculated_records[2].date.day))

    def generate_monthly_report(self, calculated_records):
        print("Highest Average: {}C".format(round(calculated_records[0], 2)))
        print("Lowest Average: {}C".format(round(calculated_records[1], 2)))
        print("Average Mean Humidity: {}%".format(round(calculated_records[2], 2)))

    def generate_graph(self, calculated_records):
        print(calculated_records[0].date.strftime("%B"), calculated_records[0].date.year)

        for record in calculated_records:
            print(f"{self.RED_START}+{self.RED_END}" * record.max_temperature, end="")
            print(f"{record.max_temperature}C")
            print(f"{self.BLUE_START}-{self.BLUE_END}" * record.min_temperature, end="")
            print(f"{record.min_temperature}C")

    def generate_horizontal_graph(self, calculated_records):
        print(calculated_records[0].date.strftime("%B"), calculated_records[0].date.year)

        for record in calculated_records:
            print(f"{self.BLUE_START}-{self.BLUE_END}" * record.min_temperature, end="")
            print(f"{self.RED_START}+{self.RED_END}" * record.max_temperature, end="")
            print(f"{record.min_temperature}C-", end="")
            print(f"{record.max_temperature}C")

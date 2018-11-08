class ReportGenerator:
    """ This class generate the reports provided the accurate details
    and display it on the console """

    RED_START = "\033[91m"
    BLUE_START = "\33[34m"
    END = "\033[0m"

    def generate_yearly_report(self, record):
        print(
            f"Highest: {record[0].max_temperature}C on ",
            f"{record[0].date.strftime('%B')}",
            f"{record[0].date.day}")
        print(
            f"Lowest: {record[1].min_temperature}C on ",
            f"{record[1].date.strftime('%B')}",
            f"{record[1].date.day}")
        print(
            f"Humidity: {record[2].max_humidity}% on ",
            f"{record[2].date.strftime('%B')}",
            f"{record[2].date.day}")

    def generate_monthly_report(self, record):
        print(f"Highest Average: {record[0]}C")
        print(f"Lowest Average: {record[1]}C")
        print(f"Average Mean Humidity: {record[2]}%")

    def generate_graph(self, records):
        print(records[0].date.strftime("%B"), records[0].date.year)

        for record in records:
            print(f"{self.RED_START}+{self.END}" * record.max_temperature, end=" ")
            print(f"{record.max_temperature}C")
            print(f"{self.BLUE_START}-{self.END}" * record.min_temperature, end=" ")
            print(f"{record.min_temperature}C")

    def generate_horizontal_graph(self, records):
        print(records[0].date.strftime("%B"), records[0].date.year)

        for record in records:
            print(f"{self.BLUE_START}-{self.END}" * record.min_temperature, end="")
            print(f"{self.RED_START}+{self.END}" * record.max_temperature, end=" ")
            print(f"{record.min_temperature}C-", end="")
            print(f"{record.max_temperature}C")

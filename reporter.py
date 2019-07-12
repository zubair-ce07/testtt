class Reports:

    def report_monthly(self, montly_results):
        print(f"Highest Average: {(montly_results[0])}")
        print(f"Lowest Average: {(montly_results[1])}")
        print(f"Average Mean Humidity:{(montly_results[2])}%\n")

    def report_yearly(self, yearly_records):
        print(f"Highest: {yearly_records[0].highest_temp}'C on"
              f" {yearly_records[0].date.day}"
              f" {yearly_records[0].date.strftime('%b')}")

        print(f"Lowest: {yearly_records[1].lowest_temp}'C on"
              f" {yearly_records[1].date.day}"
              f" {yearly_records[1].date.strftime('%b')}")

        print(f"Humidity: {yearly_records[2].highest_humidity}% on"
              f" {yearly_records[2].date.day}"
              f" {yearly_records[2].date.strftime('%b')}\n")

    def double_chart(self, records):
        for record in records:

            # git shell coloring values
            low = "\033[1;34m+"
            high = "\033[1;31m+"

            print(f"{low * record.lowest_temp}"
                  f" {record.lowest_temp} C")

            print(f"{high * record.highest_temp}"
                  f" {record.highest_temp} C\n")

    def single_chart(self, records):
        for record in records:

            # git shell coloring values
            low = "\033[1;34m+"
            high = "\033[1;31m+"

            print(f"{low * record.lowest_temp}", end='')
            print(f"{high * (record.highest_temp - record.lowest_temp)}"
                  f" {record.lowest_temp} C - {record.highest_temp} C")
from datetime import datetime
from termcolor import colored
from weather import Weather, MIN_TEMPC_COL, MAX_HUMIDITY_COL, MAX_TEMPC_COL


class Report:
    def __init__(self, dir_path):
        self.wm = Weather()
        self.data_dir = dir_path

    def monthly_report(self, year, month):
        self.wm.process_files(self.data_dir, year)
        monthlyData = self.wm.get_monthly_stats(month)
        self.print_monthly_report(monthlyData)

    def yearly_report(self, year):
        self.wm.process_files(self.data_dir)
        yearlyData = self.wm.get_year_stats(year)
        self.print_yearly_report(yearlyData)

    def monthly_horizontal_chart(self, year, month, single_line):
        self.wm.process_files(self.data_dir, year)
        done = self.wm.prepare_dataframe_for_processing(month)
        if not done:
            print("Data not found for given month of the year")
            return
        self.print_monthly_horizontal_chart(single_line)

    def format_date(self, date):
        """
            gets date in a format yyyy-mm-dd
        """
        return datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")

    def print_yearly_report(self, data):
        """
            data type : json
            data schema: {
                temp : {
                    min,
                    minDay,
                    max,
                    maxDay
                },
                humidity: {
                    max,
                    maxDay
                }
            }
        """
        if data is None:
            print("Data not found for year")
            return

        print("Highest: {}C on {}".format
              (data["temp"]["max"], self.format_date(data["temp"]["maxDay"])))

        print("Lowest: {}C on {}".format
              (data["temp"]["min"], self.format_date(data["temp"]["minDay"])))

        print("Humid: {}% on {}".format
              (
                  data["humidity"]["max"],
                  self.format_date(data["humidity"]["maxDay"]))
              )

    def print_monthly_report(self, data):
        """
            data type : json
            data schema: {
                "avg_max_temp": avg_max_temp,
                "avg_min_temp": avg_min_temp,
                "avg_max_humidity": avg_max_humidity,
            }
        """
        if data is None:
            print("Data not found for given month of the year")
            return

        print("Highest Average: {:.2f}C".format(data["avg_max_temp"]))
        print("Lowest Average: {:.2f}C".format(data["avg_min_temp"]))
        print("Average Humidity: {:.2f}%".format(data["avg_max_humidity"]))

    def draw_horizontal_bar(self, day, min, max, single_line):
        bar = '+'
        if single_line:
            print(
                day,
                colored(bar * min, 'blue') + colored(bar * max, 'red'),
                str(min) + "C - " + str(max) + "C"
            )
            return

        print(day, colored(bar * max, 'red'), str(max)+"C")
        print(day, colored(bar * min, 'blue'), str(min)+"C")

    def print_monthly_horizontal_chart(self, single_line):
        df = self.wm.dataframe
        # Droping rows where min, max temp is NAN
        df = df[df[MAX_TEMPC_COL].notnull() & df[MIN_TEMPC_COL].notnull()]
        for index, row in df.iterrows():
            self.draw_horizontal_bar(
                index,
                int(row[MIN_TEMPC_COL]),
                int(row[MAX_TEMPC_COL]),
                single_line
            )

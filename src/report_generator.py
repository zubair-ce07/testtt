class ReportGenerator:
    """
        This class provides methods to display reports on console
    """
    COLOR_BLUE = '\033[1;34;48m'
    COLOR_RED = '\033[1;31;48m'
    COLOR_PURPLE = '\033[3;37;48m'
    COLOR_DEFAULT = '\033[0m'

    def generate_year_report(self, records):
        """
            This method prints extream values weather report
        """
        if not records:
            print('No data found')
            return
        print(f"Highest: {records[0].max_temp}C on "
              f"{records[0].date.strftime('%B')} {records[0].date.day}")
        print(f"Lowest: {records[1].max_temp}C on "
              f"{records[1].date.strftime('%B')} {records[1].date.day}")
        print(f"Humidity: {records[2].mean_humidity}% on "
              f"{records[2].date.strftime('%B')} {records[2].date.day}\n")

    def generate_month_report(self, records):
        """
            This method prints average values weather report
        """
        if not records:
            print('No data found')
            return
        print(f"Highest Average: {records[0]}C")
        print(f"Lowest Average: {records[1]}C")
        print(f"Average Mean Humidity: {records[2]}C\n")

    def generate_month_chart_report(self, records, single_line=False):
        """
            This method prints temparature chart
        """
        if not records:
            print('No data found')
            return
        print(f"{records[0].date.strftime('%B')} {records[0].date.year}")
        for day in records:
            if single_line:
                self.generate_single_line_chart(day)
            else:
                self.generate_multi_line_chart(day)
        print(self.COLOR_DEFAULT)

    def generate_single_line_chart(self, day):
        print(f"{self.COLOR_PURPLE}{str(day.date.day).zfill(2)}", end=' ')
        print(f"{self.COLOR_BLUE}+" * day.min_temp, end='')
        print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{day.min_temp}C", end=' ')
        print(f"{self.COLOR_PURPLE}{day.max_temp}C")

    def generate_multi_line_chart(self, day):
        print(f"{self.COLOR_PURPLE}{str(day.date.day).zfill(2)}", end=' ')
        print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{day.max_temp}C")

        print(f"{self.COLOR_PURPLE}{str(day.date.day).zfill(2)}", end=' ')
        print(f"{self.COLOR_BLUE}+" * day.min_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{day.min_temp}C")

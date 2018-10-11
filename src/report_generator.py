import calculations


class ReportGenerator:
    '''
        This class provides methods to display reports on console
    '''
    COLOR_BLUE = '\033[1;34;48m'
    COLOR_RED = '\033[1;31;48m'
    COLOR_PURPLE = '\033[3;37;48m'
    COLOR_DEFAULT = '\033[0m'
    results = calculations.WeatherCalculations()

    def generate_year_report(self, records):
        '''
            This method prints extream values weather report
        '''
        if not records:
            print('No data found')
            return
        print(
            f"Highest: {records[0].max_temp}C on {records[0].date.strftime('%B')} {records[0].date.day}")
        print(
            f"Lowest: {records[1].max_temp}C on {records[1].date.strftime('%B')} {records[1].date.day}")
        print(
            f"Humidity: {records[2].mean_humidity}% on {records[2].date.strftime('%B')} {records[2].date.day}\n")

    def generate_average_month_report(self, records):
        '''
            This method prints average values weather report
        '''
        if not records:
            print('No data found')
            return
        print(f"Highest Average: {records[0]}C")
        print(f"Lowest Average: {records[1]}C")
        print(f"Average Mean Humidity: {records[2]}C\n")

    def generate_temp_chart(self, records, single_line=False):
        '''
            This method prints temparature chart
        '''
        if not records:
            print('No data found')
            return
        print(f"{records[0].date.strftime('%B')} {str(records[0].date.year)}")
        for day in records:
            if single_line:
                self.generate_single_line_chart(day.date.day, day.max_temp, day.min_temp)
                continue
            self.generate_multi_line_chart(day.date.day, day.max_temp, day.min_temp)
        print(self.COLOR_DEFAULT)

    def generate_single_line_chart(self, day, max_temp, min_temp):
        print(f"{self.COLOR_PURPLE}{day:02d}", end=' ')
        print(f"{self.COLOR_BLUE}+" * min_temp, end='')
        print(f"{self.COLOR_RED}+" * max_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{min_temp}C", end=' ')
        print(f"{self.COLOR_PURPLE}{max_temp}C")

    def generate_multi_line_chart(self, day, max_temp, min_temp):
        print(f"{self.COLOR_PURPLE}{day:02d}", end=' ')
        print(f"{self.COLOR_RED}+" * max_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{max_temp}C")

        print(f"{self.COLOR_PURPLE}{day:02d}", end=' ')
        print(f"{self.COLOR_BLUE}+" * min_temp, end=' ')
        print(f"{self.COLOR_PURPLE}{min_temp}C")

import calculations


class ReportGenerator:
    '''
        This class provides methods to display reports on console
    '''
    COLOR_BLUE = '\033[1;34;48m'
    COLOR_RED = '\033[1;31;48m'
    COLOR_PURPLE = '\033[3;37;48m'
    COLOR_WHITE = '\033[0m'
    results = calculations.WeatherCalculations()

    def print_extreme_record(self, data):
        '''
            This method prints extream values weather report
        '''
        if not data:
            print('No data found')
            return
        extream_values = self.results.extreme_record(data)
        print(f"Highest: {extream_values[0].max_temp}C on {extream_values[0].date.strftime('%B')} {extream_values[0].date.day}")
        print(f"Lowest: {extream_values[1].max_temp}C on {extream_values[1].date.strftime('%B')} {extream_values[1].date.day}")
        print(f"Humidity: {extream_values[2].mean_humidity}% on {extream_values[2].date.strftime('%B')} {extream_values[2].date.day}\n")

    def print_average_record(self, data):
        '''
            This method prints average values weather report
        '''
        if not data:
            print('No data found')
            return
        average_values = self.results.average_values(data)
        print(f"Highest Average: {average_values[0]}C")
        print(f"Lowest Average: {average_values[1]}C")
        print(f"Average Mean Humidity: {average_values[2]}C\n")

    def print_temp_chart(self, data):
        '''
            This method prints temparature chart
        '''
        if not data:
            print('No data found')
            return  
        print(f"{data[0].date.strftime('%B')} {str(data[0].date.year)}")
        for day in data:
            print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')
            print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
            print(f"{self.COLOR_PURPLE}{day.max_temp}C")

            print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')
            print(f"{self.COLOR_BLUE}+" * day.min_temp, end=' ')
            print(f"{self.COLOR_PURPLE}{day.min_temp}C")
        print(self.COLOR_WHITE)

    def print_temp_chart_bounus(self, data):
        '''
            This method prints temparature chart
        '''
        if not data:
            print('No data found')
            return
        print(f"{data[0].date.strftime('%B')} {str(data[0].date.year)}")
        for day in data:
            print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')

            print(f"{self.COLOR_BLUE}+" * day.min_temp, end='')
            print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
            print(f"{self.COLOR_PURPLE}{day.min_temp}C", end=' ')
            print(f"{self.COLOR_PURPLE}{day.max_temp}C")
        print(self.COLOR_WHITE)

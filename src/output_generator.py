import datetime
import calendar
import calculations


class OutputGenerator:
    '''
        This class provides methods to display reports on console
    '''
    COLOR_BLUE = '\033[1;34;48m'
    COLOR_RED = '\033[1;31;48m'
    COLOR_PURPLE = '\033[3;37;48m'
    COLOR_WHITE = '\033[0m'
    dir_path = ''
    results = calculations.WeatherCalculations()

    def print_extreme_record(self, year_data):
        '''
            This method prints weather report for -e argument
        '''
        result = self.results.highest_temparature_record(year_data)
        print(
            f"Highest: {result.max_temp}C on " +
            f"{calendar.month_name[result.date.month]} {result.date.day}")

        result = self.results.lowest_temparature_recored(year_data)
        print(
            f"Lowest: {result.max_temp}C on " +
            f"{calendar.month_name[result.date.month]} {result.date.day}")

        result = self.results.highest_humidity_recored(year_data)
        print(
            f"Humidity: {result.mean_humidity}% on " +
            f"{calendar.month_name[result.date.month]} {result.date.day}\n")

    def print_average_record(self, month_data):
        '''
            This method prints weather report for -a argument
        '''
        if(month_data):
            high_temp = self.results.average_max_temp(month_data)
            low_temp = self.results.average_min_temp(month_data)
            average_mean = self.results.average_mean_humidity(month_data)
            print(f"Highest Average: {high_temp}C")
            print(f"Lowest Average: {low_temp}C")
            print(f"Average Mean Humidity: {average_mean}C\n")

    def print_temp_chart(self, month_data):
        '''
            This method prints weather report for -c argument
        '''
        if(month_data):
            heading = None
            for day in month_data:
                if not heading:
                    heading = calendar.month_name[day.date.month] + \
                        ' ' + str(day.date.year)
                    print(heading)
                print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')
                print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
                print(f"{self.COLOR_PURPLE}{day.max_temp}C")

                print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')
                print(f"{self.COLOR_BLUE}+" * day.min_temp, end=' ')
                print(f"{self.COLOR_PURPLE}{day.min_temp}C")
            print(self.COLOR_WHITE)

    def print_temp_chart_bounus(self, month_data):
        '''
            This method prints weather report for -c argument
        '''
        if(month_data):
            heading = None
            for day in month_data:
                if not heading:
                    heading = calendar.month_name[day.date.month] + \
                        ' ' + str(day.date.year)
                    print(heading)
                print(f"{self.COLOR_PURPLE}{day.date.day:02d}", end=' ')

                print(f"{self.COLOR_BLUE}+" * day.min_temp, end='')
                print(f"{self.COLOR_RED}+" * day.max_temp, end=' ')
                print(f"{self.COLOR_PURPLE}{day.min_temp}C", end=' ')
                print(f"{self.COLOR_PURPLE}{day.max_temp}C")
            print(self.COLOR_WHITE)

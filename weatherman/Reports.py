import calendar


class Report:

    def show_yearly_results(self, result):
        print(f"Highest: {result.high_temp}C on {calendar.month_name[result.date_high_temp.month]} "
              f"{result.date_high_temp.day}")
        print(f"Lowest: {result.low_temp}C on {calendar.month_name[result.date_low_temp.month]} "
              f"{result.date_low_temp.day}")
        print(f"Humidity: {result.humidity}% on {calendar.month_name[result.date_humidity.month]} "
              f"{result.date_humidity.day}")

    def show_monthly_avgs(self, result_avgs):
        print(f"Highest Average: {result_avgs.high_temp}C")
        print(f"Lowest Average: {result_avgs.low_temp}C")
        print(f"Average Mean Humidity: {result_avgs.mean_humidity}%")

    def show_monthly_temps(self, readings, month, bonus):
        for day in readings:
            if day.date_high_temp.strftime('%Y/%m') == month:
                if bonus and day.high_temp and day.low_temp:
                    high_temp = '\033[31m' + "+" * int(day.high_temp) + '\033[30m'
                    low_temp = '\033[34m' + '+' * int(day.low_temp) + '\033[30m'
                    print(f"{day.date_high_temp.day} {high_temp}"f"{low_temp}"f"{day.high_temp}C - {day.low_temp}C ")
                else:
                    if day.high_temp and day.low_temp:
                        high_temp = '\033[31m' + "+" * int(day.high_temp) + '\033[30m'
                        low_temp = '\033[34m' + '+' * int(day.low_temp) + '\033[30m'
                        print(f"{day.date_high_temp.day} {high_temp}{day.high_temp}C")
                        print(f"{day.date_high_temp.day} {low_temp}{day.low_temp}C")

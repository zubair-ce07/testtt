import calendar


class Report:

    def show_yearly_results(self, result):
        print(f"Highest: {result.highest_temp}C on { calendar.month_name[result.date_highest_temp.month]} "
              f"{result.date_highest_temp.day}")
        print(f"Lowest: {result.lowest_temp}C on {calendar.month_name[result.date_lowest_temp.month]} "
              f"{result.date_lowest_temp.day}")
        print(f"Humidity: {result.top_humidity}% on {calendar.month_name[result.date_humidity.month]} "
              f"{result.date_humidity.day}")

    def show_monthly_avgs(self, result_avgs):
        print("Highest Average: %sC" % result_avgs.highest_temp)
        print("Lowest Average: %sC" % result_avgs.lowest_temp)
        print("Average Mean Humidity: %s%%" % result_avgs.top_humidity)

    def show_monthly_temps(self, readings, bonus):
        for day in readings:
            if bonus:
                print("%s %s%s%sC - %sC " % (day.date.day, '\033[31m' + "+" * int(day.high_temp) + '\033[30m',
                                             '\033[34m' + "+" * int(day.low_temp) + '\033[30m',
                                             day.high_temp, day.low_temp))
            else:
                print("%s %s%sC" % (day.date.day, '\033[31m' + "+" * int(day.high_temp) + '\033[30m', day.high_temp))
                print("%s %s%sC" % (day.date.day, '\033[34m' + "+" * int(day.low_temp) + '\033[30m', day.low_temp))

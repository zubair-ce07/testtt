import calendar


class Report:

    def show_yearly_results(self, result):
        print("Highest: %sC on %s %s" % (result.highest_temp, calendar.month_name[result.date_highest_temp.month],
                                         result.date_highest_temp.day))
        print("Lowest: %sC on %s %s" % (result.lowest_temp, calendar.month_name[result.date_lowest_temp.month],
                                        result.date_lowest_temp.day))
        print("Humidity: %s%% on %s %s" % (result.top_humidity, calendar.month_name[result.date_humidity.month],
                                           result.date_humidity.day))

    def show_monthly_avgs(self, result_avgs):
        print("Highest Average: %sC" % result_avgs.avg_highest)
        print("Lowest Average: %sC" % result_avgs.avg_lowest)
        print("Average Mean Humidity: %s%%" % result_avgs.avg_mean_humidity)

    def show_monthly_temps(self, readings, bonus):
        for day in readings:
            if bonus:
                print("%s %s%s%sC - %sC " % (day.date.day, '\033[31m' + "+" * int(day.high_temp) + '\033[30m',
                                             '\033[34m' + "+" * int(day.low_temp) + '\033[30m',
                                             day.high_temp, day.low_temp))
            else:
                print("%s %s%sC" % (day.date.day, '\033[31m' + "+" * int(day.high_temp) + '\033[30m', day.high_temp))
                print("%s %s%sC" % (day.date.day, '\033[34m' + "+" * int(day.low_temp) + '\033[30m', day.low_temp))

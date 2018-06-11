from MonthlyReportGenerator import MonthlyReportGenerator
from calendar import monthrange


class MonthlyResutCalculator:

    def __init__(self):
        self.month_wise_list = []

    def do_month_wise_calculation(self, weather_list, yearMon):
        dat_mon = yearMon.split("/")
        year_mon = dat_mon[0] + "-" + dat_mon[1]
        for wtr in weather_list:
            if (year_mon in str(wtr.pkt)):
                self.month_wise_list.append(wtr)

        if (len(self.month_wise_list) > 0):
            monthlyGenerator = MonthlyReportGenerator()
            monthlyGenerator.generate_monthly_report(self.get_avg_highest_temp_for_month(dat_mon[0], dat_mon[1]), \
                                                     self.get_avg_lowest_temp_for_month(dat_mon[0], dat_mon[1]), \
                                                     self.get_avg_mean_humidity_for_month(dat_mon[0], dat_mon[1]))
        else:
            print("No data available against this input")

    def get_avg_highest_temp_for_month(self, year, mon):
        return (sum([int(x) for x in self.month_wise_list[0].max_temperature_c if x is not None])\
                                       /(monthrange(int(year), int(mon)))[1])

    def get_avg_lowest_temp_for_month(self, year, mon):
       return (sum([int(x) for x in self.month_wise_list[0].min_temperature_c if x is not None])\
                                       /(monthrange(int(year), int(mon)))[1])

    def get_avg_mean_humidity_for_month(self, year, mon):
       return (sum([int(x) for x in self.month_wise_list[0].mean_humidity if x is not None])\
                                       /(monthrange(int(year), int(mon)))[1])


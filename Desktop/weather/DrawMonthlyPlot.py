from calendar import monthrange
import matplotlib.pyplot as plt


class DrawMonthlyPlot:

    def __init__(self):
        self.month_list = []

    def draw(self, weather_list, year_mon):
        dat_mon = year_mon.split("/")
        year_mon = "{0}-{1}".format(dat_mon[0], dat_mon[1])
        for year in weather_list:
            if year_mon in str(year.pkt):
                self.month_list.append(year)

        i = 0
        min_list = []
        max_list = []
        no_of_days = []
        days_count_for_month = monthrange(int(dat_mon[0]), int(dat_mon[1]))[1]
        while i < days_count_for_month:
            min_list.append(self.month_list[0].min_temperature_c[i])
            max_list.append(self.month_list[0].max_temperature_c[i])
            i+=1
            no_of_days.append(i)

        min_list = [0 if i == None else int(i) for i in min_list]
        max_list = [0 if i == None else int(i) for i in max_list]
        plt.bar(no_of_days, max_list, .5, align='center', label='max', color=['red'])
        plt.bar(no_of_days, min_list, .5, align='center', label='min', color=['blue'])
        plt.xticks(no_of_days)
        plt.yticks(max_list)
        plt.ylabel('Temperature')
        plt.xlabel('Date')
        plt.legend(loc='upper right')
        plt.show()

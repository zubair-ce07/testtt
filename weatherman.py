import calendar
from os import path
import statistics
from termcolor import colored
import sys


# ___________________________________________________________________________
class monthly_data:
    def __init__(self, mon=0, year=0):
        self.month_name = ''
        self.day = []
        self.max_temp = []
        self.mean_temp = []
        self.min_temp = []
        self.max_dew = []
        self.mean_dew = []
        self.min_dew = []
        self.max_hum = []
        self.mean_hum = []
        self.min_hum = []
        self.max_sealvl = []
        self.mean_sealvl = []
        self.min_sealvl = []
        self.max_vis = []  # float
        self.mean_vis = []  # float
        self.min_vis = []  # float
        self.max_windspeed = []
        self.mean_windspeed = []
        self.max_gust = []
        self.preci = []  # float
        self.cloud_cover = []
        self.event = []  # string
        self.wind_deg = []

        if mon != 0 and year != 0:
            self.get_data(mon, year)

    def get_data(self, mon, year):
        self.month_name = mon_name = calendar.month_name[mon]
        mon_name = mon_name[:3]
        path_name = "weatherfiles/weatherfiles/Murree_weather_"
        + str(year) + "_" + mon_name + ".txt"

        if path.exists(path_name):
            file = open(path_name)
            file.readline()
            for x in file:
                data = x.split(',')  # while line
                date = data[0].split('-')
                self.day.append(int(date[2]))  # this is only date

                self.max_temp.append(self.val_type(data[1], int))
                self.mean_temp.append(self.val_type(data[2], int))
                self.min_temp.append(self.val_type(data[3], int))

                self.max_dew.append(self.val_type(data[4], int))
                self.mean_dew.append(self.val_type(data[5], int))
                self.min_dew.append(self.val_type(data[6], int))

                self.max_hum.append(self.val_type(data[7], int))
                self.mean_hum.append(self.val_type(data[8], int))
                self.min_hum.append(self.val_type(data[9], int))

                self.max_sealvl.append(self.val_type(data[10], int))
                self.mean_sealvl.append(self.val_type(data[11], int))
                self.min_sealvl.append(self.val_type(data[12], int))

                self.max_vis.append(self.val_type(data[13], float))
                self.mean_vis.append(self.val_type(data[14], float))
                self.min_vis.append(self.val_type(data[15], float))

                self.max_windspeed.append(self.val_type(data[16], int))
                self.mean_windspeed.append(self.val_type(data[17], int))

                self.max_gust.append(self.val_type(data[18], int))

                self.preci.append(self.val_type(data[19], float))

                self.cloud_cover.append(self.val_type(data[20], int))

                self.event.append(data[21])

                self.wind_deg.append(self.val_type(data[22], int))

    def val_type(self, val, tp):  # tp for type of val
        if val == '':
            val = 0
        elif val == '\n':
            return None
        else:
            x = val.split('.')
            val = x[0]
        return tp(val)


# ___________________________________________________________________________

class yearly_data:
    def __init__(self, year=0):
        self.months = []
        if year != 0:
            self.get_m_data(year)

    def get_m_data(self, year):
        for i in range(1, 13):
            mon_name = calendar.month_name[i]
            mon_name = mon_name[:3]
            path_name = "weatherfiles/weatherfiles/Murree_weather_"
            + str(year) + "_" + mon_name + ".txt"

            if path.exists(path_name):
                temp = monthly_data(i, year)
                self.months.append(temp)


# ___________________________________________________________________________
class calc:
    def __init__(self):
        pass

    def show_yearly_data(self, year):
        y1 = yearly_data(year)
        self.__show_data_y(y1)

    def show_monthly_data_avg(self, mon, year):
        m1 = monthly_data(mon, year)
        print('\n ::: Monthly Averages :::')
        self.__show_avg_h_t(m1)
        self.__show_avg_l_t(m1)
        self.__show_avg_mean_h_t(m1)

    def show_monthly_horizontal_chart(self, mon, year):
        m2 = monthly_data(mon, year)
        print('\n ::: Monthly Horizontal Report :::')
        for i in range(len(m2.max_temp)):
            print('\n', i+1, colored('+'*m2.max_temp[i], 'red'), m2.max_temp[i], 'C')
            print('', i+1, colored('+'*m2.min_temp[i], 'blue'), m2.min_temp[i], 'C')

    def __show_data_y(self, y1):
        max_t = -9999
        d_mxt = 0
        m_mxt = ''

        min_t = 9999
        d_mnt = 0
        m_mnt = ''

        max_h = -9999
        d_mxh = 0
        m_mxh = ''
        for x in y1.months:
            max_t, d_mxt, m_mxt = self.__get_h_t(x, max_t, d_mxt, m_mxt)
            min_t, d_mnt, m_mnt = self.__get_l_t(x, min_t, d_mnt, m_mnt)
            max_h, d_mxh, m_mxh = self.__get_h_h(x, max_h, d_mxh, m_mxh)

        print('\n ::: Yearly Data :::')
        print(' Highest Temperature : ',  max_t, 'C on',  m_mxt, ',', d_mxt)
        print(' Lowest Temperature  : ',  min_t, 'C on ',  m_mnt, ',', d_mnt)
        print(' Highest Humidity    : ',  max_h, '% on',  m_mxh, ',', d_mxh)

    def __show_avg_h_t(self, m1):
        print(' Highest Average : ', int(statistics.mean(m1.max_temp)), 'C')

    def __show_avg_l_t(self, m1):
        print(' Lowest Average : ', int(statistics.mean(m1.min_temp)), 'C')

    def __show_avg_mean_h_t(self, m1):
        print(' Average Mean Humidity : ', int(statistics.mean(m1.mean_hum)), '%')

    def __get_h_t(self, x, max_t, d_mxt, m_mxt):  # returns highest temperature with date and month
        for i in range(len(x.max_temp)):
            var = x.max_temp[i]
            if var > max_t:
                max_t = var
                d_mxt = i+1
                m_mxt = x.month_name

        return max_t, d_mxt, m_mxt

    def __get_l_t(self, x, min_t, d_mnt, m_mnt):  # returns lowest temperature with date and month
        for i in range(len(x.min_temp)):
            var = x.min_temp[i]
            if var < min_t:
                min_t = var
                d_mnt = i+1
                m_mnt = x.month_name

        return min_t, d_mnt, m_mnt

    def __get_h_h(self, x, max_h, d_mxh, m_mxh):  # returns highest humidity with date and month
        for i in range(len(x.max_hum)):
            var = x.max_hum[i]
            if var > max_h:
                max_h = var
                d_mxh = i+1
                m_mxh = x.month_name

        return max_h, d_mxh, m_mxh
# ___________________________________________________________________________


flag = sys.argv[1]
print(flag)
if flag == '-e':
    year = sys.argv[2]
    c1 = calc()
    c1.show_yearly_data(int(year))
else:
    var = sys.argv[2]
    var = var.split('/')
    year, mon = var[0], var[1]
    if flag == '-a':
        c1 = calc()
        c1.show_monthly_data_avg(int(mon), int(year))
    elif flag == '-c':
        c1 = calc()
        c1.show_monthly_horizontal_chart(int(mon), int(year))

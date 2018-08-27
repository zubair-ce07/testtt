""" contain all functions to display reports """
from datetime import datetime
from classes import (Temperature, Dew, Humidity,
                     SeaLevel, Visiblity, WindSpeed,
                     DayRecord, MonthReport, MonthAvgReport,
                     YearReport, Count)


CRED = '\033[91m'
CBLUE = '\033[94m'
CEND = '\033[0m'


DEFAULT = -1000
DEFAULT_DATE = datetime.strptime("1970-01-01", '%Y-%m-%d')
FILE_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'NOV', 'DEC']


def read_single_line_record(day_data):
    """ get single line record array and return class object"""
    try:
        temp = Temperature(int(day_data[1] or DEFAULT),
                           int(day_data[2] or DEFAULT),
                           int(day_data[3] or DEFAULT))
        dew = Dew(int(day_data[4] or DEFAULT),
                  int(day_data[5] or DEFAULT),
                  int(day_data[6] or DEFAULT))
        humidity = Humidity(int(day_data[7] or DEFAULT),
                            int(day_data[8] or DEFAULT),
                            int(day_data[9] or DEFAULT))
        sea_level_p = SeaLevel(float(day_data[10] or DEFAULT),
                               float(day_data[11] or DEFAULT),
                               float(day_data[12] or DEFAULT))
        visiblity = Visiblity(float(day_data[13] or DEFAULT),
                              float(day_data[14] or DEFAULT),
                              float(day_data[15] or DEFAULT))
        wind_speed = WindSpeed(float(day_data[16] or DEFAULT),
                               float(day_data[17] or DEFAULT))
        date = datetime.strptime(day_data[0], '%Y-%m-%d')
        day_record = DayRecord(date, temp, dew, humidity, sea_level_p,
                               visiblity, wind_speed,
                               float(day_data[18] or DEFAULT),
                               float(day_data[19] or DEFAULT),
                               int(day_data[20] or DEFAULT),
                               str(day_data[21] or ""),
                               int(day_data[22] or DEFAULT))
        return day_record

    except:
        return None


def calculate_month_avg_file(filename, rec_list, month_report, month_str):
    """ calculate and return month average report """
    try:
        with open(filename, 'r') as reader:
            header = reader.readline()
            for line in reader:
                day_data = line.split(',')
                day_record = read_single_line_record(day_data)
                if day_record is not None:
                    if day_record.temp.max_temp != DEFAULT:
                        month_report.max_temp_sum += day_record.temp.max_temp
                        month_report.count.max_temp += 1
                    if day_record.temp.min_temp != DEFAULT:
                        month_report.min_temp_sum += day_record.temp.min_temp
                        month_report.count.min_temp += 1
                    if day_record.humidity.mean_humidity != DEFAULT:
                        month_report.humidity_sum += day_record.humidity.mean_humidity
                        month_report.count.humidity += 1
                    rec_list.append(day_record)
            max_temp_avg = (float(month_report.max_temp_sum) /
                            (month_report.count.max_temp))
            min_temp_avg = (float(month_report.min_temp_sum) /
                            (month_report.count.min_temp))
            humidity_avg = (float(month_report.humidity_sum) /
                            (month_report.count.humidity))
            avg_report = MonthAvgReport(max_temp_avg, min_temp_avg,
                                        humidity_avg, month_str)
            return avg_report

        if not header:
            print("<< Empty file: "+filename)
            return None

    except IOError as err:
        print("\n<< I/O error({0}: {1})".format(err.errno, err.strerror))
        return None


def calculate_month_year_file(filename, rec_list, year_report,):
    """ helping function to form year report """
    try:
        with open(filename, 'r') as reader:
            header = reader.readline()
            for line in reader:
                day_data = line.split(',')
                day_record = read_single_line_record(day_data)
                if day_record is not None:
                    if (day_record.temp.max_temp != DEFAULT and
                            day_record.temp.max_temp > year_report.max_temp):
                        year_report.max_temp = day_record.temp.max_temp
                        year_report.max_temp_date = day_record.date
                    if (day_record.temp.min_temp != DEFAULT and
                            day_record.temp.min_temp < year_report.min_temp):
                        year_report.min_temp = day_record.temp.min_temp
                        year_report.min_temp_date = day_record.date
                    if (day_record.humidity.max_humidity != DEFAULT and
                            day_record.humidity.max_humidity >
                            year_report.humidity):
                        year_report.humidity = day_record.humidity.max_humidity
                        year_report.humidity_date = day_record.date
                    rec_list.append(day_record)

        if not header:
            print("<< Empty file "+filename)
        return year_report

    except IOError:
        # print("I/O error({0}: {1})".format(err.errno, err.strerror))
        return year_report


def display_oneline_year_graph(month_report, cursor):
    """ display one line graph from of single month report """
    print(str(cursor).zfill(2), end=" ")
    if month_report.max_temp != -1000 and month_report.min_temp != 1000:
        for _ in range(month_report.max_temp):
            print(CRED + "*" + CEND, end="")
        for _ in range(month_report.min_temp):
            print(CBLUE + "*" + CEND, end="")
        print(" ", str(month_report.max_temp)+"C",
              "-", str(month_report.min_temp) + "C")
    else:
        print("-")


def display_year_report(path, year, graph):
    """ read line from given path and then display year report or
        year grap on the bases of graph flag """
    year_record_list = []
    year_report = YearReport(int(DEFAULT), DEFAULT_DATE,
                             int(1000), DEFAULT_DATE,
                             int(DEFAULT), DEFAULT_DATE)
    if graph is False:
        for month in FILE_MONTHS:
            file_name = path + "/Murree_weather_" + year + "_" + month + ".txt"
            year_report = calculate_month_year_file(file_name,
                                                    year_record_list,
                                                    year_report)
        print("")
        if year_report is not None:
            year_report.display()

    else:
        cursor = 1
        print("\n" + str(year), " Graph")
        for month in FILE_MONTHS:
            file_name = path + "/Murree_weather_" + year + "_" + month + ".txt"
            year_report = calculate_month_year_file(file_name,
                                                    year_record_list,
                                                    year_report)
            display_oneline_year_graph(year_report, cursor)
            cursor = cursor + 1
            year_report = YearReport(int(DEFAULT), DEFAULT_DATE,
                                     int(1000), DEFAULT_DATE,
                                     int(DEFAULT), DEFAULT_DATE)
        print("")


def month_display_graph_file(filename, rec_list):
    """ read line from given file and display graph report of month """
    try:
        with open(filename, 'r') as reader:
            header = reader.readline()
            for line in reader:
                day_data = line.split(',')
                day_record = read_single_line_record(day_data)
                if day_record is not None:
                    print((day_record.date).strftime('%d'), end=" ")
                    if day_record.temp.max_temp != DEFAULT:
                        for _ in range(day_record.temp.max_temp):
                            print(CRED+"+"+CEND, end="")
                        print(" "+CRED+str(day_record.temp.max_temp)+"C"+CEND)
                    print((day_record.date).strftime('%d'), end=" ")
                    if day_record.temp.min_temp != DEFAULT:
                        for _ in range(day_record.temp.min_temp):
                            print(CBLUE+"+"+CEND, end="")
                        print(" "+CBLUE+str(day_record.temp.min_temp)+"C"+CEND)
                    rec_list.append(day_record)
            print("")
        if not header:
            print("<< Empty file "+filename)

    except IOError as err:
        print("\n<< I/O error({0}: {1})".format(err.errno, err.strerror))


def display_month_report(path, year_month, graph):
    """ handle 2 modules of month (display graph, month report) with graph
        flag """
    try:
        [year, month] = year_month.split('/')
        month = int(month)
        month = month - 1
        if month > -1 and month < 12:
            file_name = (path + "/Murree_weather_" + year +
                         "_" + FILE_MONTHS[month] + ".txt")
            month_record_list = []
            if graph is False:
                month_str = datetime.strptime(year_month,
                                              "%Y/%m").strftime('%B %Y')
                count = Count(0, 0, 0)
                month_report = MonthReport(0, 0, 0, count)
                avg_report = calculate_month_avg_file(file_name,
                                                      month_record_list,
                                                      month_report,
                                                      month_str)
                print("")
                if avg_report is not None:
                    avg_report.display()
            else:
                print("")
                print(datetime.strptime(year_month,
                                        "%Y/%m").strftime('%B %Y'))
                month_display_graph_file(file_name, month_record_list)
        else:
            print("\n<< Invalid input: month value is not in range\n")

    except ValueError:
        print("\n<< Invalid month or year [required: year/month]\n")
